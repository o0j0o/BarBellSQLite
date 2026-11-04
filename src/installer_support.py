"""
The data-handling half of the Windows installer: everything that can lose or
corrupt BarBell's data lives here as ordinary, tested Python (the installer
wizard itself only asks questions and calls this - see installer/helper_main.py).

What the installer does, in order, and which function does it:

  1. find_existing()   - is BarBell already on this PC? Looks in the install
                         folder chosen, the folder a previous install recorded,
                         and the default folder. Understands both layouts: the
                         installed one (<dir>\\data holds the data) and a manual /
                         source-folder copy (data beside the program).
  2. backup_existing() - BEFORE anything is changed, back up what is there: a
                         verified backup set (database + both SSCC counters +
                         settings + audit log, via src/backup.py) kept in a
                         folder that uninstalling never touches. If the database
                         is damaged and so can't be verified, a raw copy of the
                         files is kept instead - evidence, never deleted - and
                         the user is told the backup is NOT restorable.
  3. inspect_source()  - what the user is about to restore from: a verified
                         backup folder, or a bare .db file they picked. Checks it
                         is intact and summarises it (labels, newest date).
  4. apply_data_choice() - after the program is installed: restore from a backup,
                         restore from a database file, or start blank.

The rule behind all of it: an SSCC counter NEVER moves backwards. Reissuing an
SSCC that already went out on a carton is far worse than skipping numbers, so a
restore raises each counter to at least the highest serial found in the
restored database, and "start blank" empties the history but leaves the
counters exactly as they are.
"""

import datetime
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from src.backup import (
    REASON_PRE_INSTALL,
    BackupError,
    _copy_database,
    _distinct_ssccs,
    _highest_serial_in_db,
    _integrity_ok,
    _read_last_serial,
    create_backup,
    restore_backup,
    verify_backup,
)
from src.settings import Settings, load_settings
from src.sscc import _atomic_write_last_serial

# CLC's GS1 Company Prefix (see src/sscc.py). Used ONLY to work out counter floors
# when a bare database file is restored on a machine that has no settings yet.
CLC_GS1_COMPANY_PREFIX = "08600157112"

DB_NAME = "barbell.db"
COUNTER_NAMES = {"barbados": "sscc_state.json", "jamaica": "sscc_state_jamaica.json"}
SETTINGS_NAME = "settings.json"
AUDIT_NAME = "gtin_audit_log.jsonl"
DATA_FILE_NAMES = (DB_NAME, *COUNTER_NAMES.values(), SETTINGS_NAME, AUDIT_NAME)

MODE_BLANK = "blank"
MODE_KEEP = "keep"  # the data is already where it should be (upgrade in place): leave it alone
MODE_RESTORE_BACKUP = "restore-backup"
MODE_RESTORE_DB = "restore-db"


def _stamp(now: datetime.datetime | None) -> str:
    return (now or datetime.datetime.now()).strftime("%Y%m%d_%H%M%S")


# --- 1. is BarBell already here? ------------------------------------------------------

@dataclass
class ExistingInstall:
    root: str  # the folder that was found
    data_dir: str  # where its data is (root\data when installed, root itself for a manual copy)
    layout: str  # "installed" | "source-folder" | "program-only"
    has_program: bool
    database: str | None
    counters: dict  # plant -> file path or None
    settings_file: str | None
    audit_log: str | None

    @property
    def has_data(self) -> bool:
        return bool(self.database or any(self.counters.values()) or self.settings_file or self.audit_log)


def _data_in(folder: Path) -> bool:
    return any((folder / name).is_file() for name in DATA_FILE_NAMES)


def find_existing(candidates) -> ExistingInstall | None:
    """The first candidate folder that holds a BarBell install or BarBell data,
    or None. Candidates are tried in order."""
    seen = set()
    for candidate in candidates:
        if not candidate:
            continue
        root = Path(candidate)
        key = str(root).lower()
        if key in seen or not root.is_dir():
            continue
        seen.add(key)
        has_program = (root / "BarBell.exe").is_file() or (root / "barbell_gui.py").is_file()
        for layout, data in (("installed", root / "data"), ("source-folder", root)):
            if _data_in(data):
                return _describe_install(root, data, layout, has_program)
        if has_program:
            return _describe_install(root, root / "data", "program-only", True)
    return None


