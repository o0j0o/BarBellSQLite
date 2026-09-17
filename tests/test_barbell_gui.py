import pytest

from barbell_gui import BarBellApp, check_setup_password
from src.labels import ProductInfo
from src.settings import Settings
from src.version import BUILD_DATE, version_string

VALID_BC_START = "0 51096 18492 1"
VALID_GTIN = "00051096184921"


def make_product(gtin=None, gtin_raw=None, gtin_error=None, item_number="233458", prod_num="47388"):
    return ProductInfo(
        prod_num=prod_num,
        item_number=item_number,
        description="233458 - JWN White O/P Rum B 750Ml USA - PS",
        gtin=gtin,
        gtin_raw=gtin_raw,
        gtin_error=gtin_error,
    )


def test_check_setup_password_accepts_correct_password():
    settings = Settings(setup_password="change4GOOD")
    assert check_setup_password("change4GOOD", settings) is True


def test_check_setup_password_rejects_wrong_password():
    settings = Settings(setup_password="change4GOOD")
    assert check_setup_password("wrong", settings) is False
    assert check_setup_password("", settings) is False
    assert check_setup_password("Change4GOOD", settings) is False  # case-sensitive


def _all_label_texts(widget):
    texts = []
    for child in widget.winfo_children():
        if child.winfo_class() in ("TLabel", "Label"):
            texts.append(child.cget("text"))
        texts.extend(_all_label_texts(child))
    return texts


@pytest.fixture(scope="module")
def app():
    """
    One shared BarBellApp (one Tk root) for every GUI-dependent test in this
    module - Tkinter doesn't reliably support creating a fresh Tk() root per
    test within the same process (a second root after the first is destroyed
    can leave the Tcl interpreter in a broken state).
    """
    app = BarBellApp()
    yield app
    app.destroy()


def test_set_gtin_status_text_plain(app):
    app._set_gtin_status_text("GTIN on file: 00051096184921")
    assert app.gtin_status_label.cget("text") == "GTIN on file: 00051096184921"
    assert str(app.gtin_status_label.cget("foreground")) == ""


def test_set_gtin_status_text_error_renders_red(app):
    """
    Item 3: an invalid/missing GTIN is a blocking error, shown in red so it
    stays visibly distinct from the normal "GTIN on file" state even after
    the accompanying messagebox is dismissed.
    """
    app._set_gtin_status_text("BLOCKED - item 233458: GTIN is empty (no value)", error=True)
    assert str(app.gtin_status_label.cget("foreground")) == "red"

    # and it's not sticky - a later plain call clears the red
    app._set_gtin_status_text("GTIN on file: 00051096184921")
    assert str(app.gtin_status_label.cget("foreground")) == ""


class TestApplyGtinEntryStateForProduct:
    """Amendment: manual GTIN entry is always available in Beta, not just
    when BC_Start is empty (Settings.allow_manual_gtin_override)."""

    def test_prefills_with_raw_bc_start_and_enables_entry_when_override_allowed(self, app):
        app.settings.allow_manual_gtin_override = True
        product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)

        app._apply_gtin_entry_state_for_product(product)

        assert app.gtin_status_label.cget("text") == f"GTIN on file: {VALID_GTIN}"
        assert app.gtin_entry_var.get() == VALID_BC_START
        assert str(app.gtin_entry.cget("state")) == "normal"

    def test_disables_entry_when_override_not_allowed_and_bc_start_valid(self, app):
        """Once allow_manual_gtin_override is turned off, a valid BC_Start
        becomes authoritative again and the field locks - no code change."""
        app.settings.allow_manual_gtin_override = False
        product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)

        app._apply_gtin_entry_state_for_product(product)

        assert str(app.gtin_entry.cget("state")) == "disabled"
        app.settings.allow_manual_gtin_override = True  # restore for other tests

    def test_blank_bc_start_leaves_textbox_blank_and_always_enabled(self, app, monkeypatch):
        warnings = []
        monkeypatch.setattr(
            "tkinter.messagebox.showwarning", lambda title, msg: warnings.append((title, msg))
        )
        app.settings.allow_manual_gtin_override = False  # even when off - nothing to lock to
        product = make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)")

        app._apply_gtin_entry_state_for_product(product)

        assert app.gtin_entry_var.get() == ""
        assert str(app.gtin_entry.cget("state")) == "normal"
        assert len(warnings) == 1
        assert "47388" in warnings[0][1]  # names the P/N
        assert product.description in warnings[0][1]
        assert "BLOCKED" in app.gtin_status_label.cget("text") or "No GTIN" in app.gtin_status_label.cget("text")
        app.settings.allow_manual_gtin_override = True  # restore


