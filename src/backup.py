"""
Backup and restore of everything BarBell cannot afford to lose.

A backup is one timestamped folder holding a CONSISTENT SET, because the
database alone isn't enough:

  - barbell.db  - every label/pallet BarBell has issued (copied with SQLite's
                  own online-backup call, so it's consistent even if another
                  process is using the file - never a raw file copy)
  - the SSCC counter files (Barbados and Jamaica) - these stop BarBell from
                  ever reusing an SSCC (a hard GS1 requirement, see
                  src/sscc.py), so they matter at least as much as the DB
  - settings.json and the GTIN audit log - kept for manual disaster recovery
  - manifest.json - what's in the folder, with SHA-256 hashes, so a restore
                  can prove the backup is intact before touching anything

Retention: the newest `keep` backups are kept (default 10) and older ones are
deleted - never fewer than one, and only folders this module made (they carry
a manifest.json). Pruning only happens AFTER a new backup succeeds and passes
an integrity check, so a failing backup can never rotate good ones away. A
backup is skipped when nothing has changed since the newest one, so opening
and closing BarBell repeatedly doesn't push older, different backups out.

Restore (see restore_backup) brings back the database and the counters - NOT
settings.json or the audit log, which describe THIS machine's configuration
and an append-only history that a restore must not rewind. Its overriding
rule: a restore never moves an SSCC counter backwards. Each counter becomes
the highest of (the backup's, the live file's, the highest serial actually
found in the restored database), because reissuing an SSCC is far worse than
skipping some. A safety backup of the current state is always taken first, so
a restore can itself be undone.
"""

import datetime
import hashlib
import json
import re
import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from src.settings import DEFAULT_SETTINGS_FILE
from src.sscc import _atomic_write_last_serial
from src.version import version_string

MANIFEST_NAME = "manifest.json"
MANIFEST_FORMAT = 1
BACKUP_NAME_RE = re.compile(r"^barbell_backup_\d{8}_\d{6}(?:_[a-z-]+)?(?:_\d+)?$")

REASON_EXIT = "exit"
REASON_MANUAL = "manual"
REASON_PRE_RESTORE = "pre-restore"
REASON_PRE_INSTALL = "pre-install"  # taken by the installer before it changes anything
# Safety backups: named with their reason, never counted against the rolling limit and never pruned.
_KEEP_FOREVER = (REASON_PRE_RESTORE, REASON_PRE_INSTALL)

# role -> file name inside the backup folder
ROLE_DB = "database"
ROLE_COUNTER_BARBADOS = "sscc_counter_barbados"
ROLE_COUNTER_JAMAICA = "sscc_counter_jamaica"
ROLE_SETTINGS = "settings"
ROLE_AUDIT_LOG = "gtin_audit_log"
_BACKUP_FILE_NAMES = {
    ROLE_DB: "barbell.db",
    ROLE_COUNTER_BARBADOS: "sscc_state.json",
    ROLE_COUNTER_JAMAICA: "sscc_state_jamaica.json",
    ROLE_SETTINGS: "settings.json",
    ROLE_AUDIT_LOG: "gtin_audit_log.jsonl",
}
# what counts as "changed" for skip-if-unchanged: the data, not the config
_FINGERPRINT_ROLES = (ROLE_DB, ROLE_COUNTER_BARBADOS, ROLE_COUNTER_JAMAICA, ROLE_AUDIT_LOG)


class BackupError(Exception):
    """A backup/restore problem the user should be told about in plain words."""


@dataclass
class BackupResult:
    path: Path | None  # the new backup folder, or None if skipped
    skipped: bool
    message: str


@dataclass
class RestoreSummary:
    """What a restore WOULD do - shown to the user for confirmation."""

    backup_dir: Path
    created_at: str
    app_version: str
    reason: str
    cartons_and_pallets_in_backup: int  # distinct SSCCs in the backup's database
    only_in_current: int  # distinct SSCCs in the live database that the backup lacks
    counters: dict  # plant -> {"backup": int|None, "current": int|None}