def _describe_install(root: Path, data: Path, layout: str, has_program: bool) -> ExistingInstall:
    def existing(name):
        return str(data / name) if (data / name).is_file() else None

    return ExistingInstall(
        root=str(root), data_dir=str(data), layout=layout, has_program=has_program,
        database=existing(DB_NAME),
        counters={plant: existing(name) for plant, name in COUNTER_NAMES.items()},
        settings_file=existing(SETTINGS_NAME), audit_log=existing(AUDIT_NAME),
    )


def settings_for(data_dir: Path, settings_path: Path | None = None) -> Settings:
    """Settings describing the data in data_dir: whatever its settings.json says
    (prefix, extension digits, ...) with every file path made absolute inside
    data_dir - or left alone if the install deliberately points elsewhere.
    settings_path reads the values from a different file (e.g. a backup's)
    while still resolving paths against data_dir."""
    data_dir = Path(data_dir)
    settings_path = Path(settings_path) if settings_path else data_dir / SETTINGS_NAME
    try:
        settings = load_settings(settings_path)
    except (OSError, ValueError):  # damaged settings.json: carry on with defaults, never block a backup
        settings = Settings()

    def resolve(value: str, default_name: str) -> str:
        path = Path(value or default_name)
        return str(path if path.is_absolute() else data_dir / path)

    settings.local_db_file = resolve(settings.local_db_file, DB_NAME)
    settings.sscc_state_file = resolve(settings.sscc_state_file, COUNTER_NAMES["barbados"])
    settings.jamaica_sscc_state_file = resolve(settings.jamaica_sscc_state_file, COUNTER_NAMES["jamaica"])
    settings.audit_log_file = resolve(settings.audit_log_file, AUDIT_NAME)
    return settings


# --- 2. back up what's there, before anything changes ------------------------------------

def backup_existing(existing: ExistingInstall, backup_root: Path | str, now: datetime.datetime | None = None) -> dict:
    """Backs up an existing install. Returns:
      verified_backup - path of a verified backup set (restorable), or None
      raw_copy        - path of an unverified copy of the files (when the database
                        was too damaged to verify), or None
      ok              - True if the data is safe to proceed past (a backup of one
                        kind exists, or there was nothing to back up)
    """
    backup_root = Path(backup_root)
    data_dir = Path(existing.data_dir)
    if not existing.has_data:
        return {"ok": True, "verified_backup": None, "raw_copy": None, "message": "There was no data to back up."}

    settings = settings_for(data_dir)
    try:
        result = create_backup(
            settings, backup_root, REASON_PRE_INSTALL, settings_file=data_dir / SETTINGS_NAME,
            skip_if_unchanged=False, now=now,
        )
        return {
            "ok": True, "verified_backup": str(result.path) if result.path else None, "raw_copy": None,
            "message": result.message,
        }
    except BackupError as exc:
        raw = _raw_copy(existing, settings, backup_root, now)
        return {
            "ok": raw is not None, "verified_backup": None, "raw_copy": str(raw) if raw else None,
            "message": (
                f"The database could not be verified ({exc}). A raw copy of the files was kept at {raw}; "
                "it is evidence and cannot be restored automatically."
                if raw else f"The existing data could not be backed up: {exc}"
            ),
        }


def _raw_copy(existing: ExistingInstall, settings: Settings, backup_root: Path, now) -> Path | None:
    folder = backup_root / f"barbell_rawcopy_{_stamp(now)}"
    try:
        folder.mkdir(parents=True, exist_ok=True)
        sources = [
            Path(settings.local_db_file), Path(settings.sscc_state_file),
            Path(settings.jamaica_sscc_state_file), Path(settings.audit_log_file),
            Path(existing.data_dir) / SETTINGS_NAME,
        ]
        copied = 0
        for src in sources:
            if src.is_file():
                shutil.copy2(src, folder / src.name)
                copied += 1
        (folder / "README.txt").write_text(
            "Unverified copy of BarBell's files, taken by the installer because the database "
            "failed its integrity check. Keep it; do not delete it.\n", encoding="utf-8",
        )
        return folder if copied else None
    except OSError:
        return None


