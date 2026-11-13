"""
The label CSVs BarTender Print Station reads: always the same two file names in the Setup "CSV output
directory" (carton_jwn_labels.csv and pallet_jwn_labels.csv). Before a new file is written the one
already there is moved into an `archive` folder with the date and time added to its name, and the
operator is warned (with a Cancel) before anything is issued, logged or replaced.
"""

import csv
import datetime
import os

import pytest

from src import label_files
from src.db.local_store import (
    count_label_history,
    create_pallet,
    describe_labels,
    fetch_label_history,
    record_generation_run,
)
from src.label_files import (
    ArchiveError,
    archive_existing,
    archived_name,
    ensure_archive_folder,
    label_file_name,
    label_file_path,
    write_label_file,
)
from src.labels import LabelRow
from src.sscc import SSCCGenerator, build_sscc

WHEN = datetime.datetime(2026, 11, 13, 14, 30, 52)


def rows_for(job, serials, test=False):
    return [
        LabelRow(
            job_number=job, packing_slip_number="100512", customer_number="J00005", customer_name="JWN",
            product_no="41185", item_number="234412", item_description="Rum", quantity=1000,
            batch=f"{job}41185", production_date="260505",
            sscc=f"TEST-SSCC-{n:05d}" if test else build_sscc("08600157112", "0", n),
            gtin="00636191205407", package_index=i, label_copy_index=1,
        )
        for i, n in enumerate(serials, start=1)
    ]


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- the names ------------------------------------------------------------------------------------

def test_real_labels_use_exactly_the_two_generic_names():
    assert label_file_name("CARTON") == "carton_jwn_labels.csv"
    assert label_file_name("PALLET") == "pallet_jwn_labels.csv"


def test_test_and_demo_runs_never_use_the_real_names():
    assert label_file_name("CARTON", test_mode=True) == "carton_jwn_labels_TEST.csv"
    assert label_file_name("PALLET", test_mode=True) == "pallet_jwn_labels_TEST.csv"
    assert label_file_name("CARTON", demo_mode=True) == "DEMO_carton_jwn_labels.csv"
    assert label_file_name("PALLET", test_mode=True, demo_mode=True) == "DEMO_pallet_jwn_labels_TEST.csv"


def test_the_file_goes_in_the_given_output_directory(tmp_path):
    assert label_file_path(tmp_path / "out", "CARTON") == tmp_path / "out" / "carton_jwn_labels.csv"


def test_unknown_label_type_is_refused():
    with pytest.raises(ValueError):
        label_file_name("BOX")


def test_the_archived_name_is_the_old_name_with_date_and_time_appended():
    assert archived_name("carton_jwn_labels.csv", WHEN) == "carton_jwn_labels_20261113_143052.csv"
    assert archived_name("pallet_jwn_labels.csv", WHEN) == "pallet_jwn_labels_20261113_143052.csv"


# --- the archive folder -----------------------------------------------------------------------------

def test_archive_folder_is_created_when_missing_and_skipped_when_it_exists(tmp_path):
    made = ensure_archive_folder(tmp_path)
    assert made == tmp_path / "archive" and made.is_dir()
    (made / "keep.txt").write_text("x")
    assert ensure_archive_folder(tmp_path) == made  # already there: no error ...
    assert (made / "keep.txt").read_text() == "x"  # ... and nothing in it touched


def test_the_very_first_run_still_leaves_an_archive_folder(tmp_path):
    out, archived = write_label_file(rows_for("100001", [1]), tmp_path / "carton_jwn_labels.csv", WHEN)
    assert archived is None  # nothing to archive on a first run
    assert (tmp_path / "archive").is_dir() and list((tmp_path / "archive").iterdir()) == []


def test_no_current_file_just_writes_the_new_one(tmp_path):
    target = tmp_path / "out" / "carton_jwn_labels.csv"  # even the folder does not exist yet
    out, archived = write_label_file(rows_for("100001", [1, 2]), target, WHEN)
    assert out == target and archived is None
    assert [r["SSCC"] for r in read(target)] == [build_sscc("08600157112", "0", 1), build_sscc("08600157112", "0", 2)]


# --- replacing a file ------------------------------------------------------------------------------

def test_the_old_file_is_archived_with_a_date_time_code_and_the_new_one_takes_its_place(tmp_path):
    target = tmp_path / "carton_jwn_labels.csv"
    write_label_file(rows_for("100001", [1]), target, WHEN)

    out, archived = write_label_file(rows_for("100002", [7, 8]), target, WHEN + datetime.timedelta(hours=1))

    assert archived == tmp_path / "archive" / "carton_jwn_labels_20261113_153052.csv"
    assert [r["JobNumber"] for r in read(archived)] == ["100001"]  # the OLD content, kept whole
    assert [r["JobNumber"] for r in read(target)] == ["100002", "100002"]  # the NEW content under the fixed name
    assert sorted(p.name for p in tmp_path.iterdir()) == ["archive", "carton_jwn_labels.csv"]  # no stray .tmp


