"""
Where BarBell's files live - one place that knows the difference between
running from a source folder (development) and running as an installed .exe.

  Development (python barbell_gui.py): nothing changes. The program's files and
  its data (settings.json, barbell.db, the SSCC counters, .env) are all in the
  project folder, found relative to it, exactly as before.

  Installed (the PyInstaller .exe, e.g. C:\\BarBell):
      <install dir>\\BarBell.exe ... the program (and its bundled assets)
      <install dir>\\data\\          settings.json, barbell.db, the SSCC counter
                                    files, the audit log, .env - everything that
                                    belongs to THIS machine and must survive an
                                    upgrade or uninstall.
  enter_data_dir() makes the data folder the working directory at startup, so
  the many settings that are relative file names ("barbell.db",
  "sscc_state.json", "output", ...) land in it without each needing to know.

BARBELL_DATA_DIR overrides the data folder (used by the installer's own tests).
"""

import os
import sys
from pathlib import Path

DATA_DIR_NAME = "data"


def is_frozen() -> bool:
    """True when running as the PyInstaller-built .exe."""
    return bool(getattr(sys, "frozen", False))


def install_dir() -> Path:
    """The folder holding BarBell.exe when installed; the project folder when
    running from source."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    override = os.environ.get("BARBELL_DATA_DIR")
    if override:
        return Path(override)
    if is_frozen():
        return install_dir() / DATA_DIR_NAME
    return install_dir()  # development: data sits in the project folder, as always


def settings_file() -> Path:
    return data_dir() / "settings.json"


def env_file() -> Path:
    return data_dir() / ".env"


def enter_data_dir() -> None:
    """Installed: create the data folder if needed and make it the working
    directory. Development: does nothing (the working directory is already
    wherever the developer ran from, as before)."""
    if is_frozen() or os.environ.get("BARBELL_DATA_DIR"):
        folder = data_dir()
        folder.mkdir(parents=True, exist_ok=True)
        os.chdir(folder)


def load_env() -> None:
    """Loads the Label Traxx login (.env). Installed: from the data folder.
    Development: python-dotenv's usual search, as before."""
    from dotenv import load_dotenv

    if is_frozen() or os.environ.get("BARBELL_DATA_DIR"):
        load_dotenv(env_file())
    else:
        load_dotenv()