# --- 3. what is the user about to restore from? --------------------------------------------

def describe_database(path: Path | str) -> dict:
    """Is this a usable BarBell database, and what's in it?"""
    path = Path(path)
    if not path.is_file():
        return {"ok": False, "error": f"{path} does not exist."}
    if not _integrity_ok(path):
        return {"ok": False, "error": "That file is not a healthy BarBell database (it failed the integrity check)."}
    import sqlite3

    conn = sqlite3.connect(str(path))
    try:
        try:
            rows = conn.execute("SELECT COUNT(*) FROM labels").fetchone()[0]
            newest = conn.execute("SELECT MAX(created_at) FROM labels").fetchone()[0]
        except sqlite3.DatabaseError:
            return {"ok": False, "error": "That file is a database, but not a BarBell one (no label history in it)."}
    finally:
        conn.close()
    return {
        "ok": True, "kind": "database", "label_rows": rows, "distinct_ssccs": len(_distinct_ssccs(path)),
        "newest_label_at": newest, "bytes": path.stat().st_size,
    }


def inspect_source(source: Path | str) -> dict:
    """A verified backup folder or a bare .db file -> a summary the wizard can show."""
    source = Path(source)
    if source.is_dir():
        try:
            manifest = verify_backup(source)
        except BackupError as exc:
            return {"ok": False, "error": str(exc)}
        return {
            "ok": True, "kind": "backup", "created_at": manifest["created_at"],
            "app_version": manifest["app_version"], "distinct_ssccs": manifest.get("distinct_ssccs", 0),
            "counters": manifest.get("counters", {}), "reason": manifest.get("reason", ""),
        }
    return describe_database(source)


# --- 4. apply the user's choice ----------------------------------------------------------------

def apply_data_choice(
    data_dir: Path | str,
    mode: str,
    source: Path | str | None,
    backup_root: Path | str,
    now: datetime.datetime | None = None,
) -> dict:
    """Carries out 'restore from a backup', 'restore from a database file' or
    'start blank' in data_dir (created if needed). Never raises for an expected
    problem: returns {"ok": False, "error": ...} so the wizard can show it."""
    data_dir, backup_root = Path(data_dir), Path(backup_root)
    data_dir.mkdir(parents=True, exist_ok=True)
    try:
        if mode == MODE_KEEP:
            return _keep_in_place(data_dir)
        if mode == MODE_BLANK:
            return _start_blank(data_dir, now)
        if mode == MODE_RESTORE_BACKUP:
            return _restore_from_backup(data_dir, Path(source), backup_root, now)
        if mode == MODE_RESTORE_DB:
            return _restore_from_database_file(data_dir, Path(source), now)
        return {"ok": False, "error": f"Unknown data choice {mode!r}."}
    except BackupError as exc:
        return {"ok": False, "error": str(exc)}


def _move_aside(path: Path, now) -> Path | None:
    """Renames a file to <name>.replaced-<time>.<ext> - never deleted."""
    if not path.is_file():
        return None
    target = path.with_name(f"{path.stem}.replaced-{_stamp(now)}{path.suffix}")
    n = 1
    while target.exists():
        n += 1
        target = path.with_name(f"{path.stem}.replaced-{_stamp(now)}-{n}{path.suffix}")
    path.replace(target)
    return target


def _keep_in_place(data_dir: Path) -> dict:
    """Upgrading over an install whose data folder is the one being kept: nothing is
    moved or rewritten - but a database that is already damaged is reported, not
    waved through as 'kept'."""
    db = data_dir / DB_NAME
    if db.is_file() and not _integrity_ok(db):
        return {"ok": False, "error": "The existing database is damaged, so it cannot simply be kept. "
                                      "Choose to restore from a database file or backup instead."}
    return {"ok": True, "mode": MODE_KEEP, "message": "The existing data was left exactly as it is."}


