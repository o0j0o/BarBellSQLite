import datetime
import json
import sqlite3

import pytest

from src.backup import (
    BackupError,
    REASON_EXIT,
    REASON_MANUAL,
    REASON_PRE_RESTORE,
    create_backup,
    list_backups,
    restore_backup,
    summarize_restore,
    verify_backup,
)
from src.db.local_store import fetch_label_history, record_generation_run
from src.labels import LabelRow
from src.settings import Settings
from src.sscc import _atomic_write_last_serial, build_sscc

PREFIX = "08600157112"


def make_settings(tmp_path, **overrides):
    values = dict(
        gs1_company_prefix=PREFIX, sscc_extension_digit="0",
        jamaica_gs1_company_prefix=PREFIX, jamaica_sscc_extension_digit="1",
        local_db_file=str(tmp_path / "live" / "barbell.db"),
        sscc_state_file=str(tmp_path / "live" / "sscc_state.json"),
        jamaica_sscc_state_file=str(tmp_path / "live" / "sscc_state_jamaica.json"),
        audit_log_file=str(tmp_path / "live" / "gtin_audit_log.jsonl"),
        backup_keep_count=10,
    )
    values.update(overrides)
    return Settings(**values)


def cartons(serials, ext="0"):
    return [
        LabelRow(
            job_number="122984", packing_slip_number="100495", customer_number="J00005",
            customer_name="JWN", product_no="47388", item_number="233458", item_description="desc",
            quantity=1000, batch="12298447388", production_date="260323",
            sscc=build_sscc(PREFIX, ext, serial), gtin="00051096184921",
            package_index=i, label_copy_index=1,
        )
        for i, serial in enumerate(serials, start=1)
    ]


def seed(settings, serials=(1, 2, 3), counter=3, ext="0"):
    record_generation_run(
        cartons(serials, ext), units_per_package=1000, labels_per_package=1, test_mode=False,
        db_path=settings.local_db_file,
    )
    state = settings.sscc_state_file if ext == "0" else settings.jamaica_sscc_state_file
    _atomic_write_last_serial(__import__("pathlib").Path(state), counter)


def add_settings_and_audit(settings, tmp_path):
    settings_file = tmp_path / "live" / "settings.json"
    settings_file.write_text(json.dumps({"x": 1}), encoding="utf-8")
    __import__("pathlib").Path(settings.audit_log_file).write_text('{"a":1}\n', encoding="utf-8")
    return settings_file


@pytest.fixture
def env(tmp_path):
    settings = make_settings(tmp_path)
    (tmp_path / "live").mkdir()
    seed(settings)
    settings_file = add_settings_and_audit(settings, tmp_path)
    return settings, settings_file, tmp_path / "backups", tmp_path


def at(minute):
    return datetime.datetime(2026, 11, 4, 12, minute, 0)


# --- creating a backup ----------------------------------------------------------------

def test_backup_holds_the_whole_set_with_a_verifiable_manifest(env):
    settings, settings_file, dest, _ = env

    result = create_backup(settings, dest, REASON_MANUAL, settings_file, now=at(0))

    assert not result.skipped and result.path.parent == dest
    names = {p.name for p in result.path.iterdir()}
    assert names == {"barbell.db", "sscc_state.json", "settings.json", "gtin_audit_log.jsonl", "manifest.json"}
    manifest = verify_backup(result.path)  # raises if anything doesn't match
    assert manifest["counters"] == {"barbados": 3, "jamaica": None}
    assert manifest["distinct_ssccs"] == 3
    assert manifest["reason"] == REASON_MANUAL


def test_backed_up_database_matches_the_live_one(env):
    settings, settings_file, dest, _ = env
    result = create_backup(settings, dest, settings_file=settings_file, now=at(0))

    live = [(r.sscc, r.quantity) for r in fetch_label_history(settings.local_db_file)]
    copy = [(r.sscc, r.quantity) for r in fetch_label_history(result.path / "barbell.db")]
    assert copy == live


def test_backup_works_while_another_connection_has_the_database_open(env):
    settings, settings_file, dest, _ = env
    other = sqlite3.connect(settings.local_db_file)
    other.execute("BEGIN")
    other.execute("SELECT COUNT(*) FROM labels").fetchone()
    try:
        result = create_backup(settings, dest, settings_file=settings_file, now=at(0))
    finally:
        other.close()
    assert verify_backup(result.path)


def test_nothing_to_back_up_is_reported_not_crashed(tmp_path):
    settings = make_settings(tmp_path)
    result = create_backup(settings, tmp_path / "backups", settings_file=tmp_path / "none.json")
    assert result.skipped and result.path is None


def test_unchanged_data_is_not_backed_up_again(env):
    settings, settings_file, dest, _ = env
    first = create_backup(settings, dest, settings_file=settings_file, now=at(0))
    second = create_backup(settings, dest, settings_file=settings_file, now=at(1))

    assert second.skipped and "Nothing has changed" in second.message
    assert list_backups(dest) == [first.path]


