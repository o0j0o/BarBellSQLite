"""
Job/Label History: the plain list shows the last 90 days of REAL labels so it stays short; a
Show dropdown, a Hide test labels checkbox and Show all history change that; and any search
looks through ALL history, test labels included. Nothing is ever deleted - the filter only
limits what is listed.
"""

import datetime
import sqlite3

import pytest

from src.db.local_store import count_label_history, fetch_label_history, record_generation_run
from src.labels import LabelRow
from src.sscc import build_sscc

PREFIX = "08600157112"


def rows_for(job, serials, test=False):
    return [
        LabelRow(
            job_number=job, packing_slip_number="100512", customer_number="J00005", customer_name="JWN",
            product_no="41185", item_number="234412", item_description="Rum", quantity=1000,
            batch=f"{job}41185", production_date="260505",
            sscc=f"TEST-SSCC-{n:05d}" if test else build_sscc(PREFIX, "0", n),
            gtin="00636191205407", package_index=i, label_copy_index=1,
        )
        for i, n in enumerate(serials, start=1)
    ]


def add(db, job, serials, age_days=0, test=False):
    record_generation_run(rows_for(job, serials, test), units_per_package=1000, labels_per_package=1,
                          test_mode=test, db_path=db)
    when = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=age_days)).isoformat()
    conn = sqlite3.connect(str(db))
    conn.execute("UPDATE labels SET created_at = ? WHERE job_number = ?", (when, job))
    conn.commit()
    conn.close()


@pytest.fixture
def db(tmp_path):
    path = tmp_path / "barbell.db"
    add(path, "100001", range(1, 6), age_days=5)  # real, recent      -> 5 rows
    add(path, "100002", range(10, 13), age_days=200)  # real, old (shipped long ago) -> 3 rows
    add(path, "100003", range(1, 5), age_days=5, test=True)  # test, recent -> 4 rows
    add(path, "100004", range(20, 22), age_days=200, test=True)  # test, old   -> 2 rows
    return path


def jobs(rows):
    return sorted({r.job_number for r in rows})


# --- store: the date window and hide-test ------------------------------------------------------

def test_since_days_lists_only_recent_labels(db):
    assert jobs(fetch_label_history(db, since_days=90)) == ["100001", "100003"]
    assert jobs(fetch_label_history(db, since_days=365)) == ["100001", "100002", "100003", "100004"]


def test_the_window_edge_is_exact(tmp_path):
    path = tmp_path / "barbell.db"
    add(path, "200001", [1], age_days=89)
    add(path, "200002", [2], age_days=91)
    assert jobs(fetch_label_history(path, since_days=90)) == ["200001"]


def test_hide_test_drops_test_mode_labels_only(db):
    shown = fetch_label_history(db, hide_test=True)
    assert jobs(shown) == ["100001", "100002"]
    assert all(not r.test_mode for r in shown)


def test_window_and_hide_test_combine(db):
    assert jobs(fetch_label_history(db, since_days=90, hide_test=True)) == ["100001"]


def test_no_filters_returns_everything_so_nothing_is_ever_lost(db):
    assert len(fetch_label_history(db)) == 14 == count_label_history(db)


def test_count_always_agrees_with_the_list(db):
    for kwargs in (
        {}, {"since_days": 90}, {"hide_test": True}, {"since_days": 90, "hide_test": True},
        {"since_days": 30, "sscc_contains": "0001"}, {"job_number": "100002"}, {"date": "260505", "hide_test": True},
    ):
        assert count_label_history(db, **kwargs) == len(fetch_label_history(db, **kwargs)), kwargs


# --- the window ------------------------------------------------------------------------------------------

def _find_treeview(widget):
    for child in widget.winfo_children():
        if child.winfo_class() == "Treeview":
            return child
        found = _find_treeview(child)
        if found is not None:
            return found


def _button(widget, text):
    for child in widget.winfo_children():
        if child.winfo_class() in ("TButton", "Button") and child.cget("text") == text:
            return child
        found = _button(child, text)
        if found is not None:
            return found


