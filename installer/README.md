# BarBell Windows installer (package version 1.2.0 Beta)

One file, `BarBell-Setup-1.2.0-Beta.exe`, installs BarBell on Windows 11. The development copy stays on
1.1.x; the production package is **1.2.0 Beta** (set in `build_installer.py`, only inside the build).

## Building it

```
pip install pyinstaller            # once
winget install JRSoftware.InnoSetup  # once (Inno Setup 6)
python installer\build_installer.py
```

Output: **`installer\Output\BarBell-Setup-1.2.0-Beta.exe`** in this project folder (git-ignored). The
intermediate build files are kept outside the project, in `%LOCALAPPDATA%\BarBellBuild`. (If the build is run from
inside the Claude desktop app, Windows redirects anything under AppData into that app's private storage where File
Explorer can't see it - which is why the finished installer is copied into the project.) `--skip-compile` builds just
the two `.exe` files.

## What the installer does

1. **Label Traxx ODBC** - a first page lists whether the `LT64` / `LCJ JAM` System DSNs exist on the PC and
   says the driver must be installed and configured; it asks before continuing if neither is found.
2. **Install folder** - always asks; offers `C:\BarBell`.
3. **Existing installation?** - looks in the chosen folder, the folder a previous install recorded, and
   `C:\BarBell`. If one is found, its database, **both SSCC counters**, settings and audit log are backed up
   *right then, before anything is changed* to `C:\ProgramData\BarBell\installer-backups` (never removed by
   uninstalling). A damaged database can't be verified, so a raw copy of its files is kept instead and the
   wizard says the backup is not restorable.
4. **Your data** - keep / restore from the backup just made, restore from a database file or backup folder you
   choose (checked for damage first), or start blank.
5. **Label Traxx login** - user and password for `.env` (skipped if one already exists; may be left blank).
6. Installs to `<folder>`, data in `<folder>\data`, desktop and Start menu icons, then applies the data choice.

The rule behind it: **an SSCC counter never moves backwards.** Restores raise each counter to at least the
highest serial found in the restored database; "start blank" leaves the counters exactly as they are.

Uninstalling removes the program only. `<folder>\data` and the installer backups are never touched.

## Unattended install (used by the checks)

```
BarBell-Setup-1.2.0-Beta.exe /VERYSILENT /SUPPRESSMSGBOXES /DIR="C:\BarBell" /LOG="install.log"
    [/DATAMODE=keep|blank|restore-backup|restore-file] [/DATASOURCE=<db file or backup folder>]
    [/LTUSER=<user> /LTPASSWORD=<password> /LTDSN=<dsn>] [/BACKUPROOT=<folder>]
```

## Checking it

`installer\test_installer.ps1` runs the whole installer unattended and prints PASS/FAIL: install and start,
upgrade keeps data (and the backup happens before any file changes), the restore paths, uninstall keeps data.
Run it from an **elevated** PowerShell on a Windows 11 PC. The logic that touches data is also covered by
`tests/test_installer_support.py`, run with the rest of the suite (`python -m pytest`).

## Security software and code signing

The installer and `BarBell.exe` are **unsigned**. Endpoint protection such as CylancePROTECT (installed on the
PC this was built on) blocks unsigned programs it hasn't seen ("Access is denied"), and Windows SmartScreen
shows a warning. Before rolling this out, either **sign** the installer and `BarBell.exe` with a code-signing
certificate (add `SignTool=` to `BarBell.iss` and sign the PyInstaller output), or have IT allow-list the
files / the signing certificate.