@dataclass
class RestoreResult:
    safety_backup: Path | None
    counters_after: dict  # plant -> last_serial now in the live counter file
    counters_raised: dict  # plant -> (old, new) for counters the restore had to raise


# --- locating what to back up ----------------------------------------------------

def _plants(settings) -> dict:
    """plant -> (counter role, company prefix, extension digit, counter file)."""
    return {
        "barbados": (
            ROLE_COUNTER_BARBADOS, settings.gs1_company_prefix, settings.sscc_extension_digit,
            Path(settings.sscc_state_file),
        ),
        "jamaica": (
            ROLE_COUNTER_JAMAICA,
            settings.jamaica_gs1_company_prefix or settings.gs1_company_prefix,
            settings.jamaica_sscc_extension_digit, Path(settings.jamaica_sscc_state_file),
        ),
    }


def _source_files(settings, settings_file: Path) -> dict:
    """role -> the live file (only those that exist)."""
    candidates = {
        ROLE_DB: Path(settings.local_db_file),
        ROLE_COUNTER_BARBADOS: Path(settings.sscc_state_file),
        ROLE_COUNTER_JAMAICA: Path(settings.jamaica_sscc_state_file),
        ROLE_SETTINGS: Path(settings_file),
        ROLE_AUDIT_LOG: Path(settings.audit_log_file),
    }
    return {role: path for role, path in candidates.items() if path.is_file()}


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_last_serial(path: Path) -> int | None:
    try:
        with open(path, encoding="utf-8") as f:
            return int(json.load(f)["last_serial"])
    except (OSError, ValueError, KeyError):
        return None


def _distinct_ssccs(db_path: Path) -> set[str]:
    conn = sqlite3.connect(str(db_path))
    try:
        return {row[0] for row in conn.execute("SELECT DISTINCT sscc FROM labels")}
    except sqlite3.DatabaseError:
        return set()  # a DB without a labels table yet (brand new)
    finally:
        conn.close()


def _highest_serial_in_db(db_path: Path, prefix: str, extension_digit: str) -> int | None:
    """Highest serial reference among SSCCs this plant's prefix+extension
    digit could have issued (cartons AND pallets share one counter)."""
    if not prefix or not extension_digit:
        return None
    lead = extension_digit + prefix
    width = 16 - len(prefix)
    if width < 1:
        return None
    highest = None
    for sscc in _distinct_ssccs(db_path):
        if len(sscc) == 18 and sscc.isdigit() and sscc.startswith(lead):
            serial = int(sscc[len(lead):17])
            highest = serial if highest is None else max(highest, serial)
    return highest


def _integrity_ok(db_path: Path) -> bool:
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute("PRAGMA integrity_check").fetchall() == [("ok",)]
    except sqlite3.DatabaseError:
        return False
    finally:
        conn.close()


def _copy_database(src: Path, dst: Path) -> None:
    """SQLite online backup: a consistent snapshot even if another process
    has the source open. Replaces whatever dst held, transactionally."""
    source = sqlite3.connect(str(src))
    try:
        target = sqlite3.connect(str(dst))
        try:
            source.backup(target)
        finally:
            target.close()
    except sqlite3.OperationalError as exc:
        raise BackupError(
            f"Couldn't copy the database ({exc}). If BarBell or another program has it "
            "locked, close it and try again."
        ) from exc
    finally:
        source.close()


# --- listing ------------------------------------------------------------------------

def _read_manifest(folder: Path) -> dict | None:
    try:
        with open(folder / MANIFEST_NAME, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) and data.get("format") == MANIFEST_FORMAT else None
    except (OSError, ValueError):
        return None


def list_backups(dest_root: Path | str) -> list[Path]:
    """Backup folders made by this module, oldest first (names sort by time)."""
    root = Path(dest_root)
    if not root.is_dir():
        return []
    return sorted(
        p for p in root.iterdir()
        if p.is_dir() and BACKUP_NAME_RE.match(p.name) and _read_manifest(p) is not None
    )


