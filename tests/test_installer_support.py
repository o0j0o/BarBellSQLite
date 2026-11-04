import datetime
import json
import sqlite3
from pathlib import Path

import pytest

from installer.helper_main import main as helper_main
from src import installer_support as inst
from src.backup import REASON_PRE_INSTALL, create_backup, list_backups, verify_backup
from src.db.local_store import fetch_label_history, record_generation_run
from src.labels import LabelRow
from src.settings import Settings, save_settings
from src.sscc import _atomic_write_last_serial, build_sscc

PREFIX = "08600157112"
NOW = datetime.datetime(2026, 11, 5, 9, 30, 0)


def label_rows(serials, ext="0"):
    return [
        LabelRow(
            job_number="123118", packing_slip_number="100512", customer_number="J00005", customer_name="JWN",
            product_no="41185", item_number="234412", item_description="Rum", quantity=12000,
            batch="12311841185", production_date="260505", sscc=build_sscc(PREFIX, ext, n),
            gtin="00636191205407", package_index=i, label_copy_index=1,
        )
        for i, n in enumerate(serials, start=1)
    ]


def make_data(data_dir: Path, serials=(10, 11, 12), counter=12, jamaica_counter=None, with_settings=True):
    """A BarBell data folder as the app leaves it."""
    data_dir.mkdir(parents=True, exist_ok=True)
    record_generation_run(
        label_rows(serials), units_per_package=12000, labels_per_package=1, test_mode=False,
        db_path=data_dir / "barbell.db",
    )
    _atomic_write_last_serial(data_dir / "sscc_state.json", counter)
    if jamaica_counter is not None:
        _atomic_write_last_serial(data_dir / "sscc_state_jamaica.json", jamaica_counter)
    (data_dir / "gtin_audit_log.jsonl").write_text('{"a": 1}\n', encoding="utf-8")
    if with_settings:
        save_settings(
            Settings(gs1_company_prefix=PREFIX, sscc_extension_digit="0", jamaica_sscc_extension_digit="1"),
            data_dir / "settings.json",
        )
    return data_dir


def counter(data_dir: Path, name="sscc_state.json"):
    return json.loads((data_dir / name).read_text())["last_serial"]


def sscc_set(db):
    return {r.sscc for r in fetch_label_history(db)}


def serial_set(db, serials, ext="0"):
    return {build_sscc(PREFIX, ext, n) for n in serials}


# --- is BarBell already here? ---------------------------------------------------------------

def test_finds_an_installed_layout_install(tmp_path):
    root = tmp_path / "BarBell"
    make_data(root / "data")
    (root / "BarBell.exe").write_bytes(b"x")

    found = inst.find_existing([root])

    assert found.layout == "installed" and found.has_program and found.has_data
    assert found.data_dir == str(root / "data")
    assert found.database == str(root / "data" / "barbell.db")
    assert found.counters["barbados"] and found.counters["jamaica"] is None


def test_finds_a_manual_source_folder_copy_with_data_beside_the_program(tmp_path):
    root = tmp_path / "logistic_label-app"
    make_data(root)
    (root / "barbell_gui.py").write_text("# app")

    found = inst.find_existing([root])

    assert found.layout == "source-folder" and found.data_dir == str(root) and found.has_program


def test_an_installed_program_with_no_data_is_still_an_existing_installation(tmp_path):
    root = tmp_path / "BarBell"
    root.mkdir()
    (root / "BarBell.exe").write_bytes(b"x")

    found = inst.find_existing([root])

    assert found is not None and found.layout == "program-only" and not found.has_data


def test_nothing_found_for_missing_empty_or_unrelated_folders(tmp_path):
    (tmp_path / "empty").mkdir()
    (tmp_path / "other").mkdir()
    (tmp_path / "other" / "notes.txt").write_text("hi")
    assert inst.find_existing([tmp_path / "nope", tmp_path / "empty", tmp_path / "other", "", None]) is None


