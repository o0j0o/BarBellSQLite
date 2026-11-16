"""
Package Details on the main screen: Logistics labels per package starts at 1; Units per package is
suggested from the packing slip's notes (only when they add up); and the production date must be a real
YYMMDD date, at most 7 days ahead, from this year or last year (tests/conftest.py pins today to 13 Nov 2026).
"""

import pytest

import barbell_gui
from src.demo_data import DemoConnection
from src.labels import get_product_info, list_packing_slip_line_items


@pytest.fixture
def screen(app, tmp_path, monkeypatch):
    """The main screen on the Demo data (DEMO-1001's slip notes read '2 boxes of 3 rolls x 9000')."""
    monkeypatch.setattr(app.settings, "demo_mode", True)
    monkeypatch.setattr(app.settings, "demo_db_file", str(tmp_path / "demo.db"))
    errors = []
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: errors.append((title, msg)))
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda *a, **k: None)
    app.units_per_package_var.set("")
    app.job_number_var.set("")
    yield app, errors
    app._reset_product_selection()
    app.units_per_package_var.set("")


def pick_slip(app, job, index=0):
    app.job_number_var.set(job)
    app._load_packing_slips()
    app.slip_listbox.selection_clear(0, "end")
    app.slip_listbox.selection_set(index)
    app._on_slip_selected(None)
    app.update()


# --- Logistics labels per package ------------------------------------------------------------------

def test_labels_per_package_starts_at_1():
    """A freshly started BarBell - checked in its own process, since the tests share one Tk window."""
    import subprocess
    import sys
    from pathlib import Path

    code = (
        "import barbell_gui; a = barbell_gui.BarBellApp(); "
        "print(repr(a.labels_per_package_var.get()), repr(a.units_per_package_var.get())); a.destroy()"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], cwd=Path(barbell_gui.__file__).parent, capture_output=True, text=True, timeout=120
    )
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip().splitlines()[-1] == "'1' ''"  # labels per package 1; units per package empty


def test_a_blank_labels_per_package_comes_back_to_1_when_a_new_job_is_looked_up(screen):
    app, _errors = screen
    app.labels_per_package_var.set("")
    pick_slip(app, "DEMO-1001")
    assert app.labels_per_package_var.get() == "1"


def test_a_labels_per_package_the_operator_set_is_kept(screen):
    app, _errors = screen
    app.labels_per_package_var.set("2")
    pick_slip(app, "DEMO-1001")
    assert app.labels_per_package_var.get() == "2"
    app.labels_per_package_var.set("1")


# --- Units per package from the packing slip notes -------------------------------------------------

def test_units_per_package_is_suggested_from_the_notes_when_they_add_up(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1001")  # 54,000 in 2 boxes: BOX# 1 - 2, 3 ROLLS X 9000
    assert app.units_per_package_var.get() == "27000"
    assert "packing slip notes" in app.units_hint_var.get() and "BOX# 1 - 2" in app.units_hint_var.get()


def test_the_suggestion_can_be_changed_and_the_hint_then_goes(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1001")
    app.units_per_package_var.set("13500")
    assert app.units_hint_var.get() == ""  # no longer "from the notes"
    assert app.units_per_package_var.get() == "13500"


def test_notes_with_no_box_lines_leave_units_blank(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1003")  # notes empty
    assert app.units_per_package_var.get() == "" and app.units_hint_var.get() == ""


def test_a_slip_with_two_products_leaves_units_blank_until_nothing_can_be_trusted(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1002")  # two products, notes with no box lines
    assert app.units_per_package_var.get() == ""


def test_moving_to_a_slip_without_a_suggestion_removes_the_old_suggestion(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1001")
    assert app.units_per_package_var.get() == "27000"
    pick_slip(app, "DEMO-1003")
    assert app.units_per_package_var.get() == ""  # that 27000 was BarBell's, for the other slip


def test_a_number_the_operator_typed_is_never_wiped_by_a_slip_with_no_suggestion(screen):
    app, _errors = screen
    pick_slip(app, "DEMO-1001")
    app.units_per_package_var.set("12000")  # the operator's own value
    pick_slip(app, "DEMO-1003")
    assert app.units_per_package_var.get() == "12000"


def test_the_notes_of_a_slip_that_do_not_add_up_suggest_nothing(screen, monkeypatch):
    app, _errors = screen
    from src import demo_data

    rows = list(demo_data.DEMO_TABLES["PackingSlip"][1])
    wrong = list(rows[0])
    wrong[6] = "BOX# 1 - 2   3 ROLLS X 8000"  # 48,000, but the slip ships 54,000
    monkeypatch.setitem(demo_data.DEMO_TABLES, "PackingSlip", (demo_data.DEMO_TABLES["PackingSlip"][0], [tuple(wrong)] + rows[1:]))
    pick_slip(app, "DEMO-1001")
    assert app.units_per_package_var.get() == ""


# --- the production date ----------------------------------------------------------------------------

def prime(app, date):
    pick_slip(app, "DEMO-1001")
    app.gtin_entry_var.set(app._product.gtin_raw or "")
    app.units_per_package_var.set("27000")
    app.labels_per_package_var.set("1")
    app.production_date_var.set(date)
    app.test_mode_var.set(True)


@pytest.mark.parametrize("date", ["261113", "261120", "260101", "251231", "250101"])
def test_a_date_inside_the_window_is_accepted(screen, date):
    app, errors = screen
    prime(app, date)
    assert app._gather_preview_inputs() is not None and errors == []


@pytest.mark.parametrize("date", ["261121", "270101"])
def test_a_date_more_than_7_days_ahead_is_refused_with_the_latest_allowed(screen, date):
    app, errors = screen
    prime(app, date)
    assert app._gather_preview_inputs() is None
    assert errors[-1][0] == "Invalid date" and "261120" in errors[-1][1] and "future" in errors[-1][1]


@pytest.mark.parametrize("date", ["241231", "200101"])
def test_a_date_before_last_year_is_refused(screen, date):
    app, errors = screen
    prime(app, date)
    assert app._gather_preview_inputs() is None
    assert errors[-1][0] == "Invalid date" and "past" in errors[-1][1]


@pytest.mark.parametrize("date", ["261301", "261132", "260230", "26-11-04", "2026-11-04", "", "abcdef"])
def test_a_date_that_is_not_real_is_refused_as_before(screen, date):
    app, errors = screen
    prime(app, date)
    assert app._gather_preview_inputs() is None
    assert errors[-1][0] == "Invalid date" and "YYMMDD" in errors[-1][1]


def test_the_same_rules_apply_in_test_and_demo_mode(screen):
    app, errors = screen
    prime(app, "270101")
    app.test_mode_var.set(True)  # test mode
    assert app._gather_preview_inputs() is None  # demo mode is on too (the fixture), still refused


def test_generate_stops_on_a_bad_date_before_anything_is_issued(screen, monkeypatch):
    from src.db.local_store import count_label_history

    app, errors = screen
    prime(app, "241231")
    monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: pytest.fail("must not even ask"))
    app._generate()
    assert errors[-1][0] == "Invalid date"
    assert count_label_history(app.settings.demo_db_file) == 0  # nothing logged


def test_the_history_date_search_is_not_restricted(app):
    """Searching History by an old date must still work - the rules are for entering a production date."""
    from src.dates import normalize_production_date

    assert normalize_production_date("200101") == "200101"
