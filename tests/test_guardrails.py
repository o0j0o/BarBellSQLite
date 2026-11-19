"""
The red "Labels have been generated for this ..." guardrails beside the Find Packing Slips button:
Ticket, Packing Slip and Product No. messages stacked in that order, the Product one (only when the Ticket
and Packing Slip ones are showing) with a Continue button that the operator must press before Preview or
Generate. Uses the Demo data: DEMO-1001 is job DEMO-1001, packing slip DEMO-PS-5001, product DEMO-P100.
"""

import sqlite3

import pytest

import barbell_gui
from src.db.local_store import labels_already_generated, record_generation_run
from src.labels import LabelRow
from src.sscc import build_sscc, build_test_sscc

JOB, SLIP, PRODUCT = "DEMO-1001", "DEMO-PS-5001", "DEMO-P100"
_serial = [100]


def add_labels(db, job=JOB, slip=SLIP, product=PRODUCT, test=True, count=2):
    rows = []
    for i in range(1, count + 1):
        _serial[0] += 1
        sscc = build_test_sscc(_serial[0]) if test else build_sscc("08600157112", "0", _serial[0])
        rows.append(
            LabelRow(
                job_number=job, packing_slip_number=slip, customer_number="C1", customer_name="Customer",
                product_no=product, item_number="I1", item_description="Item", quantity=1000,
                batch=f"{job}{product}", production_date="261113", sscc=sscc, gtin="00099999000016",
                package_index=i, label_copy_index=1,
            )
        )
    record_generation_run(rows, units_per_package=1000, labels_per_package=1, test_mode=test, db_path=db)


@pytest.fixture
def screen(app, tmp_path, monkeypatch):
    monkeypatch.setattr(app.settings, "demo_mode", True)
    monkeypatch.setattr(app.settings, "demo_db_file", str(tmp_path / "demo.db"))
    warnings = []
    monkeypatch.setattr("tkinter.messagebox.showwarning", lambda title, msg, **k: warnings.append((title, msg)))
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda *a, **k: None)
    app.test_mode_var.set(True)
    app.job_number_var.set("")
    app._looked_up_job = None
    app._guardrail_cleared_key = None
    app._refresh_guardrails()
    yield app, str(tmp_path / "demo.db"), warnings
    app._reset_product_selection()
    app._looked_up_job = None
    app._guardrail_cleared_key = None
    app._refresh_guardrails()
    app.test_mode_var.set(False)


def find_job(app, job=JOB):
    app.job_number_var.set(job)
    app._load_packing_slips()
    app.update()


def pick_slip(app, index=0):
    app.slip_listbox.selection_clear(0, "end")
    app.slip_listbox.selection_set(index)
    app._on_slip_selected(None)
    app.update()


def shown(app):
    """The messages on screen, top to bottom."""
    labels = [app.ticket_used_label, app.slip_used_label, app.product_used_label]
    on = [lab for lab in labels if lab.winfo_manager() == "grid" and app.guardrail_frame.winfo_manager() == "grid"]
    return [lab.cget("text") for lab in sorted(on, key=lambda lab: int(lab.grid_info()["row"]))]


def continue_visible(app):
    return app.guardrail_continue_button.winfo_manager() == "grid" and app.guardrail_frame.winfo_manager() == "grid"


def prime(app):
    app.gtin_entry_var.set(app._product.gtin_raw or "")
    app.units_per_package_var.set("27000")
    app.labels_per_package_var.set("1")
    app.production_date_var.set("261113")


TICKET_MSG = "Labels have been generated for this Ticket No."
SLIP_MSG = "Labels have been generated for this Packing Slip No."
PRODUCT_MSG = "Labels have been generated for this Product No."


# --- the messages --------------------------------------------------------------------------------------

def test_the_exact_wording_and_red_colour():
    assert barbell_gui.TICKET_USED_MESSAGE == TICKET_MSG
    assert barbell_gui.SLIP_USED_MESSAGE == SLIP_MSG
    assert barbell_gui.PRODUCT_USED_MESSAGE == PRODUCT_MSG


def test_a_job_with_no_labels_shows_nothing(screen):
    app, _db, _w = screen
    find_job(app)
    pick_slip(app)
    assert shown(app) == [] and not continue_visible(app)


def test_a_ticket_with_labels_shows_the_ticket_message_alone_after_find(screen):
    app, db, _w = screen
    add_labels(db, slip="SOME-OTHER-SLIP", product="OTHER")
    find_job(app)
    assert shown(app) == [TICKET_MSG] and not continue_visible(app)


def test_the_messages_are_red(screen):
    app, db, _w = screen
    add_labels(db)
    find_job(app)
    pick_slip(app)
    for label in (app.ticket_used_label, app.slip_used_label, app.product_used_label):
        assert str(label.cget("foreground")) == barbell_gui.GUARDRAIL_RED


def test_a_used_slip_adds_the_slip_message_under_the_ticket_one(screen):
    app, db, _w = screen
    add_labels(db, slip=SLIP, product="A-DIFFERENT-PRODUCT")  # this slip, but not this P/N
    find_job(app)
    pick_slip(app)
    assert shown(app) == [TICKET_MSG, SLIP_MSG] and not continue_visible(app)


