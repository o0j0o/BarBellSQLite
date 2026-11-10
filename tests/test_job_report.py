"""
1.1.17 Job Report: every pallet and carton logged for one job, from BarBell's own
SQLite data only (no Label Traxx / ODBC), as a hierarchy - each pallet with its
cartons, then the cartons on no pallet under "No Associated Pallet SSCC" - shown
on screen and exportable to PDF.
"""

import datetime
import sqlite3

import pytest

from src.db.local_store import (
    create_pallet,
    fetch_job_report,
    record_generation_run,
    void_pallet,
)
from src.job_report import NO_PALLET_HEADING, build_job_report_pdf, render_job_report_pages
from src.labels import LabelRow

GTIN = "00051096184921"


def carton_rows(ssccs, job="122984", copies=1, quantity=10000):
    return [
        LabelRow(
            job_number=job, packing_slip_number="100495", customer_number="J00005",
            customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
            item_description="233458 - JWN White O/P Rum B 750Ml USA - PS", quantity=quantity,
            batch="12298447388", production_date="260323", sscc=sscc, gtin=GTIN,
            package_index=i, label_copy_index=copy,
        )
        for i, sscc in enumerate(ssccs, start=1)
        for copy in range(1, copies + 1)
    ]


def sscc(n):
    return f"0086001571120{n:05d}"


def seed(db, cartons=6, on_pallet_a=2, on_pallet_b=2, job="122984", copies=1, test_mode=False):
    ssccs = [sscc(i) for i in range(1, cartons + 1)]
    record_generation_run(
        carton_rows(ssccs, job=job, copies=copies), units_per_package=10000,
        labels_per_package=copies, test_mode=test_mode, db_path=db,
    )
    pallets = {}
    for name, count, pallet_sscc in (("A", on_pallet_a, "008600157112090001"), ("B", on_pallet_b, "008600157112090002")):
        if count:
            taken = [s for s in ssccs if all(s not in v for v in pallets.values())][:count]
            create_pallet(
                carton_ssccs=taken, job_number=job, quantity=10000 * len(taken),
                production_date="260323", packing_slip_number="100495",
                pallet_sscc=pallet_sscc, carton_count=len(taken), db_path=db,
            )
            pallets[pallet_sscc] = taken
    return ssccs, pallets


def test_an_unknown_job_is_none_and_matching_is_exact(tmp_path):
    db = tmp_path / "b.db"
    seed(db)
    assert fetch_job_report("999999", db) is None
    assert fetch_job_report("12298", db) is None  # a prefix is not a match
    assert fetch_job_report("122984 ", db).job_number == "122984"  # stray spaces only
    # exact: another job number differing only by letter case is a different job
    seed(db, job="abc-1", cartons=1, on_pallet_a=0, on_pallet_b=0)
    assert fetch_job_report("ABC-1", db) is None
    assert fetch_job_report("abc-1", db).job_number == "abc-1"


def test_the_report_is_a_pallet_then_cartons_hierarchy(tmp_path):
    db = tmp_path / "b.db"
    ssccs, pallets = seed(db, cartons=6, on_pallet_a=3, on_pallet_b=2)
    report = fetch_job_report("122984", db)

    assert [p.sscc for p in report.pallets] == ["008600157112090001", "008600157112090002"]
    first, second = report.pallets
    assert [c.sscc for c in first.cartons] == pallets["008600157112090001"]
    assert [c.sscc for c in second.cartons] == pallets["008600157112090002"]
    assert (first.gtin, first.production_date, first.batch) == (GTIN, "260323", "12298447388")
    assert first.description.startswith("233458 - JWN White")
    assert (first.quantity, first.carton_count) == (30000, 3)
    assert (second.quantity, second.carton_count) == (20000, 2)
    c = first.cartons[0]
    assert (c.quantity, c.batch, c.production_date) == (10000, "12298447388", "260323")

    assert [c.sscc for c in report.unassociated_cartons] == [ssccs[5]]
    assert report.carton_total == 6
    assert report.test_mode is False


def test_print_copies_count_a_carton_once(tmp_path):
    db = tmp_path / "b.db"
    seed(db, cartons=2, on_pallet_a=1, on_pallet_b=0, copies=2)
    report = fetch_job_report("122984", db)
    assert report.carton_total == 2
    assert len(report.pallets[0].cartons) == 1 and len(report.unassociated_cartons) == 1


def test_a_voided_pallet_frees_its_cartons_into_the_unassociated_list(tmp_path):
    db = tmp_path / "b.db"
    ssccs, pallets = seed(db, cartons=4, on_pallet_a=2, on_pallet_b=2)
    void_pallet("008600157112090001", db)
    report = fetch_job_report("122984", db)
    assert [p.sscc for p in report.pallets] == ["008600157112090002"]
    assert {c.sscc for c in report.unassociated_cartons} == set(pallets["008600157112090001"])


def test_a_voided_carton_is_left_out(tmp_path):
    db = tmp_path / "b.db"
    ssccs, _ = seed(db, cartons=3, on_pallet_a=0, on_pallet_b=0)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE labels SET status = 'void' WHERE sscc = ?", (ssccs[0],))
    report = fetch_job_report("122984", db)
    assert [c.sscc for c in report.unassociated_cartons] == ssccs[1:]


