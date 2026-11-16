"""
Test-mode SSCCs are numeric: 18 digits, seven zeros, a running test number and a correct GS1 check digit
(e.g. 000000000000000178). The test number is ONE count shared by test cartons and test pallets, worked
out from the database, that never restarts - so no two test labels ever share a number and a test label
always scans like a real one. The real SSCC counter is never touched, a test label can never be a real
SSCC, old TEST-SSCC-##### rows are left exactly as they are, and a test pallet's report keeps its TEST
PALLET box.
"""

import json

import numpy as np
import pytest
import zxingcpp

from src.db.local_store import (
    CartonInfo,
    PalletReport,
    PalletReportCarton,
    count_label_history,
    create_pallet,
    fetch_label_history,
    next_test_serial,
    record_generation_run,
)
from src.labels import LabelRow
from src.pallet_report import _is_real_sscc, render_pallet_report_pages
from src.pallet_scan import check_carton_for_pallet, clean_scanned_sscc
from src.sscc import SSCCGenerator, build_sscc, build_test_sscc, gs1_check_digit, is_test_sscc

PREFIX = "08600157112"


def rows_for(job, ssccs):
    return [
        LabelRow(
            job_number=job, packing_slip_number="100512", customer_number="J00005", customer_name="JWN",
            product_no="41185", item_number="234412", item_description="Rum", quantity=1000,
            batch=f"{job}41185", production_date="260505", sscc=sscc,
            gtin="00636191205407", package_index=i, label_copy_index=1,
        )
        for i, sscc in enumerate(ssccs, start=1)
    ]


def add(db, job, ssccs, test=True):
    record_generation_run(rows_for(job, ssccs), units_per_package=1000, labels_per_package=1, test_mode=test, db_path=db)


# --- the running test count, worked out from the database ----------------------------------------------

def test_the_count_starts_at_one_in_an_empty_database(tmp_path):
    assert next_test_serial(tmp_path / "barbell.db") == 1


def test_it_continues_after_the_highest_test_number_in_the_data(tmp_path):
    db = tmp_path / "barbell.db"
    add(db, "100001", [build_test_sscc(n) for n in (1, 2, 3)])
    assert next_test_serial(db) == 4
    add(db, "100002", [build_test_sscc(n) for n in (4, 5)])
    assert next_test_serial(db) == 6


def test_it_never_goes_backwards_even_with_gaps(tmp_path):
    db = tmp_path / "barbell.db"
    add(db, "100001", [build_test_sscc(40)])
    assert next_test_serial(db) == 41


def test_real_ssccs_and_the_old_placeholders_do_not_count(tmp_path):
    db = tmp_path / "barbell.db"
    add(db, "100001", [build_sscc(PREFIX, "0", 500), build_sscc(PREFIX, "1", 41)], test=False)  # real
    add(db, "100002", ["TEST-SSCC-00099", "TEST-SSCC-00100"])  # the old format: left alone, not counted
    assert next_test_serial(db) == 1


def test_a_test_pallet_is_part_of_the_same_count(tmp_path):
    db = tmp_path / "barbell.db"
    cartons = [build_test_sscc(1), build_test_sscc(2)]
    add(db, "100001", cartons)
    create_pallet(
        carton_ssccs=cartons, job_number="100001", quantity=2000, production_date="260505",
        packing_slip_number="100512", pallet_sscc=build_test_sscc(3), carton_count=2, db_path=db,
    )
    assert next_test_serial(db) == 4  # cartons took 1-2, the pallet 3, the next anything is 4


def test_counting_changes_nothing_in_the_database(tmp_path):
    db = tmp_path / "barbell.db"
    add(db, "100001", [build_test_sscc(1)])
    before = count_label_history(db)
    for _ in range(3):
        next_test_serial(db)
    assert count_label_history(db) == before


# --- the scanner ---------------------------------------------------------------------------------------

def carton(sscc, test_mode):
    return CartonInfo(
        id=1, sscc=sscc, job_number="100001", product_no="41185", item_number="234412",
        gtin="00636191205407", batch="10000141185", quantity=1000, production_date="260505",
        packing_slip_number="100512", status="original", pallet_sscc=None, label_type="CARTON",
        test_mode=test_mode, created_at="2026-11-13T00:00:00",
    )


def test_a_test_sscc_scans_like_any_other_18_digit_sscc():
    value = build_test_sscc(7)
    assert clean_scanned_sscc(value, test_mode=True) == value
    assert clean_scanned_sscc(value, test_mode=False) == value  # valid shape; the test flag decides, below
    assert clean_scanned_sscc(f"(00){value}", test_mode=True) == value  # and the printed barcode's own form
    assert clean_scanned_sscc(f"00{value}", test_mode=True) == value