def test_candidates_are_tried_in_order(tmp_path):
    first, second = make_data(tmp_path / "a"), make_data(tmp_path / "b")
    assert inst.find_existing([second, first]).root == str(second)
    assert inst.find_existing([tmp_path / "missing", first, second]).root == str(first)


# --- backup before anything changes --------------------------------------------------------------

def test_backup_of_a_healthy_install_is_a_verified_set_with_database_and_counters(tmp_path):
    data = make_data(tmp_path / "BarBell" / "data", jamaica_counter=40)
    existing = inst.find_existing([tmp_path / "BarBell"])

    result = inst.backup_existing(existing, tmp_path / "bk", now=NOW)

    assert result["ok"] and result["verified_backup"] and result["raw_copy"] is None
    folder = Path(result["verified_backup"])
    assert folder.name.endswith("_pre-install")
    manifest = verify_backup(folder)
    assert manifest["reason"] == REASON_PRE_INSTALL
    assert manifest["counters"] == {"barbados": 12, "jamaica": 40}
    assert sscc_set(folder / "barbell.db") == sscc_set(data / "barbell.db")


def test_the_original_data_is_untouched_by_the_backup(tmp_path):
    data = make_data(tmp_path / "BarBell" / "data")
    before = {p.name: p.read_bytes() for p in data.iterdir()}
    inst.backup_existing(inst.find_existing([tmp_path / "BarBell"]), tmp_path / "bk", now=NOW)
    assert {p.name: p.read_bytes() for p in data.iterdir()} == before


def test_a_manual_copy_with_relative_settings_paths_is_backed_up_from_the_right_place(tmp_path):
    root = tmp_path / "manual"
    make_data(root)
    save_settings(Settings(gs1_company_prefix=PREFIX, local_db_file="barbell.db"), root / "settings.json")

    result = inst.backup_existing(inst.find_existing([root]), tmp_path / "bk", now=NOW)

    assert sscc_set(Path(result["verified_backup"]) / "barbell.db") == serial_set(None, (10, 11, 12))


def test_pre_install_backups_are_never_pruned(tmp_path):
    data = make_data(tmp_path / "BarBell" / "data")
    existing = inst.find_existing([tmp_path / "BarBell"])
    first = inst.backup_existing(existing, tmp_path / "bk", now=NOW)["verified_backup"]
    # a lot of ordinary rolling backups afterwards, with a tiny keep limit
    settings = Settings(
        local_db_file=str(data / "barbell.db"), sscc_state_file=str(data / "sscc_state.json"),
        jamaica_sscc_state_file=str(data / "x.json"), audit_log_file=str(data / "gtin_audit_log.jsonl"),
        backup_keep_count=1,
    )
    for i in range(4):
        _atomic_write_last_serial(data / "sscc_state.json", 100 + i)
        create_backup(settings, tmp_path / "bk", now=NOW + datetime.timedelta(minutes=i + 1), settings_file=data / "settings.json")

    assert Path(first).exists()


def test_a_damaged_database_gets_a_raw_copy_and_is_reported_as_not_restorable(tmp_path):
    data = make_data(tmp_path / "BarBell" / "data")
    raw = bytearray((data / "barbell.db").read_bytes())
    for i in range(100, len(raw), 4096):
        raw[i:i + 64] = b"\xff" * 64
    (data / "barbell.db").write_bytes(bytes(raw))

    result = inst.backup_existing(inst.find_existing([tmp_path / "BarBell"]), tmp_path / "bk", now=NOW)

    assert result["ok"] is True  # the files ARE safely kept...
    assert result["verified_backup"] is None  # ...but there is nothing to restore FROM
    copy = Path(result["raw_copy"])
    assert (copy / "barbell.db").read_bytes() == bytes(raw)  # exact, damaged, evidence
    assert (copy / "sscc_state.json").is_file() and (copy / "README.txt").is_file()
    assert "cannot be restored" in result["message"]
    assert list_backups(tmp_path / "bk") == []  # a damaged backup never masquerades as a good one