def test_the_report_needs_only_the_sqlite_file(tmp_path, monkeypatch):
    """No Label Traxx / ODBC: building the report must not touch either."""
    import src.db.readonly_connection as ro

    def boom(*a, **k):
        raise AssertionError("Job Report must not use Label Traxx / ODBC")

    monkeypatch.setattr(ro.ReadOnlyConnection, "__init__", boom)
    db = tmp_path / "b.db"
    seed(db)
    report = fetch_job_report("122984", db)
    pages = render_job_report_pages(report, company_name="Caribbean Label Crafts Ltd.")
    assert pages


def test_pages_are_us_letter_landscape_and_one_job_can_run_to_many_pages(tmp_path):
    db = tmp_path / "b.db"
    seed(db, cartons=60, on_pallet_a=20, on_pallet_b=20)
    report = fetch_job_report("122984", db)
    pages = render_job_report_pages(report, printed_at=datetime.datetime(2026, 11, 10, 9, 0))
    assert len(pages) >= 3
    assert all(p.mode == "1" for p in pages)
    assert all(p.width > p.height for p in pages)
    assert round(pages[0].width / 300, 2) == 11.0 and round(pages[0].height / 300, 2) == 8.5


def test_an_empty_job_and_a_test_pallet_still_render(tmp_path):
    db = tmp_path / "b.db"
    seed(db, cartons=1, on_pallet_a=0, on_pallet_b=0)
    with sqlite3.connect(db) as conn:
        conn.execute("DELETE FROM labels")
    report = fetch_job_report("122984", db)
    assert report is not None and report.carton_total == 0
    assert render_job_report_pages(report)

    # a TEST-SSCC placeholder pallet (not digits) can't be a barcode but must not crash
    seed(db, cartons=2, on_pallet_a=1, on_pallet_b=0, job="TESTJOB", test_mode=True)
    with sqlite3.connect(db) as conn:
        conn.execute("UPDATE labels SET sscc = 'TEST-SSCC-00001' WHERE label_type = 'PALLET' AND job_number = 'TESTJOB'")
    report = fetch_job_report("TESTJOB", db)
    assert report.test_mode is True
    assert render_job_report_pages(report)


def test_the_pdf_is_written(tmp_path):
    db = tmp_path / "b.db"
    seed(db)
    out = build_job_report_pdf(fetch_job_report("122984", db), tmp_path / "sub" / "Job_report_122984.pdf")
    assert out.exists() and out.read_bytes().startswith(b"%PDF")


# --- the screen ------------------------------------------------------------------------------


def _buttons(widget):
    result = []
    for child in widget.winfo_children():
        if child.winfo_class() in ("TButton", "Button"):
            result.append(child)
        result.extend(_buttons(child))
    return result


def _find_treeview(widget):
    for child in widget.winfo_children():
        if child.winfo_class() == "Treeview":
            return child
        found = _find_treeview(child)
        if found is not None:
            return found
    return None


@pytest.fixture
def local_db(app, tmp_path, monkeypatch):
    db = tmp_path / "barbell.db"
    monkeypatch.setattr(app.settings, "local_db_file", str(db))
    monkeypatch.setattr(app.settings, "demo_mode", False)
    monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "out"))
    return db


def test_the_screen_says_job_is_not_in_barbell_for_a_missing_job(app, local_db):
    win = app._show_job_report_screen()
    try:
        win.job_var.set("NO-SUCH-JOB")
        win.run_report()
        assert win.message_label.cget("text") == "Job is Not in BarBell"
        assert str(win.export_button.cget("state")) == "disabled"
    finally:
        win.destroy()


def test_the_screen_shows_a_job_and_exports_a_pdf(app, local_db, monkeypatch, tmp_path):
    seed(local_db)
    opened = []
    monkeypatch.setattr(type(app), "_open_file", staticmethod(lambda path: opened.append(path)))
    win = app._show_job_report_screen()
    try:
        win.job_var.set("122984")
        win.run_report()
        assert "2 pallet(s)" in win.message_label.cget("text")
        assert "6 carton(s)" in win.message_label.cget("text")
        assert win.page_photos  # pages are on screen
        assert str(win.export_button.cget("state")) == "normal"

        win.export_pdf()
        assert len(opened) == 1 and opened[0].name == "Job_report_122984.pdf"
        assert opened[0].read_bytes().startswith(b"%PDF")

        win.job_var.set("   ")
        win.run_report()
        assert win.page_photos == [] and str(win.export_button.cget("state")) == "disabled"
    finally:
        win.destroy()


def test_the_screen_can_be_opened_with_a_job_already_filled_in(app, local_db):
    seed(local_db)
    win = app._show_job_report_screen(job_number="122984")
    try:
        assert win.report is not None and win.report.job_number == "122984"
    finally:
        win.destroy()


def test_job_report_is_in_the_home_menu_and_beside_pallet_report_in_history(app, local_db):
    home = app.nametowidget(app._menubar.entrycget(0, "menu"))
    labels = [home.entrycget(i, "label") for i in range(home.index("end") + 1)]
    assert "Job Report..." in labels

    seed(local_db)
    before = set(app.winfo_children())
    app._show_history()
    history = [w for w in app.winfo_children() if w not in before and w.winfo_class() == "Toplevel"][0]
    try:
        texts = [b.cget("text") for b in _buttons(history)]
        assert "Job Report" in texts
        assert texts.index("Job Report") == texts.index("Pallet Report (PDF)") + 1
    finally:
        history.destroy()


def test_no_pallet_heading_text():
    assert NO_PALLET_HEADING == "No Associated Pallet SSCC"