class TestResolveGtin:
    def test_accepts_value_matching_bc_start_without_confirmation(self, app, monkeypatch):
        def _fail_if_called(*a, **k):
            raise AssertionError("askyesno should not be called when nothing changed")

        monkeypatch.setattr("tkinter.messagebox.askyesno", _fail_if_called)
        app._product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)
        app.gtin_entry_var.set(VALID_BC_START)  # unchanged from prefill

        assert app._resolve_gtin() == VALID_GTIN

    def test_accepts_manual_entry_when_bc_start_empty_without_confirmation(self, app, monkeypatch):
        def _fail_if_called(*a, **k):
            raise AssertionError("askyesno should not be called - nothing to override")

        monkeypatch.setattr("tkinter.messagebox.askyesno", _fail_if_called)
        app._product = make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)")
        app.gtin_entry_var.set("00000012345670")

        assert app._resolve_gtin() == "00000012345670"

    def test_requires_confirmation_when_value_differs_from_bc_start(self, app, monkeypatch):
        calls = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno",
            lambda title, msg: (calls.append((title, msg)), True)[1],
        )
        app._product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)
        app.gtin_entry_var.set("00000012345670")  # different from BC_Start

        result = app._resolve_gtin()

        assert result == "00000012345670"
        assert len(calls) == 1
        assert VALID_GTIN in calls[0][1]  # shows the Label Traxx value
        assert "00000012345670" in calls[0][1]  # shows the value being used instead

    def test_declining_override_confirmation_blocks(self, app, monkeypatch):
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda title, msg: False)
        app._product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)
        app.gtin_entry_var.set("00000012345670")

        assert app._resolve_gtin() is None

    def test_invalid_entry_blocks_with_error(self, app, monkeypatch):
        errors = []
        monkeypatch.setattr(
            "tkinter.messagebox.showerror", lambda title, msg: errors.append((title, msg))
        )
        app._product = make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START)
        app.gtin_entry_var.set("not-a-gtin")

        assert app._resolve_gtin() is None
        assert len(errors) == 1

    def test_blank_entry_blocks_never_proceeds_without_a_gtin(self, app, monkeypatch):
        errors = []
        monkeypatch.setattr(
            "tkinter.messagebox.showerror", lambda title, msg: errors.append((title, msg))
        )
        app._product = make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)")
        app.gtin_entry_var.set("")

        assert app._resolve_gtin() is None
        assert len(errors) == 1


def test_about_dialog_shows_version_and_build_date_from_version_module(app):
    """Guards against the About dialog drifting from src/version.py - the
    single source of truth - by hardcoding its own version string instead."""
    app._show_about()
    about_window = app.winfo_children()[-1]  # the About Toplevel, just created
    texts = _all_label_texts(about_window)
    assert f"Version: {version_string()}" in texts
    assert f"Build date: {BUILD_DATE}" in texts
    about_window.destroy()


def _find_treeview(widget):
    for child in widget.winfo_children():
        if child.winfo_class() == "Treeview":
            return child
        found = _find_treeview(child)
        if found is not None:
            return found
    return None