def test_a_change_to_the_database_or_a_counter_makes_a_new_backup(env):
    settings, settings_file, dest, _ = env
    create_backup(settings, dest, settings_file=settings_file, now=at(0))
    _atomic_write_last_serial(__import__("pathlib").Path(settings.sscc_state_file), 4)
    counter_change = create_backup(settings, dest, settings_file=settings_file, now=at(1))
    seed(settings, serials=(4,), counter=4)
    db_change = create_backup(settings, dest, settings_file=settings_file, now=at(2))

    assert not counter_change.skipped and not db_change.skipped
    assert len(list_backups(dest)) == 3


def test_skip_can_be_turned_off(env):
    settings, settings_file, dest, _ = env
    create_backup(settings, dest, settings_file=settings_file, now=at(0))
    again = create_backup(settings, dest, settings_file=settings_file, skip_if_unchanged=False, now=at(1))
    assert not again.skipped


# --- retention --------------------------------------------------------------------------

def make_changes(settings, settings_file, dest, count, start_minute=0):
    paths = []
    for i in range(count):
        _atomic_write_last_serial(__import__("pathlib").Path(settings.sscc_state_file), 100 + start_minute + i)
        paths.append(create_backup(settings, dest, settings_file=settings_file, now=at(start_minute + i)).path)
    return paths


def test_only_the_newest_n_backups_are_kept(env):
    settings, settings_file, dest, _ = env
    settings.backup_keep_count = 3

    paths = make_changes(settings, settings_file, dest, 5)

    assert list_backups(dest) == paths[2:]  # the 3 newest survive, the 2 oldest are gone


def test_pruning_never_touches_folders_it_did_not_make(env):
    settings, settings_file, dest, _ = env
    settings.backup_keep_count = 1
    dest.mkdir()
    (dest / "my_family_photos").mkdir()
    (dest / "my_family_photos" / "a.jpg").write_text("x")
    (dest / "barbell_backup_20200101_000000").mkdir()  # right name, but no manifest -> not ours
    (dest / "notes.txt").write_text("keep me")

    make_changes(settings, settings_file, dest, 3)

    assert (dest / "my_family_photos" / "a.jpg").exists()
    assert (dest / "barbell_backup_20200101_000000").exists()
    assert (dest / "notes.txt").exists()
    assert len(list_backups(dest)) == 1


def test_a_failed_backup_leaves_no_partial_folder_and_prunes_nothing(env):
    settings, settings_file, dest, tmp_path = env
    settings.backup_keep_count = 2
    good = make_changes(settings, settings_file, dest, 2)

    # corrupt the live database so the new backup fails its integrity check
    live = tmp_path / "live" / "barbell.db"
    data = bytearray(live.read_bytes())
    for i in range(100, len(data), 4096):
        data[i:i + 64] = b"\xff" * 64
    live.write_bytes(bytes(data))
    _atomic_write_last_serial(__import__("pathlib").Path(settings.sscc_state_file), 999)

    with pytest.raises(BackupError):
        create_backup(settings, dest, settings_file=settings_file, now=at(30))

    assert list_backups(dest) == good  # the good ones are all still there
    assert sorted(p.name for p in dest.iterdir()) == sorted(p.name for p in good)  # no half-made folder left


def test_unusable_backup_folder_is_a_clear_error(env, tmp_path):
    settings, settings_file, _, _ = env
    blocker = tmp_path / "iam_a_file"
    blocker.write_text("x")
    with pytest.raises(BackupError, match="Can't use the backup folder"):
        create_backup(settings, blocker / "sub", settings_file=settings_file)


# --- verify -------------------------------------------------------------------------------

def test_verify_rejects_a_folder_that_is_not_a_backup(tmp_path):
    (tmp_path / "x").mkdir()
    with pytest.raises(BackupError, match="isn't a BarBell backup"):
        verify_backup(tmp_path / "x")


def test_verify_catches_a_tampered_or_missing_file(env):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path

    (backup / "sscc_state.json").write_text('{"last_serial": 0}')
    with pytest.raises(BackupError, match="damaged"):
        verify_backup(backup)

    (backup / "sscc_state.json").unlink()
    with pytest.raises(BackupError, match="incomplete"):
        verify_backup(backup)


# --- restore ----------------------------------------------------------------------------------

def test_restore_brings_back_the_old_database_and_keeps_the_newer_counter(env):
    settings, settings_file, dest, tmp_path = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path  # 3 cartons, counter 3
    seed(settings, serials=(4, 5), counter=5)  # later: 2 more cartons issued, counter 5

    result = restore_backup(backup, settings, dest, settings_file)

    restored = {r.sscc for r in fetch_label_history(settings.local_db_file)}
    assert restored == {build_sscc(PREFIX, "0", n) for n in (1, 2, 3)}
    # the counter must NOT go back to 3 - serials 4 and 5 were already issued
    assert json.loads((tmp_path / "live" / "sscc_state.json").read_text())["last_serial"] == 5
    assert result.counters_after["barbados"] == 5
    assert result.safety_backup is not None


