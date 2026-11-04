"""
Everything about the installer PACKAGE that can be checked without running an
unsigned program: where the app looks for its files when installed, how it
starts Setup when installed, what the build stages and which version it stamps,
and - as a guard - that the installer script still says what the requirements
say. (Actually running the installer is installer/test_installer.ps1.)
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from installer import build_installer as build
from src import paths
from src.version import version_string

ROOT = Path(__file__).resolve().parent.parent
ISS = (ROOT / "installer" / "BarBell.iss").read_text(encoding="utf-8")


# --- where files live --------------------------------------------------------------------------

def test_from_source_the_data_stays_in_the_project_folder_as_always(monkeypatch):
    monkeypatch.delenv("BARBELL_DATA_DIR", raising=False)
    monkeypatch.setattr(sys, "frozen", False, raising=False)
    assert paths.is_frozen() is False
    assert paths.data_dir() == paths.install_dir() == ROOT
    assert paths.settings_file() == ROOT / "settings.json"


def test_installed_the_data_lives_in_a_data_folder_next_to_the_exe(monkeypatch, tmp_path):
    monkeypatch.delenv("BARBELL_DATA_DIR", raising=False)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(tmp_path / "BarBell" / "BarBell.exe"))
    assert paths.is_frozen() is True
    assert paths.install_dir() == tmp_path / "BarBell"
    assert paths.data_dir() == tmp_path / "BarBell" / "data"
    assert paths.settings_file() == tmp_path / "BarBell" / "data" / "settings.json"
    assert paths.env_file() == tmp_path / "BarBell" / "data" / ".env"


def test_the_data_folder_can_be_overridden(monkeypatch, tmp_path):
    monkeypatch.setenv("BARBELL_DATA_DIR", str(tmp_path / "elsewhere"))
    assert paths.data_dir() == tmp_path / "elsewhere"


def test_entering_the_data_folder_creates_it_and_moves_the_working_directory(monkeypatch, tmp_path):
    start = os.getcwd()
    monkeypatch.setenv("BARBELL_DATA_DIR", str(tmp_path / "data"))
    try:
        paths.enter_data_dir()
        assert (tmp_path / "data").is_dir()
        assert Path(os.getcwd()) == tmp_path / "data"
    finally:
        os.chdir(start)


def test_from_source_entering_the_data_folder_changes_nothing(monkeypatch):
    monkeypatch.delenv("BARBELL_DATA_DIR", raising=False)
    monkeypatch.setattr(sys, "frozen", False, raising=False)
    start = os.getcwd()
    paths.enter_data_dir()
    assert os.getcwd() == start


def test_the_login_is_read_from_the_data_folder_when_installed(monkeypatch, tmp_path):
    monkeypatch.setenv("BARBELL_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("LT_USER_FOR_TEST", raising=False)
    (tmp_path / ".env").write_text("LT_USER_FOR_TEST=from-the-data-folder\n", encoding="utf-8")
    paths.load_env()
    assert os.environ["LT_USER_FOR_TEST"] == "from-the-data-folder"
    monkeypatch.delenv("LT_USER_FOR_TEST")


# --- the app's own command line ---------------------------------------------------------------------

def test_version_flag_prints_the_version_and_exits():
    out = subprocess.run([sys.executable, str(ROOT / "barbell_gui.py"), "--version"],
                         capture_output=True, text=True, timeout=60)
    assert out.returncode == 0 and out.stdout.strip() == version_string()


def test_selftest_starts_the_app_in_the_data_folder_and_reports_what_it_found(tmp_path):
    report = tmp_path / "report.json"
    env = {**os.environ, "BARBELL_DATA_DIR": str(tmp_path / "data")}
    out = subprocess.run([sys.executable, str(ROOT / "barbell_gui.py"), "--selftest", str(report)],
                         capture_output=True, text=True, timeout=90, env=env)
    assert out.returncode == 0, out.stderr
    info = json.loads(report.read_text())
    assert info["title"] == f"BarBell {version_string()}"
    assert info["menu"] == ["Home", "Help"]
    assert info["logos_loaded"] is True
    assert info["data_dir"] == str(tmp_path / "data") and info["cwd"] == str(tmp_path / "data")
    assert info["settings_file"] == str(tmp_path / "data" / "settings.json")


def test_the_installed_exe_starts_setup_by_running_itself_with_setup(app, monkeypatch, tmp_path):
    """There is no setup_gui.py inside an .exe, so BarBell.exe re-runs itself as 'BarBell.exe --setup'."""
    launched = []
    monkeypatch.setattr("barbell_gui.paths.is_frozen", lambda: True)
    monkeypatch.setattr("barbell_gui.paths.data_dir", lambda: tmp_path / "data")
    monkeypatch.setattr("barbell_gui.simpledialog.askstring", lambda *a, **k: "change4GOOD")
    monkeypatch.setattr("barbell_gui.load_settings", lambda *a, **k: __import__("src.settings", fromlist=["Settings"]).Settings())
    monkeypatch.setattr("barbell_gui.subprocess.Popen", lambda cmd, **k: launched.append((cmd, k)))

    app._prompt_setup_password()

    (command, kwargs), = launched
    assert command == [sys.executable, "--setup", "--access-level", "standard"]
    assert kwargs["cwd"] == str(tmp_path / "data")


# --- what the build stages and stamps ------------------------------------------------------------------------

@pytest.fixture
def staged(tmp_path, monkeypatch):
    monkeypatch.setattr(build, "BUILD", tmp_path)
    monkeypatch.setattr(build, "STAGE", tmp_path / "stage")
    build.stage_sources()
    build.set_package_version()
    return tmp_path / "stage"


def _staged_version(staged: Path) -> str:
    spec = importlib.util.spec_from_file_location("staged_version", staged / "src" / "version.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.version_string()


def test_the_package_is_stamped_1_2_0_beta(staged):
    assert _staged_version(staged) == "1.2.0 Beta"
    assert build.release_label() == "1.2.0 Beta"


def test_the_development_copy_keeps_its_own_1_1_x_version(staged):
    assert version_string().startswith("1.1.")  # untouched by the build
    assert "1.2.0" not in (ROOT / "src" / "version.py").read_text(encoding="utf-8").split("MAJOR")[1].split("BUILD_DATE")[0]


def test_only_what_ships_is_staged_and_never_anyones_data(staged):
    names = {p.name for p in staged.rglob("*")}
    assert {"barbell_gui.py", "setup_gui.py", "helper_main.py", "barbell_app_icon.ico", "lcj_logo.png"} <= names
    assert not (staged / "tests").exists()
    for forbidden in (".env", "settings.json", "barbell.db", "sscc_state.json", "gtin_audit_log.jsonl"):
        assert forbidden not in names


# --- the installer script still says what the requirements say -----------------------------------------------------

def test_targets_windows_11_only():
    assert "MinVersion=10.0.22000" in ISS
    assert "ArchitecturesAllowed=x64compatible" in ISS


def test_prompts_for_the_install_folder_and_offers_c_barbell():
    assert "DefaultDirName=C:\\BarBell" in ISS
    assert "DisableDirPage=no" in ISS


def test_is_labelled_1_2_0_beta():
    assert '#define AppVersionLabel "1.2.0 Beta"' in ISS
    assert "AppVersion={#AppVersionLabel}" in ISS
    assert "OutputBaseFilename=BarBell-Setup-{#AppVersion}-Beta" in ISS


def test_creates_a_desktop_icon_by_default_from_the_programs_own_icon():
    assert re.search(r'^Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription', ISS, re.M)
    assert "unchecked" not in re.search(r'^Name: "desktopicon".*$', ISS, re.M).group(0)
    assert re.search(r'\{autodesktop\}\\BarBell"; Filename: "\{app\}\\BarBell\.exe"; .*IconFilename: "\{app\}\\BarBell\.exe"', ISS)


def test_uninstalling_never_deletes_the_data():
    assert "[UninstallDelete]" not in ISS
    assert re.search(r'Name: "\{app\}\\data"; .*uninsneveruninstall', ISS)
    # the only thing cleared when upgrading is the program's own libraries
    install_delete = ISS.split("[InstallDelete]")[1].split("[Files]")[0]
    assert re.findall(r'Name: "([^"]+)"', install_delete) == ["{app}\\_internal"]


def test_checks_for_an_existing_installation_and_backs_up_before_any_file_is_installed():
    assert "procedure DetectAndBackup" in ISS
    assert "DetectAndBackup(WizardDirValue)" in ISS  # at the directory page...
    step = ISS.split("procedure CurStepChanged")[1]
    assert step.index("ssInstall") < step.index("ssPostInstall")
    assert "DetectAndBackup(WizardDirValue)" in step.split("ssPostInstall")[0]  # ...and again before files, for silent installs


def test_asks_keep_or_restore_or_blank_and_lets_the_user_pick_a_database_file():
    for needle in ("RbKeep", "RbFile", "RbBlank", "GetOpenFileName", "BrowseForFolder", "restore-db", "restore-backup", "'blank'"):
        assert needle in ISS


def test_prompts_about_the_label_traxx_odbc_driver_first():
    assert "CreateOutputMsgMemoPage(wpWelcome" in ISS  # straight after the welcome page, before the folder
    assert "LT64" in ISS and "LCJ JAM" in ISS and "ODBC" in ISS


def test_a_blank_start_is_confirmed_when_there_is_data_to_lose_sight_of():
    assert "Start with a BLANK database?" in ISS