class TestHistoryViewer:
    def test_opens_and_lists_rows_from_the_local_db(self, app, tmp_path, monkeypatch):
        from src.db.local_store import record_generation_run
        from src.labels import LabelRow

        db_path = tmp_path / "barbell.db"
        rows = [
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="233458 - JWN White O/P Rum B 750Ml USA - PS", quantity=27000,
                batch="12298447388", production_date="2026-03-23", sscc="086001571120000001",
                gtin="00051096184921", package_index=1, label_copy_index=1,
            )
        ]
        record_generation_run(
            rows, units_per_package=27000, labels_per_package=1, test_mode=False, db_path=db_path
        )
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)  # read local_db_file, not demo_db_file

        app._show_history()
        history_window = app.winfo_children()[-1]
        tree = _find_treeview(history_window)

        assert tree is not None
        assert len(tree.get_children()) == 1
        values = tree.item(tree.get_children()[0], "values")
        assert values[0] == "☐"  # unchecked checkbox, nothing selected yet
        assert values[1] == "122984"  # job_number
        assert values[6] == "086001571120000001"  # sscc

        history_window.destroy()

    def test_job_number_filter_narrows_results(self, app, tmp_path, monkeypatch):
        from src.db.local_store import record_generation_run
        from src.labels import LabelRow

        db_path = tmp_path / "barbell.db"

        def make_row(job_number, sscc):
            return LabelRow(
                job_number=job_number, packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="2026-03-23",
                sscc=sscc, gtin="00051096184921", package_index=1, label_copy_index=1,
            )

        record_generation_run(
            [make_row("111111", "sscc-a")], units_per_package=100, labels_per_package=1,
            test_mode=False, db_path=db_path,
        )
        record_generation_run(
            [make_row("222222", "sscc-b")], units_per_package=100, labels_per_package=1,
            test_mode=False, db_path=db_path,
        )
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)  # read local_db_file, not demo_db_file

        app._show_history()
        history_window = app.winfo_children()[-1]
        tree = _find_treeview(history_window)
        assert len(tree.get_children()) == 2  # no filter yet - both runs shown

        entries = [
            w for w in history_window.winfo_children()[0].winfo_children()
            if w.winfo_class() in ("TEntry", "Entry")
        ]
        job_filter_entry = entries[0]
        job_filter_entry.insert(0, "111111")

        search_buttons = [
            w for w in history_window.winfo_children()[0].winfo_children()[-1].winfo_children()
            if w.winfo_class() in ("TButton", "Button") and w.cget("text") == "Search / Refresh"
        ]
        search_buttons[0].invoke()

        assert len(tree.get_children()) == 1
        values = tree.item(tree.get_children()[0], "values")
        assert values[1] == "111111"  # job_number (index 0 is the checkbox column)

        history_window.destroy()