def test_no_data_means_nothing_to_back_up_and_no_error(tmp_path):
    root = tmp_path / "BarBell"
    root.mkdir()
    (root / "BarBell.exe").write_bytes(b"x")
    result = inst.backup_existing(inst.find_existing([root]), tmp_path / "bk", now=NOW)
    assert result["ok"] and result["verified_backup"] is None and result["raw_copy"] is None


# --- what is about to be restored? -----------------------------------------------------------------------

def test_inspecting_a_backup_folder_summarises_it(tmp_path):
    make_data(tmp_path / "BarBell" / "data")
    folder = inst.backup_existing(inst.find_existing([tmp_path / "BarBell"]), tmp_path / "bk", now=NOW)["verified_backup"]

    info = inst.inspect_source(folder)

    assert info["ok"] and info["kind"] == "backup" and info["distinct_ssccs"] == 3
    assert info["counters"]["barbados"] == 12 and info["created_at"].startswith("2026-11-05")


def test_inspecting_a_database_file_summarises_it(tmp_path):
    data = make_data(tmp_path / "d")
    info = inst.inspect_source(data / "barbell.db")
    assert info["ok"] and info["kind"] == "database" and info["distinct_ssccs"] == 3 and info["label_rows"] == 3
    assert info["newest_label_at"]


def _missing_file(folder: Path) -> Path:
    return folder / "missing.db"


def _junk_file(folder: Path) -> Path:
    path = folder / "junk.db"
    path.write_bytes(b"this is not a database")
    return path


def _database_that_is_not_barbells(folder: Path) -> Path:
    path = folder / "other.db"
    conn = sqlite3.connect(str(path))
    conn.execute("CREATE TABLE t (x)")
    conn.commit()
    conn.close()
    return path


def _folder_that_is_not_a_backup(folder: Path) -> Path:
    path = folder / "notabackup"
    path.mkdir()
    return path


@pytest.mark.parametrize(
    "make_bad, expected",
    [
        (_missing_file, "does not exist"),
        (_junk_file, "integrity"),
        (_database_that_is_not_barbells, "not a BarBell one"),
        (_folder_that_is_not_a_backup, "isn't a BarBell backup"),
    ],
)
def test_bad_sources_are_refused_with_a_reason(tmp_path, make_bad, expected):
    info = inst.inspect_source(make_bad(tmp_path))
    assert info["ok"] is False and expected in info["error"]


# --- start blank -----------------------------------------------------------------------------------------------

def test_blank_moves_the_old_database_aside_and_leaves_every_counter_alone(tmp_path):
    data = make_data(tmp_path / "data", counter=12, jamaica_counter=40)
    old_bytes = (data / "barbell.db").read_bytes()

    result = inst.apply_data_choice(data, inst.MODE_BLANK, None, tmp_path / "bk", now=NOW)

    assert result["ok"] and not (data / "barbell.db").exists()
    kept = Path(result["old_database_kept_as"])
    assert kept.read_bytes() == old_bytes  # moved, never deleted
    assert counter(data) == 12 and counter(data, "sscc_state_jamaica.json") == 40  # NEVER reset
    assert result["counters_left_unchanged"] == {"barbados": 12, "jamaica": 40}


def test_blank_on_a_first_install_just_works(tmp_path):
    data = tmp_path / "fresh" / "data"
    result = inst.apply_data_choice(data, inst.MODE_BLANK, None, tmp_path / "bk", now=NOW)
    assert result["ok"] and result["old_database_kept_as"] is None and data.is_dir()


# --- restore from the installer's backup -----------------------------------------------------------------------------

def test_restore_from_backup_brings_the_old_data_back_and_never_lowers_a_counter(tmp_path):
    data = make_data(tmp_path / "BarBell" / "data", serials=(10, 11, 12), counter=12)
    backup = inst.backup_existing(inst.find_existing([tmp_path / "BarBell"]), tmp_path / "bk", now=NOW)["verified_backup"]
    # more is issued, then the data is lost / replaced by a blank
    record_generation_run(label_rows([13, 14]), units_per_package=12000, labels_per_package=1, test_mode=False, db_path=data / "barbell.db")
    _atomic_write_last_serial(data / "sscc_state.json", 14)
    inst.apply_data_choice(data, inst.MODE_BLANK, None, tmp_path / "bk", now=NOW)

    result = inst.apply_data_choice(data, inst.MODE_RESTORE_BACKUP, backup, tmp_path / "bk", now=NOW)

    assert result["ok"]
    assert sscc_set(data / "barbell.db") == serial_set(None, (10, 11, 12))
    assert counter(data) == 14  # backup said 12, but 13 and 14 were issued since: never go back


