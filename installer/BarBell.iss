; BarBell Windows installer - Inno Setup 6.
; Built by installer/build_installer.py, which passes the /D defines below.
;
; Wizard order:  Welcome -> Label Traxx ODBC check -> Install folder (default C:\BarBell)
;                -> [existing installation found? it is BACKED UP right here, before anything changes]
;                -> Your data (keep / restore from a file or backup / start blank)
;                -> Label Traxx login (only if there is no .env yet) -> Ready -> Install -> Finish
;
; Everything that can touch BarBell's data is done by barbell_install_helper.exe (src/installer_support.py,
; unit-tested); this script only asks the questions and calls it. Uninstalling removes the program and
; NEVER the data (C:\BarBell\data) or the installer backups.
;
; Unattended installs (used by the installer's own checks):
;   BarBell-Setup-1.2.1-Beta.exe /VERYSILENT /SUPPRESSMSGBOXES /DIR="C:\BarBell" /LOG="install.log"
;       [/DATAMODE=keep|blank|restore-backup|restore-file]  [/DATASOURCE=<db file or backup folder>]
;       [/LTUSER=<user> /LTPASSWORD=<password> /LTDSN=<dsn>]

; build_paths.inc is written by build_installer.py: the version and the (possibly space-containing) folder paths.
#ifexist "build_paths.inc"
  #include "build_paths.inc"
#endif
#ifndef AppVersion
  #define AppVersion "1.2.1"
#endif
#ifndef AppVersionLabel
  #define AppVersionLabel "1.2.1 Beta"
#endif
#ifndef AppDistDir
  #define AppDistDir "build\dist\BarBell"
#endif
#ifndef HelperExe
  #define HelperExe "build\dist\barbell_install_helper.exe"
#endif
#ifndef AssetsDir
  #define AssetsDir "..\assets"
#endif
#ifndef OutputDir
  #define OutputDir "Output"
#endif

#define AppRegKey "Software\Caribbean Label Crafts\BarBell"

[Setup]
AppId={{5B8D3E7A-1C94-4F62-A0D5-7E2B9C4F1A38}
AppName=BarBell
AppVersion={#AppVersionLabel}
AppVerName=BarBell {#AppVersionLabel}
AppPublisher=Caribbean Label Crafts Ltd.
VersionInfoVersion={#AppVersion}.0
VersionInfoDescription=BarBell {#AppVersionLabel} Setup
VersionInfoProductName=BarBell
VersionInfoProductVersion={#AppVersion}.0
DefaultDirName=C:\BarBell
DisableDirPage=no
UsePreviousAppDir=yes
DefaultGroupName=BarBell
DisableProgramGroupPage=yes
DisableReadyPage=no
PrivilegesRequired=admin
MinVersion=10.0.22000
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
AppMutex=BarBellAppMutex
CloseApplications=yes
WizardStyle=modern
SetupIconFile={#AssetsDir}\barbell_app_icon.ico
UninstallDisplayIcon={app}\BarBell.exe
UninstallDisplayName=BarBell {#AppVersionLabel}
OutputDir={#OutputDir}
OutputBaseFilename=BarBell-Setup-{#AppVersion}-Beta
Compression=lzma2
SolidCompression=yes

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Shortcuts:"

[Dirs]
; The data folder: operators must be able to write to it. Never removed on uninstall.
Name: "{app}\data"; Permissions: users-modify; Flags: uninsneveruninstall

[InstallDelete]
; Old program libraries only - never the data folder.
Type: filesandordirs; Name: "{app}\_internal"

[Files]
Source: "{#AppDistDir}\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "{#HelperExe}"; DestName: "barbell_install_helper.exe"; Flags: dontcopy

[Icons]
Name: "{autodesktop}\BarBell"; Filename: "{app}\BarBell.exe"; WorkingDir: "{app}\data"; IconFilename: "{app}\BarBell.exe"; Tasks: desktopicon
Name: "{autoprograms}\BarBell"; Filename: "{app}\BarBell.exe"; WorkingDir: "{app}\data"; IconFilename: "{app}\BarBell.exe"

[Registry]
Root: HKA; Subkey: "{#AppRegKey}"; ValueType: string; ValueName: "InstallLocation"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKA; Subkey: "{#AppRegKey}"; ValueType: string; ValueName: "Version"; ValueData: "{#AppVersionLabel}"

[Run]
Filename: "{app}\BarBell.exe"; Description: "Start BarBell"; WorkingDir: "{app}\data"; Flags: nowait postinstall skipifsilent

[Code]
const
  DefaultInstallDir = 'C:\BarBell';
  LtDsnBarbados = 'LT64';
  LtDsnJamaica = 'LCJ JAM';

var
  HelperReady: Boolean;
  OdbcPage: TOutputMsgMemoWizardPage;
  DataPage: TWizardPage;
  LtPage: TInputQueryWizardPage;
  RbKeep, RbFile, RbBlank: TNewRadioButton;
  LblKeep, LblBlank, LblSummary: TNewStaticText;
  EdSource: TNewEdit;
  BtnDb, BtnFolder: TNewButton;

  OdbcLt64, OdbcLcj: Boolean;

  DetectDone: Boolean;
  DetectedFor: String;
  ExistingFound, ExistingHasData, BackupOk: Boolean;
  ExistingRoot, ExistingDataDir, ExistingLayout: String;
  VerifiedBackup, RawCopy, BackupMessage: String;
  DataPageDefaultsSet: Boolean;
  SourceOk: Boolean;
  SourceKind, SourceSummary: String;

function BackupRoot: String;
begin
  { /BACKUPROOT=<folder> is for the installer's own checks; normally backups go to ProgramData }
  Result := ExpandConstant('{param:BACKUPROOT|}');
  if Result = '' then
    Result := ExpandConstant('{commonappdata}') + '\BarBell\installer-backups';
end;

function TargetDataDir: String;
begin
  Result := RemoveBackslashUnlessRoot(WizardDirValue) + '\data';
end;

function SameFolder(const A, B: String): Boolean;
begin
  Result := CompareText(RemoveBackslashUnlessRoot(A), RemoveBackslashUnlessRoot(B)) = 0;
end;

procedure EnsureHelper;
begin
  if not HelperReady then
  begin
    ExtractTemporaryFile('barbell_install_helper.exe');
    HelperReady := True;
  end;
end;

{ Runs the helper; its answer is the INI file OutFile + '.ini'. True if it exited 0 (ok). }
function RunHelper(const Params, OutFile: String): Boolean;
var
  ResultCode: Integer;
begin
  EnsureHelper;
  DeleteFile(OutFile);
  DeleteFile(OutFile + '.ini');
  Result := Exec(ExpandConstant('{tmp}\barbell_install_helper.exe'), Params + ' --out ' + AddQuotes(OutFile),
    '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
  Log('helper ' + Params + ' -> exit ' + IntToStr(ResultCode));
end;

function Answer(const OutFile, Key, Default: String): String;
begin
  Result := GetIniString('result', Key, Default, OutFile + '.ini');
end;

{ --- Label Traxx ODBC ---------------------------------------------------------------------- }

function OdbcDsnPresent(const Name: String): Boolean;
begin
  { HKLM is the 64-bit view in a 64-bit install: where 64-bit System DSNs live. }
  Result := RegValueExists(HKLM, 'SOFTWARE\ODBC\ODBC.INI\ODBC Data Sources', Name);
end;

function OdbcStatusText: String;
var
  Lt64, Lcj: String;
begin
  OdbcLt64 := OdbcDsnPresent(LtDsnBarbados);
  OdbcLcj := OdbcDsnPresent(LtDsnJamaica);
  if OdbcLt64 then Lt64 := 'FOUND' else Lt64 := 'not found';
  if OdbcLcj then Lcj := 'FOUND' else Lcj := 'not found';
  Result :=
    'BarBell reads Label Traxx through ODBC. Before BarBell is used on this PC, the Label Traxx ODBC driver ' +
    'must be installed and a 64-bit System DSN set up for this PC''s plant (Windows: "ODBC Data Sources (64-bit)").' + #13#10#13#10 +
    'Found on this PC right now:' + #13#10 +
    '    ' + LtDsnBarbados + '  (Barbados):  ' + Lt64 + #13#10 +
    '    ' + LtDsnJamaica + '  (Jamaica):  ' + Lcj + #13#10#13#10 +
    'Only the plant this PC is used for is needed. If it says "not found", install the driver and create the ' +
    'DSN first - you can do that before or after installing BarBell, but BarBell cannot read Label Traxx until it is done.';
end;

{ --- existing installation: detect + back up, BEFORE anything is changed ---------------------- }

procedure DetectAndBackup(const TargetDir: String);
var
  Ans, Params, Previous: String;
begin
  if DetectDone and SameFolder(DetectedFor, TargetDir) then Exit;
  DetectDone := True;
  DetectedFor := TargetDir;
  ExistingFound := False; ExistingHasData := False; BackupOk := True;
  ExistingRoot := ''; ExistingDataDir := ''; ExistingLayout := '';
  VerifiedBackup := ''; RawCopy := ''; BackupMessage := '';
  DataPageDefaultsSet := False;

  Params := 'detect --candidate ' + AddQuotes(RemoveBackslashUnlessRoot(TargetDir));
  if RegQueryStringValue(HKA, '{#AppRegKey}', 'InstallLocation', Previous) and (Previous <> '') then
    Params := Params + ' --candidate ' + AddQuotes(Previous);
  Params := Params + ' --candidate ' + AddQuotes(DefaultInstallDir);

  Ans := ExpandConstant('{tmp}\detect.json');
  if RunHelper(Params, Ans) and (Answer(Ans, 'found', 'false') = 'true') then
  begin
    ExistingFound := True;
    ExistingRoot := Answer(Ans, 'install.root', '');
    ExistingDataDir := Answer(Ans, 'install.data_dir', '');
    ExistingLayout := Answer(Ans, 'install.layout', '');
    ExistingHasData := Answer(Ans, 'has_data', 'false') = 'true';
    if ExistingHasData then
    begin
      Ans := ExpandConstant('{tmp}\backup.json');
      BackupOk := RunHelper('backup --existing-root ' + AddQuotes(ExistingRoot) + ' --backup-root ' + AddQuotes(BackupRoot), Ans);
      VerifiedBackup := Answer(Ans, 'verified_backup', '');
      RawCopy := Answer(Ans, 'raw_copy', '');
      BackupMessage := Answer(Ans, 'message', '');
      Log('existing install at ' + ExistingRoot + '; backup ok=' + IntToStr(Ord(BackupOk)) + ' verified=' + VerifiedBackup + ' raw=' + RawCopy);
    end;
  end;
end;

{ --- the data choice ---------------------------------------------------------------------------- }

procedure InspectSource(const Source: String);
var
  Ans: String;
begin
  SourceOk := False; SourceKind := ''; SourceSummary := '';
  if Source = '' then Exit;
  Ans := ExpandConstant('{tmp}\inspect.json');
  if RunHelper('inspect --source ' + AddQuotes(Source), Ans) then
  begin
    SourceOk := True;
    SourceKind := Answer(Ans, 'kind', '');
    if SourceKind = 'backup' then
      SourceSummary := 'A BarBell backup made ' + Answer(Ans, 'created_at', '?') + ' (BarBell ' + Answer(Ans, 'app_version', '?') +
        '), holding ' + Answer(Ans, 'distinct_ssccs', '0') + ' carton/pallet SSCCs.'
    else
      SourceSummary := 'A BarBell database with ' + Answer(Ans, 'label_rows', '0') + ' label rows (' +
        Answer(Ans, 'distinct_ssccs', '0') + ' SSCCs), newest ' + Answer(Ans, 'newest_label_at', '?') + '.';
  end
  else
    SourceSummary := 'Cannot use this: ' + Answer(Ans, 'error', 'unknown problem');
end;

procedure SourceChosen(const Path: String);
begin
  EdSource.Text := Path;
  InspectSource(Path);
  LblSummary.Caption := SourceSummary;
  RbFile.Checked := True;
end;

procedure BrowseDbClick(Sender: TObject);
var
  FileName: String;
begin
  FileName := '';
  if GetOpenFileName('Choose the BarBell database to restore', FileName, '', 'BarBell database (*.db)|*.db|All files (*.*)|*.*', 'db') then
    SourceChosen(FileName);
end;

procedure BrowseFolderClick(Sender: TObject);
var
  Dir: String;
begin
  Dir := '';
  if BrowseForFolder('Choose a BarBell backup folder (the one that contains manifest.json)', Dir, False) then
    SourceChosen(Dir);
end;

function ChosenMode: String;
var
  Param: String;
begin
  Param := ExpandConstant('{param:DATAMODE|}');
  if WizardSilent and (Param <> '') then
  begin
    if Param = 'restore-file' then
    begin
      InspectSource(ExpandConstant('{param:DATASOURCE|}'));
      if SourceKind = 'backup' then Result := 'restore-backup' else Result := 'restore-db';
    end
    else if (Param = 'keep') and not SameFolder(ExistingDataDir, TargetDataDir) and (VerifiedBackup <> '') then
      Result := 'restore-backup'
    else
      Result := Param;
    Exit;
  end;
  if WizardSilent or (RbKeep = nil) then
  begin
    { unattended with no instruction: keep what is there, otherwise start blank }
    if ExistingHasData and (VerifiedBackup <> '') then
    begin
      if SameFolder(ExistingDataDir, TargetDataDir) then Result := 'keep' else Result := 'restore-backup';
    end
    else Result := 'blank';
    Exit;
  end;
  if RbBlank.Checked then Result := 'blank'
  else if RbKeep.Checked then
  begin
    if SameFolder(ExistingDataDir, TargetDataDir) then Result := 'keep' else Result := 'restore-backup';
  end
  else if SourceKind = 'backup' then Result := 'restore-backup'
  else Result := 'restore-db';
end;

function ChosenSource: String;
var
  Param: String;
begin
  Result := '';
  Param := ExpandConstant('{param:DATASOURCE|}');
  if WizardSilent and (Param <> '') then begin Result := Param; Exit; end;
  if (ChosenMode = 'keep') or (ChosenMode = 'blank') then Exit;
  if (not WizardSilent) and (RbFile <> nil) and RbFile.Checked then Result := EdSource.Text
  else Result := VerifiedBackup;
end;

function ChosenModeText: String;
begin
  if ChosenMode = 'keep' then Result := 'Keep the existing data as it is'
  else if ChosenMode = 'restore-backup' then Result := 'Restore the database and SSCC counters from a backup: ' + ChosenSource
  else if ChosenMode = 'restore-db' then Result := 'Restore the database from the file: ' + ChosenSource
  else Result := 'Start with a blank database (SSCC counters are not reset)';
end;

procedure PrepareDataPage;
begin
  if DataPageDefaultsSet then Exit;
  DataPageDefaultsSet := True;

  if ExistingFound and ExistingHasData and (VerifiedBackup <> '') then
  begin
    RbKeep.Enabled := True;
    LblKeep.Caption := 'An existing installation was found at ' + ExistingRoot + '. The installer has backed up its database and SSCC ' +
      'counters to:' + #13#10 + VerifiedBackup;
    RbKeep.Checked := True;
  end
  else
  begin
    RbKeep.Enabled := False;
    if ExistingFound and ExistingHasData then
      LblKeep.Caption := 'An existing installation was found, but its database could not be verified (it may be damaged), so there is ' +
        'no backup to restore from. A raw copy of its files was kept at:' + #13#10 + RawCopy + #13#10 + 'Choose a good database file or backup below.'
    else
      LblKeep.Caption := 'No existing BarBell data was found on this PC, so there is nothing to keep.';
    if ExistingFound and ExistingHasData then RbFile.Checked := True else RbBlank.Checked := True;
  end;
  LblSummary.Caption := '';
  EdSource.Text := '';
  SourceOk := False; SourceKind := '';
end;

function ValidateDataChoice: Boolean;
begin
  Result := True;
  if RbFile.Checked then
  begin
    if EdSource.Text = '' then
    begin
      MsgBox('Choose a database file or a backup folder to restore from, or pick one of the other options.', mbError, MB_OK);
      Result := False;
    end
    else
    begin
      InspectSource(EdSource.Text);
      LblSummary.Caption := SourceSummary;
      if not SourceOk then
      begin
        MsgBox('That cannot be restored.' + #13#10#13#10 + SourceSummary, mbError, MB_OK);
        Result := False;
      end;
    end;
  end
  else if RbBlank.Checked and ExistingHasData then
    Result := MsgBox('Start with a BLANK database?' + #13#10#13#10 +
      'The existing database has already been backed up and is kept alongside (it is never deleted), and the SSCC counters ' +
      'are left as they are. The label history will be empty until you restore it.', mbConfirmation, MB_YESNO) = IDYES;
end;

{ --- wizard pages ------------------------------------------------------------------------------------ }

procedure InitializeWizard;
var
  Y: Integer;
begin
  EnsureHelper;

  OdbcPage := CreateOutputMsgMemoPage(wpWelcome, 'Label Traxx ODBC', 'Install and configure this first',
    'Please read, then click Next.', OdbcStatusText);

  DataPage := CreateCustomPage(wpSelectDir, 'Your data', 'Choose the database BarBell will use on this PC.');

  RbKeep := TNewRadioButton.Create(DataPage);
  RbKeep.Parent := DataPage.Surface;
  RbKeep.Left := 0; RbKeep.Top := 0; RbKeep.Width := DataPage.SurfaceWidth;
  RbKeep.Caption := 'Keep / restore my existing data (the backup the installer just made)';
  LblKeep := TNewStaticText.Create(DataPage);
  LblKeep.Parent := DataPage.Surface;
  LblKeep.Left := ScaleX(20); LblKeep.Top := RbKeep.Top + RbKeep.Height + ScaleY(2);
  LblKeep.Width := DataPage.SurfaceWidth - ScaleX(20);
  LblKeep.AutoSize := False; LblKeep.WordWrap := True; LblKeep.Height := ScaleY(48);

  Y := LblKeep.Top + LblKeep.Height + ScaleY(8);
  RbFile := TNewRadioButton.Create(DataPage);
  RbFile.Parent := DataPage.Surface;
  RbFile.Left := 0; RbFile.Top := Y; RbFile.Width := DataPage.SurfaceWidth;
  RbFile.Caption := 'Restore from a database file or a backup folder I choose';
  EdSource := TNewEdit.Create(DataPage);
  EdSource.Parent := DataPage.Surface;
  EdSource.Left := ScaleX(20); EdSource.Top := RbFile.Top + RbFile.Height + ScaleY(2);
  EdSource.Width := DataPage.SurfaceWidth - ScaleX(20); EdSource.ReadOnly := True;
  BtnDb := TNewButton.Create(DataPage);
  BtnDb.Parent := DataPage.Surface;
  BtnDb.Left := ScaleX(20); BtnDb.Top := EdSource.Top + EdSource.Height + ScaleY(4);
  BtnDb.Width := ScaleX(150); BtnDb.Height := ScaleY(23);
  BtnDb.Caption := 'Choose database file...'; BtnDb.OnClick := @BrowseDbClick;
  BtnFolder := TNewButton.Create(DataPage);
  BtnFolder.Parent := DataPage.Surface;
  BtnFolder.Left := BtnDb.Left + BtnDb.Width + ScaleX(8); BtnFolder.Top := BtnDb.Top;
  BtnFolder.Width := ScaleX(150); BtnFolder.Height := ScaleY(23);
  BtnFolder.Caption := 'Choose backup folder...'; BtnFolder.OnClick := @BrowseFolderClick;
  LblSummary := TNewStaticText.Create(DataPage);
  LblSummary.Parent := DataPage.Surface;
  LblSummary.Left := ScaleX(20); LblSummary.Top := BtnDb.Top + BtnDb.Height + ScaleY(6);
  LblSummary.Width := DataPage.SurfaceWidth - ScaleX(20);
  LblSummary.AutoSize := False; LblSummary.WordWrap := True; LblSummary.Height := ScaleY(34);

  Y := LblSummary.Top + LblSummary.Height + ScaleY(8);
  RbBlank := TNewRadioButton.Create(DataPage);
  RbBlank.Parent := DataPage.Surface;
  RbBlank.Left := 0; RbBlank.Top := Y; RbBlank.Width := DataPage.SurfaceWidth;
  RbBlank.Caption := 'Start with a blank database';
  LblBlank := TNewStaticText.Create(DataPage);
  LblBlank.Parent := DataPage.Surface;
  LblBlank.Left := ScaleX(20); LblBlank.Top := RbBlank.Top + RbBlank.Height + ScaleY(2);
  LblBlank.Width := DataPage.SurfaceWidth - ScaleX(20);
  LblBlank.AutoSize := False; LblBlank.WordWrap := True; LblBlank.Height := ScaleY(34);
  LblBlank.Caption := 'Usual for a first-time install. The label history starts empty. SSCC counters are never reset, ' +
    'so a number that was issued is never issued again.';

  LtPage := CreateInputQueryPage(DataPage.ID, 'Label Traxx login',
    'BarBell signs in to Label Traxx with this user.',
    'Enter the Label Traxx user and password. You can leave them empty and fill in the .env file in the data folder later.');
  LtPage.Add('Label Traxx user:', False);
  LtPage.Add('Label Traxx password:', True);
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  if PageID = LtPage.ID then
    Result := FileExists(TargetDataDir + '\.env') or
      ((ExistingDataDir <> '') and FileExists(ExistingDataDir + '\.env'));
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = DataPage.ID then PrepareDataPage;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if CurPageID = OdbcPage.ID then
  begin
    if (not OdbcLt64) and (not OdbcLcj) then
      Result := MsgBox('No Label Traxx ODBC data source (' + LtDsnBarbados + ' or ' + LtDsnJamaica + ') was found on this PC.' + #13#10#13#10 +
        'Install the Label Traxx ODBC driver and set up the DSN for this PC''s plant. You can do that after installing BarBell, but ' +
        'BarBell cannot read Label Traxx until it is done.' + #13#10#13#10 + 'Continue installing anyway?', mbConfirmation, MB_YESNO) = IDYES;
  end
  else if CurPageID = wpSelectDir then
  begin
    DetectAndBackup(WizardDirValue);
    if ExistingFound and ExistingHasData then
    begin
      if not BackupOk then
      begin
        MsgBox('An existing BarBell installation was found at ' + ExistingRoot + ', but its data could not be backed up:' + #13#10#13#10 +
          BackupMessage + #13#10#13#10 + 'Nothing has been changed. Fix the problem (is the disk full or the folder locked?) and try again.', mbError, MB_OK);
        Result := False;
      end
      else if VerifiedBackup <> '' then
        MsgBox('An existing BarBell installation was found at ' + ExistingRoot + '.' + #13#10#13#10 +
          'Its database and SSCC counters have been backed up (before anything is changed) to:' + #13#10 + VerifiedBackup, mbInformation, MB_OK)
      else
        MsgBox('An existing BarBell installation was found at ' + ExistingRoot + '.' + #13#10#13#10 + BackupMessage + #13#10#13#10 +
          'On the next page, choose a good database file or backup to restore from, or start blank.', mbInformation, MB_OK);
    end;
  end
  else if CurPageID = DataPage.ID then
    Result := ValidateDataChoice;
end;

function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo, MemoTypeInfo, MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
begin
  Result := MemoDirInfo + NewLine + NewLine + 'Data:' + NewLine + Space + ChosenModeText;
  if ExistingFound and (VerifiedBackup <> '') then
    Result := Result + NewLine + Space + 'Backup of the existing data: ' + VerifiedBackup;
  if MemoTasksInfo <> '' then Result := Result + NewLine + NewLine + MemoTasksInfo;
end;

{ --- doing it ----------------------------------------------------------------------------------------- }

procedure WriteLtLogin;
var
  EnvFile, User, Password, Dsn, Elsewhere: String;
begin
  EnvFile := TargetDataDir + '\.env';
  if FileExists(EnvFile) then Exit;

  { an older manual copy kept its .env beside the program: carry it over }
  Elsewhere := ExistingDataDir + '\.env';
  if (ExistingDataDir <> '') and FileExists(Elsewhere) then
  begin
    CopyFile(Elsewhere, EnvFile, True);
    Log('copied .env from ' + Elsewhere);
    Exit;
  end;

  if WizardSilent then
  begin
    User := ExpandConstant('{param:LTUSER|}');
    Password := ExpandConstant('{param:LTPASSWORD|}');
  end
  else
  begin
    User := LtPage.Values[0];
    Password := LtPage.Values[1];
  end;
  Dsn := ExpandConstant('{param:LTDSN|' + LtDsnBarbados + '}');

  if (User = '') and (Password = '') then
    SaveStringToFile(TargetDataDir + '\.env.example',
      'LT_DSN=' + LtDsnBarbados + #13#10 + 'LT_USER=' + #13#10 + 'LT_PASSWORD=' + #13#10, False)
  else
    SaveStringToFile(EnvFile,
      'LT_DSN=' + Dsn + #13#10 + 'LT_USER=' + User + #13#10 + 'LT_PASSWORD=' + Password + #13#10, False);
end;

procedure ApplyData;
var
  Ans, Mode, Source, Params: String;
begin
  Mode := ChosenMode;
  Source := ChosenSource;
  Params := 'apply --data-dir ' + AddQuotes(TargetDataDir) + ' --mode ' + Mode + ' --backup-root ' + AddQuotes(BackupRoot);
  if Source <> '' then Params := Params + ' --source ' + AddQuotes(Source);
  Ans := ExpandConstant('{tmp}\apply.json');
  if RunHelper(Params, Ans) then
    Log('DATA STEP OK: ' + Mode + ' - ' + Answer(Ans, 'message', ''))
  else
  begin
    Log('DATA STEP FAILED: ' + Mode + ' - ' + Answer(Ans, 'error', 'unknown error'));
    MsgBox('BarBell was installed, but the data step did not finish:' + #13#10#13#10 + Answer(Ans, 'error', 'unknown error') + #13#10#13#10 +
      'Your previous data has not been lost' +
      '. Backups are in ' + BackupRoot + '. Run this installer again and choose another option.', mbError, MB_OK);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
    { silent installs never visit the directory page: make sure the existing data is backed up before ANY file changes }
    DetectAndBackup(WizardDirValue);
  if CurStep = ssPostInstall then
  begin
    ApplyData;
    WriteLtLogin;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if (CurUninstallStep = usPostUninstall) and (not UninstallSilent) then
    MsgBox('BarBell has been removed.' + #13#10#13#10 + 'Your data (database, SSCC counters, settings) was NOT removed. It is still in ' +
      ExpandConstant('{app}') + '\data, and the installer backups are in ' + ExpandConstant('{commonappdata}') + '\BarBell.', mbInformation, MB_OK);
end;