def test_two_files_archived_in_the_same_second_never_overwrite_each_other(tmp_path):
    target = tmp_path / "pallet_jwn_labels.csv"
    for job in ("100001", "100002", "100003"):
        write_label_file(rows_for(job, [1]), target, WHEN)  # same timestamp every time
    archived = sorted(p.name for p in (tmp_path / "archive").iterdir())
    assert len(archived) == 2 and len(set(archived)) == 2
    assert all(n.startswith("pallet_jwn_labels_20261113_143052") for n in archived)
    assert [r["JobNumber"] for r in read(target)] == ["100003"]


def test_carton_and_pallet_files_are_archived_separately(tmp_path):
    write_label_file(rows_for("100001", [1]), tmp_path / "carton_jwn_labels.csv", WHEN)
    write_label_file(rows_for("100002", [2]), tmp_path / "pallet_jwn_labels.csv", WHEN)
    write_label_file(rows_for("100003", [3]), tmp_path / "carton_jwn_labels.csv", WHEN)
    assert [p.name for p in (tmp_path / "archive").iterdir()] == ["carton_jwn_labels_20261113_143052.csv"]
    assert [r["JobNumber"] for r in read(tmp_path / "pallet_jwn_labels.csv")] == ["100002"]  # untouched


def test_when_the_old_file_cannot_be_moved_it_is_left_alone_and_nothing_new_is_written(tmp_path, monkeypatch):
    target = tmp_path / "carton_jwn_labels.csv"
    write_label_file(rows_for("100001", [1]), target, WHEN)
    before = target.read_bytes()

    def locked(src, dst):
        raise PermissionError("[WinError 32] being used by another process")

    monkeypatch.setattr(label_files.os, "rename", locked)
    with pytest.raises(ArchiveError) as exc:
        write_label_file(rows_for("100002", [2]), target, WHEN)

    assert "BarTender Print Station" in str(exc.value)
    assert target.read_bytes() == before  # the old file is exactly as it was
    assert sorted(p.name for p in tmp_path.iterdir()) == ["archive", "carton_jwn_labels.csv"]  # no .tmp left over
    assert list((tmp_path / "archive").iterdir()) == []


def test_a_failed_write_keeps_the_old_file_in_place(tmp_path, monkeypatch):
    target = tmp_path / "carton_jwn_labels.csv"
    write_label_file(rows_for("100001", [1]), target, WHEN)
    before = target.read_bytes()

    def broken(rows, out_path):
        raise OSError("disk full")

    monkeypatch.setattr(label_files, "write_flat_csv", broken)
    with pytest.raises(OSError):
        write_label_file(rows_for("100002", [2]), target, WHEN)

    assert target.read_bytes() == before
    assert list((tmp_path / "archive").iterdir()) == []  # nothing was archived either


def test_archive_existing_with_no_file_does_nothing(tmp_path):
    assert archive_existing(tmp_path / "carton_jwn_labels.csv", WHEN) is None
    assert not (tmp_path / "archive").exists()


def test_describe_labels_reports_type_and_test_flag(tmp_path):
    db = tmp_path / "barbell.db"
    record_generation_run(rows_for("100001", [1]), units_per_package=1000, labels_per_package=1, test_mode=False, db_path=db)
    record_generation_run(rows_for("100002", [1], test=True), units_per_package=1000, labels_per_package=1, test_mode=True, db_path=db)
    ids = [r.id for r in fetch_label_history(db)]
    kinds = describe_labels(sorted(ids), db)
    assert sorted(kinds) == [("CARTON", False), ("CARTON", True)]
    with pytest.raises(ValueError):
        describe_labels([9999], db)


# --- Generate Labels (main screen) ------------------------------------------------------------------

class Dialogs:
    """Stands in for the message boxes and records what was asked."""

    def __init__(self, monkeypatch, ok=True):
        self.ok = ok
        self.asked = []  # askokcancel (title, message)
        self.infos = []
        self.errors = []
        monkeypatch.setattr("tkinter.messagebox.askokcancel", self._askokcancel)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: self.infos.append((title, msg)))
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: self.errors.append((title, msg)))

    def _askokcancel(self, title, message, **k):
        self.asked.append((title, message, k))
        return self.ok