class TestDemoMode:
    """Demo Mode is read once at startup (self.settings), same as every
    other setting - _apply_demo_mode_ui() is the pure widget-update half of
    that, factored out so it's directly testable without restarting the app
    for each case. Every test restores demo_mode=False at the end since
    `app` is a module-scoped, shared Tk root."""

    def test_turning_demo_mode_on_shows_banner_and_locks_test_mode_on(self, app):
        app.settings.demo_mode = True
        try:
            app._apply_demo_mode_ui()

            assert app.title() == "BarBell - DEMO MODE"
            assert app.demo_banner.grid_info() != {}  # visible
            assert app.test_mode_var.get() is True
            assert str(app.test_mode_checkbox.cget("state")) == "disabled"
            assert "DEMO-1001" in app.demo_hint_label.cget("text")
        finally:
            app.settings.demo_mode = False
            app._apply_demo_mode_ui()

    def test_turning_demo_mode_off_hides_banner_and_unlocks_test_mode(self, app):
        app.settings.demo_mode = True
        app._apply_demo_mode_ui()

        app.settings.demo_mode = False
        app._apply_demo_mode_ui()

        assert app.title() == "BarBell"
        assert app.demo_banner.grid_info() == {}  # hidden
        assert str(app.test_mode_checkbox.cget("state")) == "normal"
        assert app.demo_hint_label.cget("text") == ""

    def test_connect_returns_demo_connection_when_demo_mode_is_on(self, app):
        from src.demo_data import DemoConnection

        app.settings.demo_mode = True
        try:
            assert isinstance(app._connect(), DemoConnection)
        finally:
            app.settings.demo_mode = False

    def test_connect_returns_real_connection_when_demo_mode_is_off(self, app):
        from src.db.readonly_connection import ReadOnlyConnection

        app.settings.demo_mode = False
        assert isinstance(app._connect(), ReadOnlyConnection)

    def test_write_csv_prefixes_demo_filename_and_keeps_test_suffix(self, app, tmp_path, monkeypatch):
        from src.labels import LabelRow

        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path))
        rows = [
            LabelRow(
                job_number="DEMO-1001", packing_slip_number="DEMO-PS-5001", customer_number="DEMO-C01",
                customer_name="Acme (DEMO)", product_no="DEMO-P100", item_number="D-100",
                item_description="desc", quantity=100, batch="batch", production_date="2026-09-16",
                sscc="TEST-SSCC-00001", gtin="00099999000016", package_index=1, label_copy_index=1,
            )
        ]

        out_path = app._write_csv(rows, "DEMO-1001", "DEMO-PS-5001", test_mode=True, demo_mode=True)

        assert out_path.name == "DEMO_labels_DEMO-1001_DEMO-PS-5001_TEST.csv"
        assert out_path.exists()

    def test_write_csv_has_no_demo_prefix_when_demo_mode_is_false(self, app, tmp_path, monkeypatch):
        from src.labels import LabelRow

        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path))
        rows = [
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="2026-03-23",
                sscc="086001571120000001", gtin="00051096184921", package_index=1, label_copy_index=1,
            )
        ]

        out_path = app._write_csv(rows, "122984", "100495", test_mode=False, demo_mode=False)

        assert out_path.name == "labels_122984_100495.csv"


CHECKED, UNCHECKED = "☑", "☐"


def _click_checkbox_cell(tree, iid):
    """Simulates the user clicking a row's checkbox cell - bbox() needs a
    real geometry pass first, hence win.update() (not just update_idletasks())
    in every test that uses this."""
    bbox = tree.bbox(iid, "#1")
    assert bbox, f"row {iid!r} isn't rendered/visible - call win.update() first"
    x, y = bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2
    tree.event_generate("<Button-1>", x=x, y=y)


def _click_select_all_heading(tree):
    """The heading's command= callback is registered as a Tcl command -
    invoking it directly is more reliable than clicking header pixels."""
    tree.tk.call(tree.heading("sel", "command"))


