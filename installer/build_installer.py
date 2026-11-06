"""
Builds the BarBell Windows installer.

    python installer/build_installer.py                 # builds BarBell-Setup-1.2.1-Beta.exe
    python installer/build_installer.py --skip-compile  # only the .exe files, no installer

What it does:
  1. Stages a clean copy of just what ships (the app, setup, src/, assets/, the
     installer helper) into installer/build/stage - never tests, databases,
     settings.json, .env or counters.
  2. Sets the PACKAGE's version in that staged copy only. Your development
     copy keeps its own 1.1.x number (src/version.py is untouched); the
     production package is "1.2.1 Beta" (RELEASE_* below).
  3. Builds BarBell.exe (the app, no console window) and barbell_install_helper.exe
     (what the installer wizard runs to detect / back up / restore data) with PyInstaller.
  4. Compiles installer/BarBell.iss with Inno Setup into
     installer/Output/BarBell-Setup-<version>.exe.

Needs: PyInstaller (pip install pyinstaller) and Inno Setup 6 (ISCC.exe).
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALLER_DIR = ROOT / "installer"
# Build output is large and disposable, so it lives OUTSIDE the project (and OneDrive):
# %LOCALAPPDATA%\\BarBellBuild, or BARBELL_BUILD_DIR if set.
BUILD = Path(os.environ.get("BARBELL_BUILD_DIR") or (Path(os.environ.get("LOCALAPPDATA", str(ROOT))) / "BarBellBuild"))
STAGE = BUILD / "stage"
OUTPUT = BUILD / "Output"  # where the compiler writes it (next to the other build output)
# Where the FINISHED installer is put for people: a real, visible folder in the project (git-ignored).
# Not the build folder: when this runs inside the Claude desktop app, anything written under AppData is
# silently redirected into that app's private storage, where File Explorer can't see it.
FINAL_OUTPUT = INSTALLER_DIR / "Output"

# The production package's version. The dev copy stays on 1.1.x.
RELEASE_MAJOR, RELEASE_MINOR, RELEASE_PATCH, RELEASE_BETA = 1, 2, 1, True

STAGED_FILES = ["barbell_gui.py", "setup_gui.py"]
STAGED_DIRS = ["src", "assets"]


def release_version() -> str:
    return f"{RELEASE_MAJOR}.{RELEASE_MINOR}.{RELEASE_PATCH}"


def release_label() -> str:
    return release_version() + (" Beta" if RELEASE_BETA else "")


def find_iscc() -> Path | None:
    candidates = [
        os.environ.get("ISCC"),
        shutil.which("iscc"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("ProgramFiles(x86)", "")) / "Inno Setup 6" / "ISCC.exe",
        Path(os.environ.get("ProgramFiles", "")) / "Inno Setup 6" / "ISCC.exe",
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return Path(c)
    return None


def _clear_folder(path: Path) -> bool:
    """Deletes a folder, retrying: security software that scans freshly written
    files can hold a handle for a moment and make Windows refuse the delete."""
    import stat
    import time

    def make_writable_and_retry(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    for _ in range(6):
        if not path.exists():
            return True
        try:
            shutil.rmtree(path, onexc=make_writable_and_retry)
            return True
        except OSError:
            time.sleep(1.0)
    return not path.exists()


def stage_sources() -> None:
    """A clean copy of exactly what ships."""
    global STAGE
    if not _clear_folder(STAGE):
        # something is still holding the old one: stage into a fresh, uniquely named folder instead
        STAGE = BUILD / f"stage-{os.getpid()}"
        print(f"(old stage folder is locked; staging in {STAGE.name})")
        _clear_folder(STAGE)
    STAGE.mkdir(parents=True)
    for name in STAGED_FILES:
        shutil.copy2(ROOT / name, STAGE / name)
    for name in STAGED_DIRS:
        shutil.copytree(ROOT / name, STAGE / name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (STAGE / "installer").mkdir()
    shutil.copy2(INSTALLER_DIR / "helper_main.py", STAGE / "installer" / "helper_main.py")
    (STAGE / "installer" / "__init__.py").write_text("", encoding="utf-8")
    # Never ship anything that is one machine's data.
    forbidden = [p for p in STAGE.rglob("*") if p.name in (".env", "settings.json", "barbell.db", "sscc_state.json")]
    assert not forbidden, f"staged data files that must never ship: {forbidden}"


def set_package_version() -> None:
    """Rewrites the version in the STAGED src/version.py only."""
    path = STAGE / "src" / "version.py"
    text = path.read_text(encoding="utf-8")
    replacements = {
        r"^MAJOR = \d+$": f"MAJOR = {RELEASE_MAJOR}",
        r"^MINOR = \d+$": f"MINOR = {RELEASE_MINOR}",
        r"^PATCH = \d+$": f"PATCH = {RELEASE_PATCH}",
        r"^BETA = (True|False)$": f"BETA = {RELEASE_BETA}",
        r'^BUILD_DATE = ".*?"': f'BUILD_DATE = "{datetime.date.today().isoformat()}"',
    }
    for pattern, new in replacements.items():
        text, n = re.subn(pattern, new, text, count=1, flags=re.MULTILINE)
        assert n == 1, f"could not set {pattern!r} in staged version.py"
    path.write_text(text, encoding="utf-8")


def run(cmd, cwd=None) -> None:
    print("\n>>", " ".join(str(c) for c in cmd), flush=True)
    subprocess.run([str(c) for c in cmd], cwd=cwd, check=True)


def build_exes() -> None:
    dist, work, spec = BUILD / "dist", BUILD / "work", BUILD / "spec"
    common = ["--noconfirm", "--clean", "--distpath", dist, "--workpath", work, "--specpath", spec]
    icon = STAGE / "assets" / "barbell_app_icon.ico"

    run([sys.executable, "-m", "PyInstaller", *common, "--onedir", "--windowed", "--name", "BarBell",
         "--icon", icon, "--add-data", f"{STAGE / 'assets'};assets", "--collect-data", "barcode",
         "--paths", STAGE, STAGE / "barbell_gui.py"], cwd=STAGE)

    run([sys.executable, "-m", "PyInstaller", *common, "--onefile", "--console", "--name", "barbell_install_helper",
         "--icon", icon, "--paths", STAGE, STAGE / "installer" / "helper_main.py"], cwd=STAGE)


def compile_installer() -> Path:
    iscc = find_iscc()
    if iscc is None:
        sys.exit("Inno Setup 6 (ISCC.exe) was not found. Install it (winget install JRSoftware.InnoSetup) "
                 "or set the ISCC environment variable.")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    # Paths go in an include file: ISCC's command line can't take /D values containing spaces
    # (this project's own folder has some).
    (INSTALLER_DIR / "build_paths.inc").write_text(
        f'#define AppVersion "{release_version()}"\n'
        f'#define AppVersionLabel "{release_label()}"\n'
        f'#define AppDistDir "{BUILD / "dist" / "BarBell"}"\n'
        f'#define HelperExe "{BUILD / "dist" / "barbell_install_helper.exe"}"\n'
        f'#define AssetsDir "{STAGE / "assets"}"\n'
        f'#define OutputDir "{OUTPUT}"\n',
        encoding="utf-8",
    )
    run([iscc, INSTALLER_DIR / "BarBell.iss"])
    built = OUTPUT / f"BarBell-Setup-{release_version()}{'-Beta' if RELEASE_BETA else ''}.exe"
    assert built.is_file(), f"expected {built}"
    return built


def publish(built: Path) -> Path:
    """Copies the finished installer to installer/Output so it can be found and handed out."""
    FINAL_OUTPUT.mkdir(parents=True, exist_ok=True)
    target = FINAL_OUTPUT / built.name
    shutil.copy2(built, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-compile", action="store_true", help="build the .exe files only")
    args = parser.parse_args()

    print(f"Building BarBell {release_label()} (development copy is untouched)")
    stage_sources()
    set_package_version()
    build_exes()
    if args.skip_compile:
        print("\nBuilt the .exe files in", BUILD / "dist")
        return 0
    built = compile_installer()
    final = publish(built)
    print(f"\nInstaller ready: {final}  ({final.stat().st_size / 1_000_000:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
