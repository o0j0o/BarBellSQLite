<#
.SYNOPSIS
  Checks the BarBell installer end to end, unattended. Prints PASS / FAIL for each check.

.DESCRIPTION
  Run it from an ELEVATED PowerShell (right-click -> Run as administrator) on a Windows 11 PC where
  unsigned programs are allowed to run. It installs BarBell into a throwaway folder
  (C:\BarBell-InstallTest by default), exercises the installer with /VERYSILENT, and removes
  everything afterwards. It never touches C:\BarBell or your real data, and refuses to run if a real
  BarBell is registered on this PC.

  Checks (the four you asked for):
    1. Install and start the app       - files, shortcuts, registry, the app starts and says 1.2.1 Beta
    2. Upgrade keeps data              - existing install detected, database + counters backed up BEFORE any
                                         file is changed, and left unchanged afterwards
    3. Restore paths                   - restore from the installer's backup (with a damaged database), a
                                         database file on a "new machine", start blank - counters never go back
    4. Uninstall keeps data            - program removed; database, counters and backups are not

  Needs Python on PATH (it uses the project's own source to make and inspect test data).

.EXAMPLE
  .\installer\test_installer.ps1
  .\installer\test_installer.ps1 -Setup "C:\path\BarBell-Setup-1.2.1-Beta.exe" -KeepFiles
#>
[CmdletBinding()]
param(
  [string]$Setup,
  [string]$Root = 'C:\BarBell-InstallTest',
  [string]$Python = 'python',
  [switch]$KeepFiles
)

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$tool = Join-Path $here 'data_tool.py'
if (-not $Setup) {
  # the finished installer is put in installer\Output beside this script; the build folder is the fallback
  $Setup = (Get-ChildItem "$here\Output\BarBell-Setup-*.exe", "$env:LOCALAPPDATA\BarBellBuild\Output\BarBell-Setup-*.exe" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
}
$expectedLabel = '1.2.1 Beta'
$regKey = 'HKLM:\SOFTWARE\Caribbean Label Crafts\BarBell'
$A = Join-Path $Root 'A'          # the install under test
$B = Join-Path $Root 'B'          # a "new machine"
$Backups = Join-Path $Root 'installer-backups'
$Good = Join-Path $Root 'good'    # a known-good database to restore from

$script:results = New-Object System.Collections.ArrayList

function Check([string]$Name, [scriptblock]$Body) {
  try {
    $r = & $Body
    if ($r -eq $false) { throw 'the check returned false' }
    [void]$script:results.Add([pscustomobject]@{ Name = $Name; Pass = $true; Detail = '' })
    Write-Host "  PASS  $Name" -ForegroundColor Green
  } catch {
    [void]$script:results.Add([pscustomobject]@{ Name = $Name; Pass = $false; Detail = $_.Exception.Message })
    Write-Host "  FAIL  $Name   <-- $($_.Exception.Message)" -ForegroundColor Red
  }
}
function Assert($Condition, [string]$Message) { if (-not $Condition) { throw $Message } }

function Tool([string[]]$ToolArgs) {
  $out = & $Python $tool @ToolArgs
  if ($LASTEXITCODE -ne 0) { throw "data_tool $($ToolArgs -join ' ') failed: $out" }
  ($out | Out-String) | ConvertFrom-Json
}

function Run-Setup([string[]]$Extra, [string]$LogName) {
  $log = Join-Path $Root $LogName
  $all = @('/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/SP-', "/LOG=`"$log`"", "/BACKUPROOT=`"$Backups`"") + $Extra
  $p = Start-Process -FilePath $Setup -ArgumentList ($all -join ' ') -Wait -PassThru
  $text = ''
  if (Test-Path $log) { $text = Get-Content $log -Raw }
  [pscustomobject]@{ Code = $p.ExitCode; Log = $log; Text = $text }
}

function Run-App([string]$Exe, [string[]]$AppArgs) {
  $p = Start-Process -FilePath $Exe -ArgumentList ($AppArgs -join ' ') -Wait -PassThru
  $p.ExitCode
}

function Newest-PreInstallBackup {
  Get-ChildItem $Backups -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -like 'barbell_backup_*_pre-install*' } |
    Sort-Object Name | Select-Object -Last 1
}

function Uninstall([string]$Dir) {
  $u = Join-Path $Dir 'unins000.exe'
  if (Test-Path $u) { Start-Process -FilePath $u -ArgumentList '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART' -Wait }
}

# --------------------------------------------------------------------------- before anything
Write-Host ''
Write-Host 'BarBell installer checks' -ForegroundColor Cyan
Write-Host "  installer: $Setup"
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) { throw 'Run this from an elevated PowerShell (Run as administrator): the installer installs for all users.' }
if (-not $Setup -or -not (Test-Path $Setup)) { throw "Installer not found. Build it first (python installer\build_installer.py) or pass -Setup." }
$existing = Get-ItemProperty $regKey -ErrorAction SilentlyContinue
if ($existing -and $existing.InstallLocation -and -not ($existing.InstallLocation -like "$Root*")) {
  throw "A real BarBell installation is registered at $($existing.InstallLocation). This test would interfere with it; uninstall it first."
}
if ((Test-Path 'C:\BarBell\data\barbell.db') -or (Test-Path 'C:\BarBell\barbell.db')) {
  Write-Host '  note: C:\BarBell has data. The installer will back it up while looking for an existing install (harmless).' -ForegroundColor Yellow
}
if (Test-Path $Root) { Remove-Item $Root -Recurse -Force }
New-Item -ItemType Directory $Root, $Backups | Out-Null
$build = [Environment]::OSVersion.Version.Build
Write-Host "  Windows build: $build  (Windows 11 is 22000 or higher)"

Write-Host ''
Write-Host '0. Environment' -ForegroundColor Cyan
Check 'Windows 11 (build 22000 or higher)' { Assert ($build -ge 22000) "this is build $build" }
Check 'Installer carries the 1.2.1 Beta label' {
  $v = (Get-Item $Setup).VersionInfo
  Assert ($v.ProductVersion -like '1.2.1*') "ProductVersion is '$($v.ProductVersion)'"
  Assert ((Split-Path $Setup -Leaf) -like '*1.2.1-Beta*') "file name is $(Split-Path $Setup -Leaf)"
}

# --------------------------------------------------------------------------- 1. install and start
Write-Host ''
Write-Host '1. Install and start the app' -ForegroundColor Cyan
$r1 = Run-Setup @("/DIR=`"$A`"", '/DATAMODE=blank') 'log1-install.txt'
Check 'silent install into a new folder succeeds (exit code 0)' { Assert ($r1.Code -eq 0) "exit code $($r1.Code); see $($r1.Log)" }
Check 'program and data folder are in place' {
  Assert (Test-Path "$A\BarBell.exe") 'BarBell.exe missing'
  Assert (Test-Path "$A\data") 'data folder missing'
  Assert (Test-Path "$A\unins000.exe") 'uninstaller missing'
}
Check 'a desktop icon and a Start menu icon were created' {
  Assert (Test-Path (Join-Path ([Environment]::GetFolderPath('CommonDesktopDirectory')) 'BarBell.lnk')) 'no desktop icon'
  Assert (Test-Path (Join-Path ([Environment]::GetFolderPath('CommonPrograms')) 'BarBell.lnk')) 'no Start menu icon'
}
Check 'the install is recorded in the registry' {
  Assert ((Get-ItemProperty $regKey).InstallLocation -eq $A) 'InstallLocation is wrong or missing'
  Assert ((Get-ItemProperty $regKey).Version -eq $expectedLabel) 'Version value is wrong'
}
Check 'no existing installation was reported on a first install' { Assert ($r1.Text -notmatch 'existing install at') 'it claimed to find one' }
Check 'the installed app starts, says 1.2.1 Beta, and uses the data folder' {
  $out = Join-Path $Root 'selftest.json'
  [void](Run-App "$A\BarBell.exe" @('--selftest', "`"$out`""))
  Assert (Test-Path $out) 'the app did not write its self-test file (did it start?)'
  $j = Get-Content $out -Raw | ConvertFrom-Json
  Assert ($j.title -eq "BarBell $expectedLabel") "title is '$($j.title)'"
  Assert ($j.frozen -eq $true) 'not running as the packaged program'
  Assert ($j.data_dir -eq "$A\data") "data_dir is '$($j.data_dir)'"
  Assert ($j.logos_loaded -eq $true) 'logos did not load from the package'
  Assert (($j.menu -join ',') -eq 'Home,Help') "menu is '$($j.menu -join ',')'"
}

# --------------------------------------------------------------------------- 2. upgrade keeps data
Write-Host ''
Write-Host '2. Upgrade keeps data' -ForegroundColor Cyan
[void](Tool @('make', "$A\data", '--serials', '10-14', '--jamaica-serials', '38-40', '--counter', '14', '--jamaica-counter', '40'))
[void](Tool @('make', $Good, '--serials', '10-14', '--jamaica-serials', '38-40', '--counter', '14', '--jamaica-counter', '40'))
$before = Tool @('check', "$A\data")
$r2 = Run-Setup @("/DIR=`"$A`"", '/DATAMODE=keep') 'log2-upgrade.txt'
Check 'upgrade over the existing install succeeds' { Assert ($r2.Code -eq 0) "exit code $($r2.Code); see $($r2.Log)" }
Check 'the existing installation was detected' { Assert ($r2.Text -match 'existing install at') 'not detected' }
Check 'the backup was made BEFORE any file was installed' {
  $iBackup = $r2.Text.IndexOf('existing install at')
  $iFiles = $r2.Text.IndexOf('-- File entry --')
  Assert ($iBackup -ge 0 -and $iFiles -ge 0) 'could not find the markers in the setup log'
  Assert ($iBackup -lt $iFiles) 'the first file was installed before the backup was logged'
}
$bk2 = Newest-PreInstallBackup
Check 'a verified backup set exists with the database and both SSCC counters' {
  Assert ($null -ne $bk2) 'no *_pre-install backup folder'
  $v = Tool @('verify-backup', $bk2.FullName)
  Assert ($v.ok -eq $true) "backup does not verify: $($v.error)"
  Assert ($v.ssccs -eq $before.ssccs) "backup holds $($v.ssccs) SSCCs, expected $($before.ssccs)"
  Assert ($v.counters.barbados -eq 14 -and $v.counters.jamaica -eq 40) 'backup counters are wrong'
}
Check 'the database and both counters are exactly as they were' {
  $after = Tool @('check', "$A\data")
  Assert ($after.sha256_db -eq $before.sha256_db) 'database changed'
  Assert ($after.sha256_barbados -eq $before.sha256_barbados) 'Barbados counter file changed'
  Assert ($after.sha256_jamaica -eq $before.sha256_jamaica) 'Jamaica counter file changed'
}

# --------------------------------------------------------------------------- 3. restore paths
Write-Host ''
Write-Host '3. Restore paths' -ForegroundColor Cyan
Tool @('corrupt', "$A\data\barbell.db") | Out-Null
$damaged = Tool @('check', "$A\data")
$r3a = Run-Setup @("/DIR=`"$A`"", '/DATAMODE=restore-file', "/DATASOURCE=`"$($bk2.FullName)`"") 'log3a-recover.txt'
Check 'damaged database: a raw copy is kept as evidence and no bad backup is passed off as good' {
  Assert ($r3a.Code -eq 0) "exit code $($r3a.Code)"
  $raw = Get-ChildItem $Backups -Directory | Where-Object { $_.Name -like 'barbell_rawcopy_*' } | Select-Object -Last 1
  Assert ($null -ne $raw) 'no raw copy was made'
  Assert ((Get-FileHash "$($raw.FullName)\barbell.db").Hash.ToLower() -eq $damaged.sha256_db) 'raw copy is not the damaged file'
}
Check 'restore from the installer backup: the data is back and healthy' {
  Assert ($r3a.Text -match 'DATA STEP OK') 'the data step did not report OK'
  $c = Tool @('check', "$A\data")
  Assert ($c.integrity -eq 'ok') "integrity is '$($c.integrity)'"
  Assert ($c.ssccs -eq $before.ssccs) "has $($c.ssccs) SSCCs, expected $($before.ssccs)"
  Assert ($c.counters.barbados -eq 14 -and $c.counters.jamaica -eq 40) 'counters are wrong'
}
Tool @('counter', "$A\data", 'sscc_state.json', '20') | Out-Null
$r3b = Run-Setup @("/DIR=`"$A`"", '/DATAMODE=restore-file', "/DATASOURCE=`"$($bk2.FullName)`"") 'log3b-neverlower.txt'
Check 'a counter that is already ahead is NOT moved back by a restore (backup says 14, live says 20)' {
  Assert ($r3b.Code -eq 0) "exit code $($r3b.Code)"
  Assert ((Tool @('check', "$A\data")).counters.barbados -eq 20) 'the counter went backwards'
}
$r3c = Run-Setup @("/DIR=`"$A`"", '/DATAMODE=blank') 'log3c-blank.txt'
Check 'start blank: the old database is kept aside, and the counters are left alone' {
  Assert ($r3c.Code -eq 0) "exit code $($r3c.Code)"
  Assert (-not (Test-Path "$A\data\barbell.db")) 'the old database is still in place'
  Assert ((Get-ChildItem "$A\data" -Filter 'barbell.replaced-*.db').Count -ge 1) 'the old database was not kept'
  $c = Tool @('check', "$A\data")
  Assert ($c.counters.barbados -eq 20 -and $c.counters.jamaica -eq 40) 'a counter was reset or changed'
}

# --------------------------------------------------------------------------- 4. uninstall keeps data
Write-Host ''
Write-Host '4. Uninstall keeps data' -ForegroundColor Cyan
$beforeUn = Tool @('check', "$A\data")
Uninstall $A
Check 'the program, shortcuts and registry entry are removed' {
  Assert (-not (Test-Path "$A\BarBell.exe")) 'BarBell.exe is still there'
  Assert (-not (Test-Path (Join-Path ([Environment]::GetFolderPath('CommonDesktopDirectory')) 'BarBell.lnk'))) 'desktop icon is still there'
  Assert (-not (Test-Path $regKey)) 'registry entry is still there'
}
Check 'the data folder, counters and backups are all still there' {
  $c = Tool @('check', "$A\data")
  Assert ($c.counters.barbados -eq 20 -and $c.counters.jamaica -eq 40) 'counters are gone or changed'
  Assert ($c.sha256_barbados -eq $beforeUn.sha256_barbados) 'Barbados counter file changed'
  Assert ((Get-ChildItem "$A\data" -Filter 'barbell.replaced-*.db').Count -ge 1) 'the kept database is gone'
  Assert ((Get-ChildItem $Backups -Directory).Count -ge 3) 'installer backups were removed'
}

# --------------------------------------------------------------------------- 3 (cont.) new machine
Write-Host ''
Write-Host '3b. A new machine: restore from a database file' -ForegroundColor Cyan
$r3d = Run-Setup @("/DIR=`"$B`"", '/DATAMODE=restore-file', "/DATASOURCE=`"$Good\barbell.db`"") 'log3d-newmachine.txt'
Check 'install on a "new machine" restoring from a bare database file' {
  Assert ($r3d.Code -eq 0) "exit code $($r3d.Code)"
  Assert ($r3d.Text -match 'DATA STEP OK') 'the data step did not report OK'
  $c = Tool @('check', "$B\data")
  Assert ($c.integrity -eq 'ok' -and $c.ssccs -eq $before.ssccs) "database has $($c.ssccs) SSCCs, integrity $($c.integrity)"
  Assert ($c.counters.barbados -eq 14 -and $c.counters.jamaica -eq 40) "counters rebuilt as $($c.counters.barbados)/$($c.counters.jamaica), expected 14/40"
}
Uninstall $B

# --------------------------------------------------------------------------- summary
if (-not $KeepFiles) { Remove-Item $Root -Recurse -Force -ErrorAction SilentlyContinue }
$failed = @($script:results | Where-Object { -not $_.Pass })
Write-Host ''
Write-Host ('=' * 70)
Write-Host ("{0} checks: {1} passed, {2} failed" -f $script:results.Count, ($script:results.Count - $failed.Count), $failed.Count)
if ($failed.Count -gt 0) {
  $failed | ForEach-Object { Write-Host "  FAILED: $($_.Name) -- $($_.Detail)" -ForegroundColor Red }
  if ($KeepFiles) { Write-Host "Logs and data kept in $Root" }
  exit 1
}
Write-Host 'ALL CHECKS PASSED' -ForegroundColor Green
exit 0