class TestHistoryReprintSelection:
    def _seed_two_jobs(self, db_path):
        from src.db.local_store import record_generation_run
        from src.labels import LabelRow

        def make_row(job_number, sscc):
            return LabelRow(
                job_number=job_number, packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="2026-03-23",
                sscc=sscc, gtin="00051096184921", package_index=1, label_copy_index=1,
            )

        record_generation_run(
            [make_row("111111", "sscc-a"), make_row("111111", "sscc-b")],
            units_per_package=100, labels_per_package=1, test_mode=False, db_path=db_path,
        )
        record_generation_run(
            [make_row("222222", "sscc-c")],
            units_per_package=100, labels_per_package=1, test_mode=False, db_path=db_path,
        )

    def test_clicking_a_row_checkbox_toggles_only_that_row(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_two_jobs(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)
        children = tree.get_children()  # 3 rows, newest first

        _click_checkbox_cell(tree, children[0])
        win.update()

        assert tree.item(children[0], "values")[0] == CHECKED
        assert tree.item(children[1], "values")[0] == UNCHECKED
        assert tree.item(children[2], "values")[0] == UNCHECKED

        # clicking it again unchecks it
        _click_checkbox_cell(tree, children[0])
        win.update()
        assert tree.item(children[0], "values")[0] == UNCHECKED

        win.destroy()

    def test_select_all_applies_only_to_currently_filtered_rows(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_two_jobs(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)

        # Filter down to job 111111 (2 rows) before selecting all.
        entries = [
            w for w in win.winfo_children()[0].winfo_children()
            if w.winfo_class() in ("TEntry", "Entry")
        ]
        entries[0].insert(0, "111111")
        button_frame = win.winfo_children()[0].winfo_children()[-1]
        search_button = [
            b for b in button_frame.winfo_children()
            if b.winfo_class() in ("TButton", "Button") and b.cget("text") == "Search / Refresh"
        ][0]
        search_button.invoke()
        win.update()

        filtered_children = tree.get_children()
        assert len(filtered_children) == 2  # only job 111111's rows

        _click_select_all_heading(tree)
        win.update()

        assert tree.heading("sel", "text") == CHECKED
        assert all(tree.item(iid, "values")[0] == CHECKED for iid in filtered_children)

        # clicking select-all again deselects everything
        _click_select_all_heading(tree)
        win.update()
        assert tree.heading("sel", "text") == UNCHECKED
        assert all(tree.item(iid, "values")[0] == UNCHECKED for iid in filtered_children)

        win.destroy()

    def test_new_search_clears_stale_selections(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_two_jobs(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)

        _click_select_all_heading(tree)
        win.update()
        assert tree.heading("sel", "text") == CHECKED

        # Running Search/Refresh again (even with the same filter) must clear it.
        button_frame = win.winfo_children()[0].winfo_children()[-1]
        search_button = [
            b for b in button_frame.winfo_children()
            if b.winfo_class() in ("TButton", "Button") and b.cget("text") == "Search / Refresh"
        ][0]
        search_button.invoke()
        win.update()

        assert tree.heading("sel", "text") == UNCHECKED
        assert all(tree.item(iid, "values")[0] == UNCHECKED for iid in tree.get_children())

        win.destroy()

    def test_export_selected_writes_csv_and_logs_reprint_rows(self, app, tmp_path, monkeypatch):
        from src.db.local_store import fetch_label_history

        db_path = tmp_path / "barbell.db"
        self._seed_two_jobs(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)

        before = fetch_label_history(db_path)
        original_ids = sorted(r.id for r in before)

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)
        children = tree.get_children()  # 3 rows total

        _click_checkbox_cell(tree, children[0])
        _click_checkbox_cell(tree, children[1])
        win.update()

        button_frame = win.winfo_children()[0].winfo_children()[-1]
        export_button = [
            b for b in button_frame.winfo_children()
            if b.winfo_class() in ("TButton", "Button") and "Reprint" in b.cget("text")
        ][0]
        export_button.invoke()
        win.update()

        after = fetch_label_history(db_path)
        assert len(after) == len(before) + 2  # two new reprint rows, nothing removed

        reprints = [r for r in after if r.status == "reprint"]
        assert len(reprints) == 2
        assert {r.superseded_id for r in reprints} == {int(children[0]), int(children[1])}

        # originals must still be there, unchanged
        for original_id in original_ids:
            assert any(r.id == original_id and r.status == "original" for r in after)

        csv_files = list((tmp_path / "output").glob("reprint_*.csv"))
        assert len(csv_files) == 1
        with open(csv_files[0], newline="", encoding="utf-8") as f:
            content = f.read()
        assert content.count("\n") == 3  # header + 2 rows (+ trailing newline)

        win.destroy()

    def test_export_selected_does_nothing_when_none_checked(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_two_jobs(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))

        info_calls = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: info_calls.append(a))
        confirm_calls = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda *a, **k: confirm_calls.append(a) or True
        )

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()

        button_frame = win.winfo_children()[0].winfo_children()[-1]
        export_button = [
            b for b in button_frame.winfo_children()
            if b.winfo_class() in ("TButton", "Button") and "Reprint" in b.cget("text")
        ][0]
        export_button.invoke()

        assert len(info_calls) == 1  # "nothing selected" message
        assert len(confirm_calls) == 0  # never got as far as asking to confirm
        assert not (tmp_path / "output").exists()

        win.destroy()
