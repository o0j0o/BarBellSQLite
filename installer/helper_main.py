"""
BarBell installer helper - the small console program the Windows installer
(installer/BarBell.iss) runs for everything that touches BarBell's data. The
wizard can only run a program and read a file, so every command here writes its
answer as JSON to --out and exits 0 (ok) or 1 (not ok); the logic itself is
src/installer_support.py, which is unit-tested.

  detect   --candidate DIR [--candidate DIR ...] --out FILE
  backup   --existing-root DIR --backup-root DIR --out FILE
  inspect  --source FILE_OR_BACKUP_FOLDER --out FILE
  apply    --data-dir DIR --mode keep|blank|restore-backup|restore-db [--source PATH] --backup-root DIR --out FILE
  version  --out FILE
"""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from src import installer_support as support
from src.version import version_string


def _flatten(prefix: str, value, into: dict) -> None:
    """dicts become dotted keys; lists are skipped (the INI is for simple answers)."""
    if isinstance(value, dict):
        for key, inner in value.items():
            _flatten(f"{prefix}.{key}" if prefix else str(key), inner, into)
    elif isinstance(value, bool):
        into[prefix] = "true" if value else "false"
    elif isinstance(value, (str, int, float)) or value is None:
        into[prefix] = "" if value is None else str(value).replace("\r", " ").replace("\n", " ")


def _write(out: str, payload: dict) -> int:
    """Writes the answer twice: JSON (for people and tests) and <out>.ini (flat key=value,
    because the installer wizard can read an INI file but not parse JSON)."""
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    flat: dict = {}
    _flatten("", payload, flat)
    with open(out + ".ini", "w", encoding="utf-8") as f:
        f.write("[result]\n")
        for key, value in flat.items():
            f.write(f"{key}={value}\n")
    return 0 if payload.get("ok", False) else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="barbell_install_helper")
    sub = parser.add_subparsers(dest="command", required=True)

    detect = sub.add_parser("detect")
    detect.add_argument("--candidate", action="append", default=[])
    detect.add_argument("--out", required=True)

    backup = sub.add_parser("backup")
    backup.add_argument("--existing-root", required=True)
    backup.add_argument("--backup-root", required=True)
    backup.add_argument("--out", required=True)

    inspect = sub.add_parser("inspect")
    inspect.add_argument("--source", required=True)
    inspect.add_argument("--out", required=True)

    apply = sub.add_parser("apply")
    apply.add_argument("--data-dir", required=True)
    apply.add_argument("--mode", required=True, choices=[support.MODE_BLANK, support.MODE_KEEP, support.MODE_RESTORE_BACKUP, support.MODE_RESTORE_DB])
    apply.add_argument("--source", default="")
    apply.add_argument("--backup-root", required=True)
    apply.add_argument("--out", required=True)

    version = sub.add_parser("version")
    version.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "detect":
            existing = support.find_existing(args.candidate)
            return _write(args.out, {"ok": True, "found": existing is not None,
                                      "install": asdict(existing) if existing else None,
                                      "has_data": bool(existing and existing.has_data)})
        if args.command == "backup":
            existing = support.find_existing([args.existing_root])
            if existing is None:
                return _write(args.out, {"ok": True, "verified_backup": None, "raw_copy": None,
                                          "message": "Nothing found to back up."})
            return _write(args.out, support.backup_existing(existing, args.backup_root))
        if args.command == "inspect":
            return _write(args.out, support.inspect_source(args.source))
        if args.command == "apply":
            return _write(args.out, support.apply_data_choice(
                args.data_dir, args.mode, args.source or None, args.backup_root))
        if args.command == "version":
            return _write(args.out, {"ok": True, "version": version_string()})
    except Exception as exc:  # noqa: BLE001 - the wizard must always get an answer file, never a crash
        return _write(args.out, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})
    return 1


if __name__ == "__main__":
    sys.exit(main())