def _start_blank(data_dir: Path, now) -> dict:
    moved = _move_aside(data_dir / DB_NAME, now)
    counters = {p: _read_last_serial(data_dir / n) for p, n in COUNTER_NAMES.items() if (data_dir / n).is_file()}
    return {
        "ok": True, "mode": MODE_BLANK, "old_database_kept_as": str(moved) if moved else None,
        "counters_left_unchanged": counters,
        "message": "Starting with a blank database. The SSCC counters were not touched.",
    }


def _restore_from_backup(data_dir: Path, backup: Path, backup_root: Path, now) -> dict:
    manifest = verify_backup(backup)
    live_settings = data_dir / SETTINGS_NAME
    backup_settings = backup / manifest["files"]["settings"]["name"] if "settings" in manifest["files"] else None
    # A machine with no settings yet (new PC, or wiped): work out prefix / extension digits - and so the
    # counter floors - from the settings the backup was made with, but only copy that file into place
    # AFTER the restore, so the safety backup the restore takes reflects what was really there.
    target = settings_for(data_dir, settings_path=None if live_settings.is_file() else backup_settings)
    result = restore_backup(backup, target, backup_root, settings_file=live_settings)
    if backup_settings and not live_settings.is_file():
        shutil.copy2(backup_settings, live_settings)
    if not (data_dir / AUDIT_NAME).is_file() and "gtin_audit_log" in manifest["files"]:
        shutil.copy2(backup / manifest["files"]["gtin_audit_log"]["name"], data_dir / AUDIT_NAME)
    return {
        "ok": True, "mode": MODE_RESTORE_BACKUP, "restored_from": str(backup),
        "safety_backup": str(result.safety_backup) if result.safety_backup else None,
        "counters_after": result.counters_after,
        "counters_raised": {p: list(v) for p, v in result.counters_raised.items()},
        "message": "Restored the database and SSCC counters from the backup.",
    }


def _restore_from_database_file(data_dir: Path, db_file: Path, now) -> dict:
    info = describe_database(db_file)
    if not info["ok"]:
        return {"ok": False, "error": info["error"]}

    target = settings_for(data_dir)
    live_db = Path(target.local_db_file)
    live_db.parent.mkdir(parents=True, exist_ok=True)
    moved = _move_aside(live_db, now)  # never overwrite in place; the old file stays beside it
    _copy_database(db_file, live_db)
    if not _integrity_ok(live_db):
        raise BackupError("The restored database failed its integrity check.")

    warnings, counters_set = [], {}
    known_prefix = bool(target.gs1_company_prefix)
    plants = {
        "barbados": (target.gs1_company_prefix or CLC_GS1_COMPANY_PREFIX, target.sscc_extension_digit, target.sscc_state_file),
        "jamaica": (
            target.jamaica_gs1_company_prefix or target.gs1_company_prefix or CLC_GS1_COMPANY_PREFIX,
            target.jamaica_sscc_extension_digit, target.jamaica_sscc_state_file,
        ),
    }
    for plant, (prefix, extension_digit, counter_file) in plants.items():
        floor = _highest_serial_in_db(live_db, prefix, extension_digit)
        if floor is None:
            continue  # this plant never issued anything that this database knows about
        counter_path = Path(counter_file)
        current = _read_last_serial(counter_path) if counter_path.is_file() else None
        new = floor if current is None else max(current, floor)
        if current is None or new > current:
            counter_path.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_last_serial(counter_path, new)
            counters_set[plant] = [current, new]
    if counters_set and not known_prefix:
        warnings.append(
            f"No settings were found, so the counters were set using CLC's GS1 Company Prefix "
            f"({CLC_GS1_COMPANY_PREFIX}). Check the prefix and counters in Setup before printing."
        )
    if not counters_set:
        warnings.append(
            "No SSCC counters could be worked out from this database. Check them in Setup before printing."
        )
    return {
        "ok": True, "mode": MODE_RESTORE_DB, "restored_from": str(db_file),
        "old_database_kept_as": str(moved) if moved else None, "counters_set": counters_set,
        "warnings": warnings, "message": "Restored the database from the file you chose.",
    }


def to_json_dict(obj) -> dict:
    return asdict(obj) if hasattr(obj, "__dataclass_fields__") else obj
