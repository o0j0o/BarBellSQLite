"""
Setup's Backup and Restore section. Setup is its own Tk window (a separate
program, setup_gui.py), and the test suite already holds one Tk root for the
main window - so each scenario runs in a fresh Python subprocess against a
TEMP settings file and prints a JSON result. The real settings.json is never
touched.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

DRIVER = r'''
import functools, json, sys
from pathlib import Path

root, scenario, tmp = sys.argv[1], sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, root)

import tkinter.filedialog as fd
import tkinter.messagebox as mb

log = {"info": [], "error": [], "ask": []}
answer = {"ask": True}
mb.showinfo = lambda t, m, **k: log["info"].append(m)
mb.showerror = lambda t, m, **k: log["error"].append(m)
mb.askyesno = lambda t, m, **k: (log["ask"].append(t), answer["ask"])[1]

import setup_gui
from src import backup
from src import settings as sm
from src.db.local_store import fetch_label_history, record_generation_run
from src.labels import LabelRow
from src.settings import Settings
from src.setup_access import SetupAccessLevel
from src.sscc import _atomic_write_last_serial, build_sscc

PREFIX = "08600157112"
live = tmp / "live"
live.mkdir()
settings_path = tmp / "settings.json"
base = Settings(
    gs1_company_prefix=PREFIX, output_dir=str(tmp / "out"),
    local_db_file=str(live / "barbell.db"), sscc_state_file=str(live / "sscc_state.json"),
    jamaica_sscc_state_file=str(live / "sscc_state_jamaica.json"), audit_log_file=str(live / "audit.jsonl"),
)
sm.save_settings(base, settings_path)
setup_gui.load_settings = lambda path=settings_path: sm.load_settings(settings_path)
setup_gui.save_settings = lambda s: sm.save_settings(s, settings_path)
setup_gui.create_backup = functools.partial(backup.create_backup, settings_file=settings_path)
setup_gui.restore_backup = functools.partial(backup.restore_backup, settings_file=settings_path)


def carton_rows(serials):
    return [
        LabelRow(
            job_number="122984", packing_slip_number="100495", customer_number="J00005",
            customer_name="JWN", product_no="47388", item_number="233458", item_description="d",
            quantity=1000, batch="12298447388", production_date="260323",
            sscc=build_sscc(PREFIX, "0", n), gtin="00051096184921", package_index=i, label_copy_index=1,
        )
        for i, n in enumerate(serials, start=1)
    ]


def issue(serials, counter):
    record_generation_run(carton_rows(serials), units_per_package=1000, labels_per_package=1,
                          test_mode=False, db_path=base.local_db_file)
    _atomic_write_last_serial(Path(base.sscc_state_file), counter)


level = SetupAccessLevel.Admin if scenario.startswith("admin") else SetupAccessLevel.Standard
gui = setup_gui.SetupGUI(level)
gui.update()
out = {"restore_state": str(gui.restore_button.cget("state")), "is_admin": gui.is_admin}
backups = tmp / "bk"

if scenario.endswith("save_dir"):
    gui.backup_dir_var.set(str(backups))
    gui._save()
    out["saved"] = json.loads(settings_path.read_text())["backup_dir"]
    out["folder_made"] = backups.is_dir()

elif scenario.endswith("onedrive_no") or scenario.endswith("onedrive_yes"):
    answer["ask"] = scenario.endswith("yes")
    gui.backup_dir_var.set(str(tmp / "OneDrive - Co" / "bk"))
    gui._save()
    out["saved"] = json.loads(settings_path.read_text())["backup_dir"]

elif scenario.endswith("backup_now_no_dir"):
    gui._backup_now()

elif scenario.endswith("backup_now"):
    issue([1, 2, 3], 3)
    gui.backup_dir_var.set(str(backups))
    gui._backup_now()
    gui._backup_now()
    out["folders"] = sorted(p.name for p in backups.iterdir())

elif scenario.endswith("restore") or scenario.endswith("restore_bad_folder"):
    issue([1, 2, 3], 3)
    gui.backup_dir_var.set(str(backups))
    made = backup.create_backup(Settings(**{**base.__dict__}), backups, settings_file=settings_path).path
    issue([4], 4)
    empty = tmp / "not_a_backup"
    empty.mkdir()
    chosen = empty if scenario.endswith("bad_folder") else made
    fd.askdirectory = lambda **k: str(chosen)
    gui._restore_from_backup()
    out["ssccs"] = sorted(r.sscc[-6:] for r in fetch_label_history(base.local_db_file))
    out["counter"] = json.loads(Path(base.sscc_state_file).read_text())["last_serial"]
    out["safety"] = sorted(p.name for p in backups.iterdir() if "pre-restore" in p.name)

out["log"] = log
print("RESULT " + json.dumps(out))
'''


def run(scenario, tmp_path):
    proc = subprocess.run(
        [sys.executable, "-c", DRIVER, str(ROOT), scenario, str(tmp_path)],
        capture_output=True, text=True, timeout=120,
    )
    lines = [l for l in proc.stdout.splitlines() if l.startswith("RESULT ")]
    assert lines, f"driver failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    return json.loads(lines[-1][len("RESULT "):])


def test_standard_setup_cannot_restore(tmp_path):
    result = run("standard_state", tmp_path)
    assert result["is_admin"] is False
    assert result["restore_state"] == "disabled"


def test_admin_setup_can_restore(tmp_path):
    result = run("admin_state", tmp_path)
    assert result["is_admin"] is True
    assert result["restore_state"] == "normal"


def test_backup_directory_is_saved_with_the_other_settings_and_created(tmp_path):
    result = run("standard_save_dir", tmp_path)
    assert result["saved"] == str(tmp_path / "bk")
    assert result["folder_made"] is True


def test_a_backup_directory_inside_onedrive_asks_first_and_no_keeps_the_old_value(tmp_path):
    result = run("standard_onedrive_no", tmp_path)
    assert result["saved"] == ""  # declined -> not saved
    assert result["log"]["ask"] == ["Backup directory is in OneDrive"]


def test_a_backup_directory_inside_onedrive_can_still_be_chosen_deliberately(tmp_path):
    result = run("standard_onedrive_yes", tmp_path)
    assert result["saved"].endswith("bk") and "OneDrive" in result["saved"]


def test_back_up_now_without_a_directory_asks_for_one(tmp_path):
    result = run("standard_backup_now_no_dir", tmp_path)
    assert result["log"]["info"] == ["Choose a backup directory first."]


def test_back_up_now_works_for_standard_setup_and_skips_when_unchanged(tmp_path):
    result = run("standard_backup_now", tmp_path)
    assert len(result["folders"]) == 1
    assert result["log"]["info"][0].startswith("Backed up to")
    assert "Nothing has changed" in result["log"]["info"][1]


def test_admin_restore_round_trip_keeps_the_counter_ahead_and_makes_a_safety_backup(tmp_path):
    result = run("admin_restore", tmp_path)

    from src.sscc import build_sscc

    # database is back to the 3 cartons that existed at backup time (carton 4 is gone from history)
    assert result["ssccs"] == sorted(build_sscc("08600157112", "0", n)[-6:] for n in (1, 2, 3))
    assert result["counter"] == 4  # ...but carton 4 WAS issued, so the counter is never moved back to 3
    assert len(result["safety"]) == 1  # the pre-restore safety backup (holds carton 4)
    assert result["log"]["ask"] == ["Confirm restore"]
    assert any("Restart BarBell" in m for m in result["log"]["info"])
    assert result["log"]["error"] == []


def test_restoring_from_a_folder_that_is_not_a_backup_is_refused_and_changes_nothing(tmp_path):
    result = run("admin_restore_bad_folder", tmp_path)

    assert len(result["ssccs"]) == 4  # all four cartons still there
    assert result["counter"] == 4
    assert result["safety"] == []
    assert len(result["log"]["error"]) == 1 and "isn't a BarBell backup" in result["log"]["error"][0]