def test_the_older_placeholders_are_still_accepted_in_test_mode_only():
    assert clean_scanned_sscc("TEST-SSCC-00007", test_mode=True) == "TEST-SSCC-00007"
    with pytest.raises(ValueError):
        clean_scanned_sscc("TEST-SSCC-00007", test_mode=False)


def test_a_numeric_test_carton_can_never_go_on_a_real_pallet():
    result = check_carton_for_pallet(carton(build_test_sscc(7), True), [], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason and "test carton" in result.blocked_reason


def test_a_real_carton_can_never_go_on_a_test_pallet():
    result = check_carton_for_pallet(carton(build_sscc(PREFIX, "0", 12), False), [], expected_count=5, pallet_test_mode=True)
    assert result.blocked_reason and "production carton" in result.blocked_reason


def test_numeric_test_cartons_go_on_a_test_pallet():
    result = check_carton_for_pallet(carton(build_test_sscc(7), True), [], expected_count=5, pallet_test_mode=True)
    assert result.blocked_reason is None


# --- the reports keep the TEST PALLET box -----------------------------------------------------------------

def test_a_test_sscc_is_not_a_real_one_to_the_reports():
    assert not _is_real_sscc(build_test_sscc(3))
    assert not _is_real_sscc("TEST-SSCC-00003")
    assert _is_real_sscc(build_sscc(PREFIX, "0", 159))


def decoded(pages):
    return [r.text for page in pages for r in zxingcpp.read_barcodes(np.array(page.convert("L")))]


def report(pallet_sscc, carton_ssccs, test_mode):
    return PalletReport(
        pallet_sscc=pallet_sscc, job_number="100001", packing_slip_number="100512", production_date="260505",
        test_mode=test_mode, created_at="2026-11-13T14:03:00+00:00",
        cartons=[
            PalletReportCarton(
                sscc=s, item_number="234412", description="Rum", quantity=1000 + i, batch="10000141185",
                gtin="00636191205407", production_date="260505",
            )
            for i, s in enumerate(carton_ssccs)  # different quantities, so each contents barcode is its own
        ],
    )


def test_a_numeric_test_pallet_report_has_no_pallet_barcode_and_no_test_carton_barcodes():
    test_cartons = [build_test_sscc(1), build_test_sscc(2)]
    texts = decoded(render_pallet_report_pages(report(build_test_sscc(3), test_cartons, True)))

    assert not any(t.startswith("(00)") for t in texts)  # no barcode that looks like a real SSCC at all
    assert len([t for t in texts if t.startswith("(02)")]) == 2  # the contents barcodes still print


def test_a_real_pallet_report_still_has_its_barcodes():
    real = [build_sscc(PREFIX, "0", 128), build_sscc(PREFIX, "0", 135)]
    texts = decoded(render_pallet_report_pages(report(build_sscc(PREFIX, "0", 159), real, False)))
    assert f"(00){build_sscc(PREFIX, '0', 159)}" in texts
    assert all(f"(00){s}" in texts for s in real)


# --- the screens -------------------------------------------------------------------------------------------

class Dialogs:
    def __init__(self, monkeypatch):
        self.errors = []
        monkeypatch.setattr("tkinter.messagebox.askokcancel", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: self.errors.append((title, msg)))


@pytest.fixture
def test_run_screen(app, tmp_path, monkeypatch):
    """The main screen ready to Generate Labels in Test mode (real, not Demo) against sample data, with a
    real SSCC counter file that must stay untouched."""
    from src.demo_data import DemoConnection
    from src.labels import get_product_info, list_packing_slip_line_items

    state_file = tmp_path / "sscc_state.json"
    SSCCGenerator(PREFIX, "0", state_file).initialize(start_at=10)
    for name, value in {
        "demo_mode": False, "local_db_file": str(tmp_path / "barbell.db"),
        "output_dir": str(tmp_path / "output"), "audit_log_file": str(tmp_path / "audit.jsonl"),
        "gs1_company_prefix": PREFIX, "sscc_extension_digit": "0", "sscc_state_file": str(state_file),
    }.items():
        monkeypatch.setattr(app.settings, name, value)
    monkeypatch.setattr(app, "_connect", lambda: DemoConnection())
    monkeypatch.setattr("barbell_gui.winsound.MessageBeep", lambda *_a, **_k: None)
    conn = DemoConnection()
    line_item = list_packing_slip_line_items(conn, "DEMO-PS-5001")[0]
    app.job_number_var.set("DEMO-1001")
    app._selected_line_item = line_item
    app._product = get_product_info(conn, line_item.product_number)
    app.gtin_entry_var.set(app._product.gtin_raw or "")
    app.units_per_package_var.set("27000")
    app.labels_per_package_var.set("1")
    app.production_date_var.set("261104")
    app.test_mode_var.set(True)
    yield app, tmp_path, state_file
    app.test_mode_var.set(True)


def test_every_test_run_continues_the_one_count_and_nothing_repeats(test_run_screen, monkeypatch):
    app, tmp_path, state_file = test_run_screen
    dialogs = Dialogs(monkeypatch)
    counter_before = state_file.read_text()

    for _ in range(3):
        app._generate()

    assert dialogs.errors == []
    ssccs = [r.sscc for r in fetch_label_history(app.settings.local_db_file, job_number="DEMO-1001")]
    distinct = sorted(set(ssccs))
    assert len(distinct) == len(ssccs)  # one label per package here: no repeats at all
    assert all(is_test_sscc(s) for s in distinct)
    assert [int(s[7:17]) for s in distinct] == list(range(1, len(distinct) + 1))  # 1, 2, 3 ... no gaps, no restarts
    assert all(s[-1] == gs1_check_digit(s[:-1]) for s in distinct)
    assert next_test_serial(app.settings.local_db_file) == len(distinct) + 1
    assert state_file.read_text() == counter_before  # the real counter was never touched


def test_the_preview_shows_the_next_test_number(test_run_screen, monkeypatch):
    app, tmp_path, _state = test_run_screen
    Dialogs(monkeypatch)

    assert app._gather_preview_inputs()["preview_sscc"] == build_test_sscc(1)
    app._generate()
    after = next_test_serial(app.settings.local_db_file)
    assert after > 1
    assert app._gather_preview_inputs()["preview_sscc"] == build_test_sscc(after)


def test_the_csv_carries_the_numeric_test_ssccs(test_run_screen, monkeypatch):
    import csv

    app, tmp_path, _state = test_run_screen
    Dialogs(monkeypatch)
    app._generate()

    with open(tmp_path / "output" / "carton_jwn_labels_TEST.csv", newline="", encoding="utf-8") as f:
        written = [row["SSCC"] for row in csv.DictReader(f)]
    assert written and all(is_test_sscc(s) for s in written)


def _find(widget, cls):
    for child in widget.winfo_children():
        if child.winfo_class() == cls:
            yield child
        yield from _find(child, cls)


def test_a_test_pallet_takes_the_next_number_in_the_same_count(app, tmp_path, monkeypatch):
    """Demo Mode forces the pallet screen into test mode, so no real SSCC can be issued here."""
    dialogs = Dialogs(monkeypatch)
    db = tmp_path / "demo.db"
    monkeypatch.setattr(app.settings, "demo_mode", True)
    monkeypatch.setattr(app.settings, "demo_db_file", str(db))
    monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
    monkeypatch.setattr("barbell_gui.winsound.MessageBeep", lambda *_a, **_k: None)
    cartons = [build_test_sscc(1), build_test_sscc(2)]
    add(db, "100001", cartons)

    before = set(app.winfo_children())
    app._show_pallet_screen()
    win = next(iter(set(app.winfo_children()) - before))
    win.update()
    try:
        entries = list(_find(win, "TEntry"))
        entries[0].insert(0, "2")
        for sscc in cartons:
            win.focus_force()
            entries[1].focus_force()
            win.update()
            entries[1].insert(0, sscc)
            entries[1].event_generate("<Return>")
            win.update()
        next(b for b in _find(win, "TButton") if "Generate Pallet Label" in b.cget("text")).invoke()
        win.update()
    finally:
        win.destroy()

    assert dialogs.errors == []
    pallet_ssccs = {r.sscc for r in fetch_label_history(db) if r.label_type == "PALLET"}
    assert pallet_ssccs == {build_test_sscc(3)}  # cartons 1-2, so the pallet is 3, never a repeat
    assert next_test_serial(db) == 4


def test_the_old_test_rows_are_left_exactly_as_they_are(tmp_path):
    db = tmp_path / "barbell.db"
    add(db, "100001", ["TEST-SSCC-00001", "TEST-SSCC-00002"])
    before = [(r.id, r.sscc) for r in fetch_label_history(db)]
    add(db, "100002", [build_test_sscc(next_test_serial(db))])
    after = [(r.id, r.sscc) for r in fetch_label_history(db)]
    assert all(row in after for row in before)  # nothing renamed, renumbered or removed
    assert len(after) == len(before) + 1
    json.dumps(after)  # (plain data - just proving nothing odd crept in)
