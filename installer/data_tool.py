"""
Test-data tool for the installer's checks (installer/test_installer.ps1). Developer use only -
it is NOT shipped. Every command prints one JSON object.

  make   DIR [--serials 10-14] [--jamaica-serials 38-40] [--counter 14] [--jamaica-counter 40]
         Writes a BarBell data folder: barbell.db (cartons with real-looking SSCCs), the SSCC counter
         files, settings.json and a GTIN audit log - the way the app leaves them.
  check  PATH                  PATH is a data folder or a .db file: integrity, SSCC count, counters, SHA-256s.
  corrupt DB                   Damages a database file so it fails SQLite's integrity check.
  verify-backup FOLDER         Verifies a BarBell backup folder and reports what's in it.
  counter DIR NAME VALUE       Sets a counter file (sscc_state.json | sscc_state_jamaica.json).
"""

import argparse
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.backup import BackupError, verify_backup  # noqa: E402
from src.db.local_store import record_generation_run  # noqa: E402
from src.labels import LabelRow  # noqa: E402
from src.settings import Settings, save_settings  # noqa: E402
from src.sscc import _atomic_write_last_serial, build_sscc  # noqa: E402

PREFIX = "08600157112"


def _rows(serials, ext):
    return [
        LabelRow(
            job_number="123118", packing_slip_number="100512", customer_number="J00005", customer_name="JWN",
            product_no="41185", item_number="234412", item_description="234412 - JWN Kingston 62", quantity=12000,
            batch="12311841185", production_date="260505", sscc=build_sscc(PREFIX, ext, n),
            gtin="00636191205407", package_index=i, label_copy_index=1,
        )
        for i, n in enumerate(serials, start=1)
    ]


def _span(text: str):
    a, _, b = text.partition("-")
    return range(int(a), int(b or a) + 1)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check(path: Path) -> dict:
    data_dir = path if path.is_dir() else path.parent
    db = path if path.is_file() else path / "barbell.db"
    out: dict = {"db_exists": db.is_file()}
    if db.is_file():
        try:
            conn = sqlite3.connect(str(db))
            out["integrity"] = conn.execute("PRAGMA integrity_check").fetchone()[0]
            out["ssccs"] = conn.execute("SELECT COUNT(DISTINCT sscc) FROM labels").fetchone()[0]
            conn.close()
        except sqlite3.DatabaseError as exc:
            out["integrity"] = f"error: {exc}"
            out["ssccs"] = None
        out["sha256_db"] = _sha(db)
    counters = {}
    for plant, name in (("barbados", "sscc_state.json"), ("jamaica", "sscc_state_jamaica.json")):
        f = data_dir / name
        counters[plant] = json.loads(f.read_text())["last_serial"] if f.is_file() else None
        if f.is_file():
            out[f"sha256_{plant}"] = _sha(f)
    out["counters"] = counters
    return out


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("make")
    mk.add_argument("dir")
    mk.add_argument("--serials", default="10-14")
    mk.add_argument("--jamaica-serials", default="")
    mk.add_argument("--counter", type=int, default=14)
    mk.add_argument("--jamaica-counter", type=int, default=None)
    ck = sub.add_parser("check")
    ck.add_argument("path")
    co = sub.add_parser("corrupt")
    co.add_argument("db")
    vb = sub.add_parser("verify-backup")
    vb.add_argument("folder")
    ct = sub.add_parser("counter")
    ct.add_argument("dir")
    ct.add_argument("name")
    ct.add_argument("value", type=int)
    args = p.parse_args(argv)

    if args.cmd == "make":
        d = Path(args.dir)
        d.mkdir(parents=True, exist_ok=True)
        db = d / "barbell.db"
        record_generation_run(_rows(_span(args.serials), "0"), units_per_package=12000, labels_per_package=1,
                              test_mode=False, db_path=db)
        if args.jamaica_serials:
            record_generation_run(_rows(_span(args.jamaica_serials), "1"), units_per_package=12000,
                                  labels_per_package=1, test_mode=False, db_path=db)
        _atomic_write_last_serial(d / "sscc_state.json", args.counter)
        if args.jamaica_counter is not None:
            _atomic_write_last_serial(d / "sscc_state_jamaica.json", args.jamaica_counter)
        save_settings(Settings(gs1_company_prefix=PREFIX, jamaica_gs1_company_prefix=PREFIX), d / "settings.json")
        (d / "gtin_audit_log.jsonl").write_text('{"test": true}\n', encoding="utf-8")
        print(json.dumps(_check(d)))
    elif args.cmd == "check":
        print(json.dumps(_check(Path(args.path))))
    elif args.cmd == "corrupt":
        raw = bytearray(Path(args.db).read_bytes())
        for i in range(100, len(raw), 4096):
            raw[i:i + 64] = b"\xff" * 64
        Path(args.db).write_bytes(bytes(raw))
        print(json.dumps({"ok": True}))
    elif args.cmd == "verify-backup":
        try:
            m = verify_backup(args.folder)
            print(json.dumps({"ok": True, "reason": m.get("reason"), "ssccs": m.get("distinct_ssccs"),
                              "counters": m.get("counters")}))
        except BackupError as exc:
            print(json.dumps({"ok": False, "error": str(exc)}))
    elif args.cmd == "counter":
        _atomic_write_last_serial(Path(args.dir) / args.name, args.value)
        print(json.dumps({"ok": True}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