def test_restore_on_a_brand_new_machine_takes_settings_and_audit_from_the_backup(tmp_path):
    make_data(tmp_path / "old" / "data", counter=12, jamaica_counter=40)
    backup = inst.backup_existing(inst.find_existing([tmp_path / "old"]), tmp_path / "bk", now=NOW)["verified_backup"]
    new_data = tmp_path / "new" / "data"

    result = inst.apply_data_choice(new_data, inst.MODE_RESTORE_BACKUP, backup, tmp_path / "bk2", now=NOW)

    assert result["ok"] and result["safety_backup"] is None  # nothing existed to protect
    assert sscc_set(new_data / "barbell.db") == serial_set(None, (10, 11, 12))
    assert counter(new_data) == 12 and counter(new_data, "sscc_state_jamaica.json") == 40
    assert json.loads((new_data / "settings.json").read_text())["gs1_company_prefix"] == PREFIX
    assert (new_data / "gtin_audit_log.jsonl").is_file()
    assert list_backups(tmp_path / "bk2") == []  # no pointless 'safety' backup of an empty machine


def test_restore_does_not_overwrite_the_settings_already_on_the_machine(tmp_path):
    make_data(tmp_path / "old" / "data")
    backup = inst.backup_existing(inst.find_existing([tmp_path / "old"]), tmp_path / "bk", now=NOW)["verified_backup"]
    target = make_data(tmp_path / "new" / "data", serials=(99,), counter=99)
    save_settings(Settings(gs1_company_prefix=PREFIX, output_dir="D:/mine"), target / "settings.json")

    inst.apply_data_choice(target, inst.MODE_RESTORE_BACKUP, backup, tmp_path / "bk2", now=NOW)

    assert json.loads((target / "settings.json").read_text())["output_dir"] == "D:/mine"
    assert counter(target) == 99  # the machine's counter was already ahead
    assert len(list_backups(tmp_path / "bk2")) == 1  # and what was there was safety-backed-up first


def test_a_damaged_backup_is_refused_and_nothing_changes(tmp_path):
    make_data(tmp_path / "old" / "data")
    backup = Path(inst.backup_existing(inst.find_existing([tmp_path / "old"]), tmp_path / "bk", now=NOW)["verified_backup"])
    target = make_data(tmp_path / "new" / "data", serials=(99,), counter=99)
    before = (target / "barbell.db").read_bytes()
    (backup / "barbell.db").write_bytes(b"tampered")

    result = inst.apply_data_choice(target, inst.MODE_RESTORE_BACKUP, backup, tmp_path / "bk2", now=NOW)

    assert result["ok"] is False and result["error"]
    assert (target / "barbell.db").read_bytes() == before and counter(target) == 99


# --- restore from a database file the user picks --------------------------------------------------------------------------

def test_restore_from_a_picked_database_rebuilds_the_counters_from_it(tmp_path):
    source = make_data(tmp_path / "usb")  # a copied-off barbell.db: just the file is used
    target = tmp_path / "BarBell" / "data"  # new machine, nothing there

    result = inst.apply_data_choice(target, inst.MODE_RESTORE_DB, source / "barbell.db", tmp_path / "bk", now=NOW)

    assert result["ok"]
    assert sscc_set(target / "barbell.db") == serial_set(None, (10, 11, 12))
    assert counter(target) == 12  # highest serial found in the database
    assert result["counters_set"]["barbados"] == [None, 12]
    assert any("CLC's GS1 Company Prefix" in w for w in result["warnings"])  # no settings on this PC yet