@pytest.fixture
def carton_screen(app, tmp_path, monkeypatch):
    """The main screen ready to Generate Labels for real (not Test mode): sample Label Traxx data, a
    temporary history database and SSCC counter, and a temporary output directory."""
    from src.demo_data import DemoConnection
    from src.labels import get_product_info, list_packing_slip_line_items

    state_file = tmp_path / "sscc_state.json"
    SSCCGenerator("08600157112", "0", state_file).initialize(start_at=0)
    for name, value in {
        "demo_mode": False, "local_db_file": str(tmp_path / "barbell.db"),
        "output_dir": str(tmp_path / "output"), "audit_log_file": str(tmp_path / "audit.jsonl"),
        "gs1_company_prefix": "08600157112", "sscc_extension_digit": "0", "sscc_state_file": str(state_file),
    }.items():
        monkeypatch.setattr(app.settings, name, value)
    monkeypatch.setattr(app, "_connect", lambda: DemoConnection())
    monkeypatch.setattr("barbell_gui.winsound.MessageBeep", lambda *_a, **_k: None)
    conn = DemoConnection()
    line_item = list_packing_slip_line_items(conn, "DEMO-PS-5001")[0]
    product = get_product_info(conn, line_item.product_number)
    app.job_number_var.set("DEMO-1001")
    app._selected_line_item = line_item
    app._product = product
    app.gtin_entry_var.set(product.gtin_raw or "")
    app.units_per_package_var.set("27000")
    app.labels_per_package_var.set("1")
    app.production_date_var.set("261104")
    app.test_mode_var.set(False)
    yield app, tmp_path
    app.test_mode_var.set(True)


def test_generate_writes_the_fixed_carton_file_and_an_archive_folder(carton_screen, monkeypatch):
    app, tmp_path = carton_screen
    dialogs = Dialogs(monkeypatch)

    app._generate()

    out = tmp_path / "output"
    assert dialogs.errors == []
    assert [p.name for p in out.glob("*.csv")] == ["carton_jwn_labels.csv"]
    assert (out / "archive").is_dir()
    assert dialogs.asked == []  # no earlier file, so no warning
    assert "carton_jwn_labels.csv" in dialogs.infos[-1][1]


def test_a_second_generate_warns_then_archives_the_old_file_and_writes_the_new_one(carton_screen, monkeypatch):
    app, tmp_path = carton_screen
    dialogs = Dialogs(monkeypatch)
    app._generate()
    out = tmp_path / "output"
    first = read(out / "carton_jwn_labels.csv")

    app._generate()

    assert len(dialogs.asked) == 1
    title, message, kwargs = dialogs.asked[0]
    assert "carton_jwn_labels.csv" in message and "archive" in message
    assert kwargs.get("default") == "cancel"  # the safe button has the focus
    archived = list((out / "archive").iterdir())
    assert len(archived) == 1 and archived[0].name.startswith("carton_jwn_labels_20")
    assert read(archived[0]) == first  # the old labels, whole
    new = read(out / "carton_jwn_labels.csv")
    assert {r["SSCC"] for r in new}.isdisjoint({r["SSCC"] for r in first})  # new SSCCs in the fixed file
    assert "moved to the archive folder" in dialogs.infos[-1][1]


def test_cancelling_the_warning_issues_nothing_and_keeps_the_file(carton_screen, monkeypatch):
    app, tmp_path = carton_screen
    dialogs = Dialogs(monkeypatch)
    app._generate()
    out = tmp_path / "output"
    before_bytes = (out / "carton_jwn_labels.csv").read_bytes()
    db = app.settings.local_db_file
    rows_before = count_label_history(db)
    counter_before = (tmp_path / "sscc_state.json").read_text()
    dialogs.ok = False

    app._generate()

    assert count_label_history(db) == rows_before  # nothing logged
    assert (tmp_path / "sscc_state.json").read_text() == counter_before  # no SSCC used
    assert (out / "carton_jwn_labels.csv").read_bytes() == before_bytes  # file unchanged
    assert list((out / "archive").iterdir()) == []  # nothing archived
    title, note = dialogs.infos[-1]
    assert title == "Cancelled"
    assert "will NOT print" in note and "run Generate Labels again" in note and "No SSCC numbers were used" in note


def test_if_the_old_file_cannot_be_archived_the_operator_is_told_and_the_old_file_stays(carton_screen, monkeypatch):
    app, tmp_path = carton_screen
    dialogs = Dialogs(monkeypatch)
    app._generate()
    out = tmp_path / "output"
    before_bytes = (out / "carton_jwn_labels.csv").read_bytes()
    monkeypatch.setattr(label_files.os, "rename", lambda s, d: (_ for _ in ()).throw(PermissionError("in use")))

    app._generate()

    assert dialogs.errors and dialogs.errors[-1][0] == "Could not archive the old label file"
    assert "Reprint Selected" in dialogs.errors[-1][1]
    assert (out / "carton_jwn_labels.csv").read_bytes() == before_bytes