def test_all_three_stack_in_order_with_continue_when_the_product_was_used_too(screen):
    app, db, _w = screen
    add_labels(db)
    find_job(app)
    assert shown(app) == [TICKET_MSG]  # only the ticket, until a slip is picked
    pick_slip(app)
    assert shown(app) == [TICKET_MSG, SLIP_MSG, PRODUCT_MSG]
    assert continue_visible(app)


def test_a_slip_that_was_not_used_shows_no_slip_message(screen):
    app, db, _w = screen
    add_labels(db, slip="SOME-OTHER-SLIP", product=PRODUCT)  # same job and P/N, but another slip
    find_job(app)
    pick_slip(app)
    assert shown(app) == [TICKET_MSG]  # and so never the product message either


def test_looking_up_another_job_clears_the_messages(screen):
    app, db, _w = screen
    add_labels(db)
    find_job(app)
    pick_slip(app)
    assert len(shown(app)) == 3
    find_job(app, "DEMO-1003")
    assert shown(app) == []


# --- Test mode and real labels are kept apart -----------------------------------------------------------

def test_real_labels_do_not_count_for_a_test_run_and_the_checkbox_re_checks(screen):
    app, db, _w = screen
    add_labels(db, test=False)  # real labels
    find_job(app)
    pick_slip(app)
    assert shown(app) == []  # Test mode is on: real labels are not "used" for a practice run
    app.test_mode_var.set(False)  # untick: now it is a real run
    app.update()
    assert shown(app) == [TICKET_MSG, SLIP_MSG, PRODUCT_MSG]
    app.test_mode_var.set(True)
    app.update()
    assert shown(app) == []


# --- Continue ---------------------------------------------------------------------------------------------

def test_preview_and_generate_are_blocked_until_continue(screen):
    app, db, warnings = screen
    add_labels(db)
    find_job(app)
    pick_slip(app)
    prime(app)
    assert app._gather_preview_inputs() is None
    assert warnings and warnings[-1][0] == "Labels already generated" and PRODUCT_MSG in warnings[-1][1]


def test_continue_lets_the_operator_move_along_and_keeps_the_messages_up(screen):
    app, db, warnings = screen
    add_labels(db)
    find_job(app)
    pick_slip(app)
    prime(app)
    app.guardrail_continue_button.invoke()
    assert not continue_visible(app)
    assert shown(app) == [TICKET_MSG, SLIP_MSG, PRODUCT_MSG]  # still there to read
    assert app._gather_preview_inputs() is not None


def test_continue_covers_only_the_product_it_was_pressed_for(screen):
    app, db, warnings = screen
    add_labels(db, job="DEMO-1002", slip="DEMO-PS-5002", product="DEMO-P200")
    add_labels(db, job="DEMO-1002", slip="DEMO-PS-5002", product="DEMO-P201")
    find_job(app, "DEMO-1002")
    pick_slip(app)  # a slip with two products: none is selected yet
    assert shown(app) == [TICKET_MSG, SLIP_MSG]
    app.product_listbox.selection_set(0)
    app._on_product_selected(None)
    assert shown(app)[-1] == PRODUCT_MSG and continue_visible(app)
    app.guardrail_continue_button.invoke()
    assert not continue_visible(app)
    app.product_listbox.selection_clear(0, "end")
    app.product_listbox.selection_set(1)  # the other product, also already used
    app._on_product_selected(None)
    assert shown(app)[-1] == PRODUCT_MSG and continue_visible(app)  # Continue is asked for again


def test_generate_stops_at_the_block_and_issues_nothing(screen, monkeypatch):
    from src.db.local_store import count_label_history

    app, db, warnings = screen
    add_labels(db)
    before = count_label_history(db)
    find_job(app)
    pick_slip(app)
    prime(app)
    monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: pytest.fail("must not get as far as asking"))
    app._generate()
    assert count_label_history(db) == before


# --- the lookup itself -----------------------------------------------------------------------------------

def test_labels_already_generated_by_ticket_slip_and_product(tmp_path):
    db = tmp_path / "x.db"
    add_labels(db, job="J1", slip="S1", product="P1", test=False)
    assert labels_already_generated(db, "J1")
    assert labels_already_generated(db, "J1", packing_slip_number="S1")
    assert labels_already_generated(db, "J1", packing_slip_number="S1", product_no="P1")
    assert not labels_already_generated(db, "J2")
    assert not labels_already_generated(db, "J1", packing_slip_number="S2")
    assert not labels_already_generated(db, "J1", packing_slip_number="S1", product_no="P2")
    assert not labels_already_generated(db, "J1", test_mode=True)  # real labels do not count for a test run


def test_voided_labels_do_not_count(tmp_path):
    db = tmp_path / "x.db"
    add_labels(db, job="J1", slip="S1", product="P1", test=False)
    conn = sqlite3.connect(str(db))
    conn.execute("UPDATE labels SET status = 'void'")
    conn.commit()
    conn.close()
    assert not labels_already_generated(db, "J1")


def test_older_labels_with_no_product_of_their_own_use_the_jobs_row(tmp_path):
    db = tmp_path / "x.db"
    add_labels(db, job="J1", slip="S1", product="P1", test=False)
    conn = sqlite3.connect(str(db))
    conn.execute("UPDATE labels SET product_no = NULL, packing_slip_number = NULL")
    conn.commit()
    conn.close()
    assert labels_already_generated(db, "J1", packing_slip_number="S1", product_no="P1")
    assert not labels_already_generated(db, "J1", packing_slip_number="S1", product_no="P9")