def test_restore_takes_a_safety_backup_of_the_state_it_replaces(env):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    seed(settings, serials=(4,), counter=4)

    result = restore_backup(backup, settings, dest, settings_file)

    manifest = verify_backup(result.safety_backup)
    assert manifest["reason"] == REASON_PRE_RESTORE
    safety_ssccs = {r.sscc for r in fetch_label_history(result.safety_backup / "barbell.db")}
    assert build_sscc(PREFIX, "0", 4) in safety_ssccs  # the carton the restore removed is recoverable


def test_pre_restore_backups_are_not_pruned_by_normal_rotation(env):
    settings, settings_file, dest, _ = env
    settings.backup_keep_count = 1
    first = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    seed(settings, serials=(4,), counter=4)
    safety = restore_backup(first, settings, dest, settings_file).safety_backup
    make_changes(settings, settings_file, dest, 3, start_minute=10)

    assert safety.exists()


def test_restore_raises_a_missing_counter_from_the_backup(env, tmp_path):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    (tmp_path / "live" / "sscc_state.json").unlink()  # counter file lost

    result = restore_backup(backup, settings, dest, settings_file)

    assert json.loads((tmp_path / "live" / "sscc_state.json").read_text())["last_serial"] == 3
    assert result.counters_raised["barbados"] == (None, 3)


def test_restore_raises_a_counter_that_is_behind_the_restored_database(env, tmp_path):
    settings, settings_file, dest, _ = env
    # a backup whose counter file lags its own database (serials up to 9 exist, counter says 3)
    seed(settings, serials=(7, 8, 9), counter=3)
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    _atomic_write_last_serial(__import__("pathlib").Path(settings.sscc_state_file), 3)

    result = restore_backup(backup, settings, dest, settings_file)

    assert json.loads((tmp_path / "live" / "sscc_state.json").read_text())["last_serial"] == 9
    assert result.counters_raised["barbados"] == (3, 9)


def test_each_plants_counter_is_handled_separately(env, tmp_path):
    settings, settings_file, dest, _ = env
    seed(settings, serials=(1, 2), counter=2, ext="1")  # Jamaica
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    (tmp_path / "live" / "sscc_state_jamaica.json").unlink()

    restore_backup(backup, settings, dest, settings_file)

    assert json.loads((tmp_path / "live" / "sscc_state.json").read_text())["last_serial"] == 3
    assert json.loads((tmp_path / "live" / "sscc_state_jamaica.json").read_text())["last_serial"] == 2


def test_a_damaged_backup_is_refused_and_nothing_is_changed(env, tmp_path):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    seed(settings, serials=(4,), counter=4)
    before_db = (tmp_path / "live" / "barbell.db").read_bytes()
    before_counter = (tmp_path / "live" / "sscc_state.json").read_text()
    (backup / "barbell.db").write_bytes(b"not a database")

    with pytest.raises(BackupError):
        restore_backup(backup, settings, dest, settings_file)

    assert (tmp_path / "live" / "barbell.db").read_bytes() == before_db
    assert (tmp_path / "live" / "sscc_state.json").read_text() == before_counter
    assert [p for p in list_backups(dest) if "pre-restore" in p.name] == []  # not even a safety backup


def test_restore_does_not_overwrite_settings_or_the_audit_log(env, tmp_path):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    settings_file.write_text(json.dumps({"changed": True}), encoding="utf-8")
    audit = __import__("pathlib").Path(settings.audit_log_file)
    audit.write_text('{"newer":1}\n{"newer":2}\n', encoding="utf-8")

    restore_backup(backup, settings, dest, settings_file)

    assert json.loads(settings_file.read_text()) == {"changed": True}
    assert audit.read_text() == '{"newer":1}\n{"newer":2}\n'


def test_restore_works_on_a_fresh_machine_with_no_existing_files(env, tmp_path):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    fresh = make_settings(tmp_path / "newpc")  # nothing exists there yet

    result = restore_backup(backup, fresh, tmp_path / "newpc" / "backups", tmp_path / "newpc" / "settings.json")

    assert {r.sscc for r in fetch_label_history(fresh.local_db_file)} == {
        build_sscc(PREFIX, "0", n) for n in (1, 2, 3)
    }
    assert result.safety_backup is None  # nothing existed to protect
    assert json.loads((tmp_path / "newpc" / "live" / "sscc_state.json").read_text())["last_serial"] == 3


def test_summary_tells_the_user_what_a_restore_would_lose(env):
    settings, settings_file, dest, _ = env
    backup = create_backup(settings, dest, settings_file=settings_file, now=at(0)).path
    seed(settings, serials=(4, 5), counter=5)

    summary = summarize_restore(backup, settings)

    assert summary.cartons_and_pallets_in_backup == 3
    assert summary.only_in_current == 2
    assert summary.counters["barbados"] == {"backup": 3, "current": 5}
    assert summary.created_at == "2026-11-04T12:00:00"


def test_exit_and_manual_reasons_are_recorded(env):
    settings, settings_file, dest, _ = env
    a = create_backup(settings, dest, REASON_EXIT, settings_file, now=at(0)).path
    assert verify_backup(a)["reason"] == REASON_EXIT