@pytest.fixture
def history(app, db, monkeypatch):
    monkeypatch.setattr(app.settings, "local_db_file", str(db))
    monkeypatch.setattr(app.settings, "demo_mode", False)
    app._show_history()
    win = app.winfo_children()[-1]
    win.update()
    tree = _find_treeview(win)
    yield win, tree, win.history_controls
    win.destroy()


def listed_jobs(tree):
    return sorted({tree.item(i, "values")[1] for i in tree.get_children()})


def status(controls):
    return str(controls["status"].cget("text"))


def test_the_default_list_is_the_last_90_days_of_real_labels(history):
    win, tree, c = history
    assert c["period"].get() == "Last 90 days" and c["hide_test"].get() is True
    assert listed_jobs(tree) == ["100001"] and len(tree.get_children()) == 5


def test_the_status_line_says_how_many_are_hidden_and_why(history):
    win, tree, c = history
    text = status(c)
    assert "Showing 5 of 14 label row(s)" in text
    assert "3 older than 90 days" in text and "6 test label(s)" in text  # 3 old real; 4 + 2 test
    assert "Show all history" in text


def test_choosing_a_longer_period_shows_the_older_real_labels(history):
    win, tree, c = history
    c["period"].set("Last year")
    c["period_combo"].event_generate("<<ComboboxSelected>>")
    win.update()
    assert listed_jobs(tree) == ["100001", "100002"] and len(tree.get_children()) == 8
    assert "older than" not in status(c)  # nothing real is hidden any more


def test_unticking_hide_test_labels_shows_recent_test_labels(history):
    win, tree, c = history
    c["hide_check"].invoke()
    win.update()
    assert c["hide_test"].get() is False
    assert listed_jobs(tree) == ["100001", "100003"]


def test_show_all_history_removes_both_limits_and_says_nothing_is_hidden(history):
    win, tree, c = history
    c["show_all"].invoke()
    win.update()
    assert c["period"].get() == "All history" and c["hide_test"].get() is False
    assert len(tree.get_children()) == 14
    assert status(c) == "14 label row(s)"


def test_an_old_shipped_label_is_found_by_its_sscc_even_though_the_list_hides_it(history):
    """The rework case: a box comes back long after it shipped."""
    win, tree, c = history
    old_sscc = build_sscc(PREFIX, "0", 11)
    assert old_sscc not in {tree.item(i, "values")[6] for i in tree.get_children()}  # not in the plain list

    c["sscc"].set(old_sscc)
    win.update()

    assert [tree.item(i, "values")[6] for i in tree.get_children()] == [old_sscc]
    assert tree.item(tree.get_children()[0], "values")[1] == "100002"
    assert "found searching all history" in status(c)


def test_the_filter_controls_grey_out_while_searching_and_come_back_after(history):
    win, tree, c = history
    c["sscc"].set("0001")
    win.update()
    assert str(c["period_combo"].cget("state")) == "disabled"
    assert str(c["hide_check"].cget("state")) == "disabled"
    assert str(c["show_all"].cget("state")) == "disabled"

    c["sscc"].set("")
    win.update()
    assert str(c["period_combo"].cget("state")) == "readonly"
    assert str(c["hide_check"].cget("state")) == "normal"
    assert listed_jobs(tree) == ["100001"]  # back to the plain list


def test_a_test_label_can_still_be_found_while_hide_test_is_ticked(history):
    win, tree, c = history
    assert c["hide_test"].get() is True
    c["sscc"].set("TEST-SSCC-00003")
    win.update()
    assert [tree.item(i, "values")[6] for i in tree.get_children()] == ["TEST-SSCC-00003"]
    assert "test labels included" in status(c)


def test_searching_by_job_number_also_covers_all_history(history):
    win, tree, c = history
    c["job"].set("100002")  # a job from 200 days ago
    _button(win, "Search / Refresh").invoke()
    win.update()
    assert listed_jobs(tree) == ["100002"] and len(tree.get_children()) == 3


def test_viewing_never_deletes_anything(history, db):
    win, tree, c = history
    for action in (lambda: c["show_all"].invoke(), lambda: c["hide_check"].invoke(),
                   lambda: c["period"].set("Last 30 days")):
        action()
        win.update()
    assert count_label_history(db) == 14