def test_a_picked_database_never_lowers_a_counter_that_is_already_ahead(tmp_path):
    source = make_data(tmp_path / "usb", serials=(10, 11, 12))
    target = make_data(tmp_path / "BarBell" / "data", serials=(10, 11, 12, 13, 14, 15), counter=15)

    result = inst.apply_data_choice(target, inst.MODE_RESTORE_DB, source / "barbell.db", tmp_path / "bk", now=NOW)

    assert result["ok"] and counter(target) == 15
    assert sscc_set(target / "barbell.db") == serial_set(None, (10, 11, 12))
    assert Path(result["old_database_kept_as"]).exists()  # the database it replaced is still there


def test_each_plants_counter_is_rebuilt_from_its_own_extension_digit(tmp_path):
    source = tmp_path / "usb"
    make_data(source, serials=(10, 11), counter=11)
    record_generation_run(label_rows([40, 41, 42], ext="1"), units_per_package=12000, labels_per_package=1, test_mode=False, db_path=source / "barbell.db")
    target = tmp_path / "BarBell" / "data"

    inst.apply_data_choice(target, inst.MODE_RESTORE_DB, source / "barbell.db", tmp_path / "bk", now=NOW)

    assert counter(target) == 11 and counter(target, "sscc_state_jamaica.json") == 42


def test_a_damaged_picked_file_is_refused_and_the_existing_database_is_left_alone(tmp_path):
    target = make_data(tmp_path / "BarBell" / "data")
    before = (target / "barbell.db").read_bytes()
    bad = tmp_path / "bad.db"
    bad.write_bytes(b"not a database at all")

    result = inst.apply_data_choice(target, inst.MODE_RESTORE_DB, bad, tmp_path / "bk", now=NOW)

    assert result["ok"] is False and "integrity" in result["error"]
    assert (target / "barbell.db").read_bytes() == before


def test_an_unknown_choice_is_an_error_not_a_crash(tmp_path):
    result = inst.apply_data_choice(tmp_path / "d", "something-else", None, tmp_path / "bk")
    assert result["ok"] is False


# --- the command-line helper the wizard actually calls ---------------------------------------------------------------------------

def run_helper(tmp_path, *args):
    out = tmp_path / f"out-{len(list(tmp_path.glob('out-*.json')))}.json"
    code = helper_main([*args, "--out", str(out)])
    return code, json.loads(out.read_text())


def test_helper_detect_backup_inspect_apply_round_trip(tmp_path):
    root = tmp_path / "BarBell"
    make_data(root / "data")
    (root / "BarBell.exe").write_bytes(b"x")

    code, found = run_helper(tmp_path, "detect", "--candidate", str(tmp_path / "nowhere"), "--candidate", str(root))
    assert code == 0 and found["found"] and found["has_data"] and found["install"]["layout"] == "installed"

    code, backup = run_helper(tmp_path, "backup", "--existing-root", str(root), "--backup-root", str(tmp_path / "bk"))
    assert code == 0 and backup["verified_backup"]

    code, info = run_helper(tmp_path, "inspect", "--source", backup["verified_backup"])
    assert code == 0 and info["kind"] == "backup"

    target = tmp_path / "new" / "data"
    code, applied = run_helper(
        tmp_path, "apply", "--data-dir", str(target), "--mode", "restore-backup",
        "--source", backup["verified_backup"], "--backup-root", str(tmp_path / "bk"),
    )
    assert code == 0 and applied["ok"] and (target / "barbell.db").is_file()


def test_helper_reports_failure_with_exit_code_1_and_an_answer_file(tmp_path):
    code, info = run_helper(tmp_path, "inspect", "--source", str(tmp_path / "nothing-here.db"))
    assert code == 1 and info["ok"] is False and info["error"]


def test_helper_detect_with_no_install_is_a_clean_negative(tmp_path):
    code, found = run_helper(tmp_path, "detect", "--candidate", str(tmp_path / "nothing"))
    assert code == 0 and found["found"] is False and found["install"] is None