def _prune(dest_root: Path, keep: int) -> list[Path]:
    """Deletes the oldest regular (not pre-restore) backups beyond `keep`."""
    keep = max(1, int(keep))
    regular = [p for p in list_backups(dest_root) if _read_manifest(p).get("reason") not in _KEEP_FOREVER]
    removed = []
    for old in regular[: max(0, len(regular) - keep)]:
        try:
            shutil.rmtree(old)
        except OSError:
            continue  # something has a file open in it - leave it, try again next time
        removed.append(old)
    return removed


# --- backup -----------------------------------------------------------------------

def create_backup(
    settings,
    dest_root: Path | str,
    reason: str = REASON_MANUAL,
    settings_file: Path | str = DEFAULT_SETTINGS_FILE,
    skip_if_unchanged: bool = True,
    now: datetime.datetime | None = None,
) -> BackupResult:
    """
    Writes a new backup folder under dest_root. Raises BackupError if it can't
    be made or fails its integrity check (and in that case leaves no partial
    folder behind and prunes nothing).
    """
    dest_root = Path(dest_root)
    now = now or datetime.datetime.now()
    sources = _source_files(settings, Path(settings_file))
    if not sources:
        return BackupResult(None, True, "There's nothing to back up yet.")

    fingerprint = hashlib.sha256()
    for role in _FINGERPRINT_ROLES:
        if role in sources:
            fingerprint.update(f"{role}:{_sha256(sources[role])};".encode())
    fingerprint_hex = fingerprint.hexdigest()

    existing = list_backups(dest_root)
    if skip_if_unchanged and existing:
        latest = _read_manifest(existing[-1])
        if latest and latest.get("fingerprint") == fingerprint_hex:
            return BackupResult(
                None, True, f"Nothing has changed since the last backup ({existing[-1].name})."
            )

    try:
        dest_root.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise BackupError(f"Can't use the backup folder {dest_root}: {exc}") from exc

    stamp = now.strftime("%Y%m%d_%H%M%S")
    suffix = f"_{reason}" if reason in _KEEP_FOREVER else ""
    final = dest_root / f"barbell_backup_{stamp}{suffix}"
    n = 1
    while final.exists():
        n += 1
        final = dest_root / f"barbell_backup_{stamp}{suffix}_{n}"

    # Written straight into its final folder, manifest LAST: a folder with no
    # manifest isn't a backup as far as list_backups/_prune/verify_backup are
    # concerned, so an interrupted run is never mistaken for a good one. (No
    # write-then-rename of the folder: on Windows an antivirus scan or the
    # indexer can briefly hold a file in a new folder and make that rename fail.)
    try:
        final.mkdir()
        files = {}
        for role, src in sources.items():
            dst = final / _BACKUP_FILE_NAMES[role]
            if role == ROLE_DB:
                _copy_database(src, dst)
                if not _integrity_ok(dst):
                    raise BackupError(
                        "The database failed its integrity check, so this backup was NOT kept "
                        "(your existing backups were left alone). The database may be damaged."
                    )
            else:
                shutil.copy2(src, dst)
            files[role] = {"name": dst.name, "sha256": _sha256(dst), "bytes": dst.stat().st_size}

        manifest = {
            "format": MANIFEST_FORMAT,
            "created_at": now.isoformat(timespec="seconds"),
            "app_version": version_string(),
            "reason": reason,
            "fingerprint": fingerprint_hex,
            "files": files,
            "distinct_ssccs": len(_distinct_ssccs(final / files[ROLE_DB]["name"])) if ROLE_DB in files else 0,
            "counters": {
                plant: _read_last_serial(final / files[role]["name"]) if role in files else None
                for plant, (role, *_rest) in _plants(settings).items()
            },
        }
        with open(final / MANIFEST_NAME, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
    except BaseException:
        shutil.rmtree(final, ignore_errors=True)
        raise

    removed = _prune(dest_root, getattr(settings, "backup_keep_count", 10)) if reason not in _KEEP_FOREVER else []
    note = f" ({len(removed)} older backup(s) removed)" if removed else ""
    return BackupResult(final, False, f"Backed up to {final}{note}")


# --- verify / restore ------------------------------------------------------------

def verify_backup(backup_dir: Path | str) -> dict:
    """Proves a backup folder is intact (manifest present, every file present
    with a matching SHA-256, database passes its integrity check). Returns
    the manifest; raises BackupError saying what's wrong."""
    folder = Path(backup_dir)
    manifest = _read_manifest(folder)
    if manifest is None:
        raise BackupError(f"{folder} isn't a BarBell backup folder (no valid {MANIFEST_NAME}).")
    for role, info in manifest["files"].items():
        path = folder / info["name"]
        if not path.is_file():
            raise BackupError(f"The backup is incomplete: {info['name']} is missing.")
        if _sha256(path) != info["sha256"]:
            raise BackupError(f"The backup is damaged: {info['name']} doesn't match its recorded checksum.")
    if ROLE_DB not in manifest["files"]:
        raise BackupError("This backup has no database in it, so there's nothing to restore.")
    if not _integrity_ok(folder / manifest["files"][ROLE_DB]["name"]):
        raise BackupError("The backed-up database fails its integrity check.")
    return manifest


def summarize_restore(backup_dir: Path | str, settings) -> RestoreSummary:
    """What restoring this backup would change - verifies it first."""
    manifest = verify_backup(backup_dir)
    folder = Path(backup_dir)
    in_backup = _distinct_ssccs(folder / manifest["files"][ROLE_DB]["name"])
    live_db = Path(settings.local_db_file)
    in_current = _distinct_ssccs(live_db) if live_db.is_file() else set()
    counters = {
        plant: {"backup": manifest.get("counters", {}).get(plant), "current": _read_last_serial(path)}
        for plant, (_role, _prefix, _ext, path) in _plants(settings).items()
    }
    return RestoreSummary(
        backup_dir=folder, created_at=manifest["created_at"], app_version=manifest["app_version"],
        reason=manifest.get("reason", ""), cartons_and_pallets_in_backup=len(in_backup),
        only_in_current=len(in_current - in_backup), counters=counters,
    )


def restore_backup(
    backup_dir: Path | str,
    settings,
    dest_root: Path | str,
    settings_file: Path | str = DEFAULT_SETTINGS_FILE,
) -> RestoreResult:
    """
    Restores the database and SSCC counters from a verified backup.
    Order matters: verify the backup -> take a safety backup of the current
    state -> restore the database -> raise (never lower) each counter.
    """
    manifest = verify_backup(backup_dir)
    folder = Path(backup_dir)

    safety = create_backup(
        settings, dest_root, reason=REASON_PRE_RESTORE, settings_file=settings_file,
        skip_if_unchanged=False,
    ).path

    live_db = Path(settings.local_db_file)
    live_db.parent.mkdir(parents=True, exist_ok=True)
    _copy_database(folder / manifest["files"][ROLE_DB]["name"], live_db)
    if not _integrity_ok(live_db):
        raise BackupError(
            "The restored database failed its integrity check. Your previous data is in the "
            f"safety backup: {safety}"
        )

    counters_after, counters_raised = {}, {}
    for plant, (role, prefix, extension_digit, live_counter) in _plants(settings).items():
        backup_last = (
            _read_last_serial(folder / manifest["files"][role]["name"]) if role in manifest["files"] else None
        )
        current_last = _read_last_serial(live_counter) if live_counter.is_file() else None
        db_floor = _highest_serial_in_db(live_db, prefix, extension_digit)
        candidates = [v for v in (backup_last, current_last, db_floor) if v is not None]
        if not candidates:
            continue  # this plant has never issued anything - nothing to restore
        target = max(candidates)
        if current_last is None or target > current_last:
            live_counter.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_last_serial(live_counter, target)
            counters_raised[plant] = (current_last, target)
        counters_after[plant] = target
    return RestoreResult(safety, counters_after, counters_raised)