def test_test_mode_runs_use_their_own_file_so_the_real_one_is_never_touched(carton_screen, monkeypatch):
    app, tmp_path = carton_screen
    dialogs = Dialogs(monkeypatch)
    app._generate()
    out = tmp_path / "output"
    real_bytes = (out / "carton_jwn_labels.csv").read_bytes()

    app.test_mode_var.set(True)
    app._generate()

    assert (out / "carton_jwn_labels.csv").read_bytes() == real_bytes
    assert (out / "carton_jwn_labels_TEST.csv").exists()
    assert dialogs.asked == []  # no earlier _TEST file, so no warning


# --- Reprint Selected -------------------------------------------------------------------------------

def _find_tree(widget):
    for child in widget.winfo_children():
        if child.winfo_class() == "Treeview":
            return child
        found = _find_tree(child)
        if found is not None:
            return found


def _all_buttons(widget):
    found = []
    for child in widget.winfo_children():
        if child.winfo_class() == "TButton":
            found.append(child)
        found.extend(_all_buttons(child))
    return found


def _tick(tree, iid):
    bbox = tree.bbox(iid, "#1")
    tree.event_generate("<Button-1>", x=bbox[0] + bbox[2] // 2, y=bbox[1] + bbox[3] // 2)


@pytest.fixture
def history_with_carton_and_pallet(app, tmp_path, monkeypatch):
    db = tmp_path / "barbell.db"
    cartons = rows_for("100001", [1, 2])
    record_generation_run(cartons, units_per_package=1000, labels_per_package=1, test_mode=False, db_path=db)
    create_pallet(
        carton_ssccs=[c.sscc for c in cartons], job_number="100001", quantity=2000, production_date="260505",
        packing_slip_number="100512", pallet_sscc=build_sscc("08600157112", "0", 9), carton_count=2, db_path=db,
    )
    monkeypatch.setattr(app.settings, "local_db_file", str(db))
    monkeypatch.setattr(app.settings, "demo_mode", False)
    monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
    app._show_history()
    win = app.winfo_children()[-1]
    win.update()
    yield win, tmp_path
    win.destroy()


def _reprint(win, tree, label_types):
    for iid in tree.get_children():
        if tree.item(iid, "values")[11] in label_types:
            _tick(tree, iid)
    win.update()
    next(b for b in _all_buttons(win) if "Reprint" in b.cget("text")).invoke()
    win.update()


def test_reprinting_cartons_and_a_pallet_writes_both_fixed_files(history_with_carton_and_pallet, monkeypatch):
    win, tmp_path = history_with_carton_and_pallet
    dialogs = Dialogs(monkeypatch)

    _reprint(win, _find_tree(win), {"CARTON", "PALLET"})

    out = tmp_path / "output"
    assert sorted(p.name for p in out.glob("*.csv")) == ["carton_jwn_labels.csv", "pallet_jwn_labels.csv"]
    assert {r["LabelType"] for r in read(out / "carton_jwn_labels.csv")} == {"CARTON"}
    assert {r["LabelType"] for r in read(out / "pallet_jwn_labels.csv")} == {"PALLET"}
    assert dialogs.errors == [] and (out / "archive").is_dir()


def test_a_reprint_archives_the_files_it_replaces_after_one_warning(history_with_carton_and_pallet, monkeypatch):
    win, tmp_path = history_with_carton_and_pallet
    dialogs = Dialogs(monkeypatch)
    out = tmp_path / "output"
    _reprint(win, _find_tree(win), {"CARTON", "PALLET"})  # first time: files created
    assert dialogs.asked == []

    _reprint(win, _find_tree(win), {"CARTON", "PALLET"})  # second time (the list refreshed itself): both replaced

    assert len(dialogs.asked) == 1
    assert "carton_jwn_labels.csv" in dialogs.asked[0][1] and "pallet_jwn_labels.csv" in dialogs.asked[0][1]
    names = sorted(p.name for p in (out / "archive").iterdir())
    assert len(names) == 2
    assert names[0].startswith("carton_jwn_labels_20") and names[1].startswith("pallet_jwn_labels_20")


def test_cancelling_a_reprint_logs_nothing_and_changes_no_file(history_with_carton_and_pallet, monkeypatch):
    win, tmp_path = history_with_carton_and_pallet
    dialogs = Dialogs(monkeypatch)
    out = tmp_path / "output"
    tree = _find_tree(win)
    _reprint(win, tree, {"CARTON"})  # makes carton_jwn_labels.csv
    db = win.master.settings.local_db_file
    rows_before = count_label_history(db)
    file_before = (out / "carton_jwn_labels.csv").read_bytes()
    dialogs.ok = False

    _reprint(win, _find_tree(win), {"CARTON"})

    assert count_label_history(db) == rows_before  # no reprint rows logged
    assert (out / "carton_jwn_labels.csv").read_bytes() == file_before
    assert dialogs.infos[-1][0] == "Cancelled" and "will NOT print" in dialogs.infos[-1][1]
