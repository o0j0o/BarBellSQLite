import pytest

from barbell_gui import check_setup_password
from src.gs1 import build_contents_element_string
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


def test_title_bar_shows_version_from_version_module(app, monkeypatch):
    """Same guard as the About dialog's, for the title bar."""
    monkeypatch.setattr(app.settings, "demo_mode", False)
    app._apply_demo_mode_ui()
    assert app.title() == f"BarBell {version_string()}"

    monkeypatch.setattr(app.settings, "demo_mode", True)
    app._apply_demo_mode_ui()
    assert app.title() == f"BarBell {version_string()} - DEMO MODE"

    monkeypatch.setattr(app.settings, "demo_mode", False)
    app._apply_demo_mode_ui()


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
                batch="12298447388", production_date="260323", sscc="086001571120000001",
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
                item_description="desc", quantity=100, batch="batch", production_date="260323",
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

            assert app.title() == f"BarBell {version_string()} - DEMO MODE"
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

        assert app.title() == f"BarBell {version_string()}"
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
                item_description="desc", quantity=100, batch="batch", production_date="260916",
                sscc="TEST-SSCC-00001", gtin="00099999000016", package_index=1, label_copy_index=1,
            )
        ]

        out_path = app._write_csv(rows, "DEMO-1001", "DEMO-PS-5001", test_mode=True, demo_mode=True)

        assert out_path.name == "DEMO_carton_jwn_labels_TEST.csv"  # never the real name a Print Station reads
        assert out_path.exists()

    def test_write_csv_has_no_demo_prefix_when_demo_mode_is_false(self, app, tmp_path, monkeypatch):
        from src.labels import LabelRow

        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path))
        rows = [
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="260323",
                sscc="086001571120000001", gtin="00051096184921", package_index=1, label_copy_index=1,
            )
        ]

        out_path = app._write_csv(rows, "122984", "100495", test_mode=False, demo_mode=False)

        assert out_path.name == "carton_jwn_labels.csv"  # the one fixed file BarTender Print Station reads


CHECKED, UNCHECKED = "☑", "☐"


def _all_buttons(widget):
    """Every ttk button anywhere under widget - the History window's buttons
    sit in two rows (filters, then actions on the checked rows)."""
    found = []
    for child in widget.winfo_children():
        if child.winfo_class() == "TButton":
            found.append(child)
        found.extend(_all_buttons(child))
    return found


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
                item_description="desc", quantity=100, batch="batch", production_date="260323",
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
        search_button = [
            b for b in _all_buttons(win)
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
        search_button = [
            b for b in _all_buttons(win)
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

        export_button = [
            b for b in _all_buttons(win)
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

        csv_files = list((tmp_path / "output").glob("*.csv"))
        assert [f.name for f in csv_files] == ["carton_jwn_labels.csv"]  # reprints use the fixed file too
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

        export_button = [
            b for b in _all_buttons(win)
            if b.winfo_class() in ("TButton", "Button") and "Reprint" in b.cget("text")
        ][0]
        export_button.invoke()

        assert len(info_calls) == 1  # "nothing selected" message
        assert len(confirm_calls) == 0  # never got as far as asking to confirm
        assert not (tmp_path / "output").exists()

        win.destroy()


class TestHistorySsccSearchAndScrolling:
    def _seed(self, db_path, ssccs):
        from src.db.local_store import record_generation_run
        from src.labels import LabelRow

        rows = [
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="260323",
                sscc=sscc, gtin="00051096184921", package_index=i, label_copy_index=1,
            )
            for i, sscc in enumerate(ssccs, start=1)
        ]
        record_generation_run(
            rows, units_per_package=100, labels_per_package=1, test_mode=False, db_path=db_path
        )

    def _open(self, app, tmp_path, monkeypatch, ssccs):
        db_path = tmp_path / "barbell.db"
        self._seed(db_path, ssccs)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        return win, _find_treeview(win)

    def _sscc_entry(self, win):
        entries = [
            w for w in win.winfo_children()[0].winfo_children()
            if w.winfo_class() in ("TEntry", "Entry")
        ]
        return entries[2]  # Job No, Date, then SSCC

    def test_typing_in_sscc_box_filters_live_with_no_button_press(self, app, tmp_path, monkeypatch):
        ssccs = ["008600157112000000108", "008600157112000000115", "008600157112000001234"]
        win, tree = self._open(app, tmp_path, monkeypatch, ssccs)
        assert len(tree.get_children()) == 3

        entry = self._sscc_entry(win)
        entry.insert(0, "1234")  # a sequence-only fragment, no company prefix
        win.update()
        assert [tree.item(i, "values")[6] for i in tree.get_children()] == ["008600157112000001234"]

        entry.delete(0, "end")  # clearing the box restores everything
        win.update()
        assert len(tree.get_children()) == 3

        win.destroy()

    def test_sscc_box_updates_after_every_keystroke(self, app, tmp_path, monkeypatch):
        ssccs = ["008600157112000000108", "008600157112000000115"]
        win, tree = self._open(app, tmp_path, monkeypatch, ssccs)
        entry = self._sscc_entry(win)

        entry.insert("end", "0000001")  # matches both
        assert len(tree.get_children()) == 2
        entry.insert("end", "08")  # now only "...000000108"
        assert len(tree.get_children()) == 1

        win.destroy()

    def test_clear_filters_also_clears_the_sscc_box(self, app, tmp_path, monkeypatch):
        win, tree = self._open(app, tmp_path, monkeypatch, ["AAA1", "BBB2"])
        entry = self._sscc_entry(win)
        entry.insert(0, "AAA")
        assert len(tree.get_children()) == 1

        clear = [b for b in _all_buttons(win) if b.cget("text") == "Clear filters"][0]
        clear.invoke()
        win.update()

        assert entry.get() == ""
        assert len(tree.get_children()) == 2
        win.destroy()

    def test_grid_has_working_vertical_and_horizontal_scrollbars(self, app, tmp_path, monkeypatch):
        win, tree = self._open(app, tmp_path, monkeypatch, ["AAA1"])

        scrollbars = {
            str(w.cget("orient")): w
            for w in tree.master.winfo_children()
            if w.winfo_class() == "TScrollbar"
        }
        assert set(scrollbars) == {"vertical", "horizontal"}
        # both are gridded (visible), not pushed off-screen or unmanaged
        assert scrollbars["vertical"].grid_info() != {}
        assert scrollbars["horizontal"].grid_info() != {}
        # and both are actually hooked to the tree
        assert tree.cget("yscrollcommand")
        assert tree.cget("xscrollcommand")
        # columns don't shrink to fit - that's what makes horizontal scrolling possible
        assert not any(bool(int(tree.column(c, "stretch"))) for c in tree["columns"])

        win.destroy()


class TestConnectDsnSelection:
    """BarBellApp._connect() - which plant's Label Traxx to talk to. See
    tests/test_connect_dsn_selection.py for the CLI equivalent
    (generate_labels.connect())."""

    def test_connect_passes_label_traxx_dsn_through(self, app, monkeypatch):
        from src.db.readonly_connection import ReadOnlyConnection

        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr(app.settings, "label_traxx_dsn", "LCJ JAM")

        conn = app._connect()
        assert isinstance(conn, ReadOnlyConnection)
        assert conn._dsn == "LCJ JAM"

    def test_connect_falls_back_to_env_when_label_traxx_dsn_unset(self, app, monkeypatch):
        monkeypatch.setenv("LT_DSN", "LT64")
        monkeypatch.setenv("LT_USER", "designer")
        monkeypatch.setenv("LT_PASSWORD", "unused")
        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr(app.settings, "label_traxx_dsn", "")

        conn = app._connect()
        assert conn._dsn == "LT64"

    def test_connect_returns_demo_connection_when_demo_mode_is_on(self, app, monkeypatch):
        from src.demo_data import DemoConnection

        monkeypatch.setattr(app.settings, "demo_mode", True)
        monkeypatch.setattr(app.settings, "label_traxx_dsn", "LCJ JAM")

        assert isinstance(app._connect(), DemoConnection)


class TestVoidPallet:
    def _seed_pallet(self, db_path):
        from src.db.local_store import create_pallet, record_generation_run
        from src.labels import LabelRow

        cartons = [
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=10000, batch="12298447388",
                production_date="260323", sscc=sscc, gtin="00051096184921",
                package_index=i, label_copy_index=1,
            )
            for i, sscc in enumerate(["008600157112000128", "008600157112000296"], start=1)
        ]
        record_generation_run(
            cartons, units_per_package=10000, labels_per_package=1, test_mode=False, db_path=db_path
        )
        create_pallet(
            carton_ssccs=[c.sscc for c in cartons], job_number="122984", quantity=20000,
            production_date="260323", packing_slip_number="100495",
            pallet_sscc="008600157112099999", carton_count=2, db_path=db_path,
        )
        return [c.sscc for c in cartons]

    def test_void_pallet_marks_void_and_frees_cartons(self, app, tmp_path, monkeypatch):
        from src.db.local_store import fetch_label_history

        db_path = tmp_path / "barbell.db"
        carton_ssccs = self._seed_pallet(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)

        pallet_iids = [
            iid for iid in tree.get_children() if tree.item(iid, "values")[6] == "008600157112099999"
        ]
        assert len(pallet_iids) == 2  # both print copies
        for iid in pallet_iids:
            _click_checkbox_cell(tree, iid)
        win.update()

        void_button = [b for b in _all_buttons(win) if b.cget("text") == "Void Pallet"][0]
        void_button.invoke()
        win.update()

        history = fetch_label_history(db_path, job_number="122984")
        pallet_rows = [r for r in history if r.label_type == "PALLET"]
        carton_rows = [r for r in history if r.label_type == "CARTON"]
        assert all(r.status == "void" for r in pallet_rows)
        assert all(r.pallet_sscc is None for r in carton_rows)

        win.destroy()

    def test_void_pallet_rejects_mixed_carton_and_pallet_selection(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_pallet(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        errors = []
        monkeypatch.setattr(
            "tkinter.messagebox.showerror", lambda title, msg, **k: errors.append(msg)
        )
        confirms = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda *a, **k: (confirms.append(1), True)[1]
        )

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)

        # check one pallet row and one carton row
        pallet_iid = next(
            iid for iid in tree.get_children() if tree.item(iid, "values")[6] == "008600157112099999"
        )
        carton_iid = next(
            iid for iid in tree.get_children() if tree.item(iid, "values")[6] == "008600157112000128"
        )
        _click_checkbox_cell(tree, pallet_iid)
        _click_checkbox_cell(tree, carton_iid)
        win.update()

        void_button = [b for b in _all_buttons(win) if b.cget("text") == "Void Pallet"][0]
        void_button.invoke()

        assert len(errors) == 1
        assert len(confirms) == 0  # never got as far as confirming

        win.destroy()

    def test_void_pallet_does_nothing_when_none_selected(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        self._seed_pallet(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        info_calls = []
        monkeypatch.setattr(
            "tkinter.messagebox.showinfo", lambda title, msg, **k: info_calls.append(msg)
        )

        app._show_history()
        win = app.winfo_children()[-1]
        win.update()

        void_button = [b for b in _all_buttons(win) if b.cget("text") == "Void Pallet"][0]
        void_button.invoke()

        assert len(info_calls) == 1

        win.destroy()


class TestPalletReport:
    PALLET_SSCC = "008600157112099999"

    def _setup(self, app, tmp_path, monkeypatch):
        db_path = tmp_path / "barbell.db"
        TestVoidPallet()._seed_pallet(db_path)
        monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
        monkeypatch.setattr(app.settings, "demo_mode", False)
        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
        opened = []
        monkeypatch.setattr(type(app), "_open_file", staticmethod(lambda path: opened.append(path)))
        return db_path, opened

    def _open_history(self, app):
        app._show_history()
        win = app.winfo_children()[-1]
        win.update()
        tree = _find_treeview(win)
        report_button = [
            b for b in _all_buttons(win) if b.cget("text") == "Pallet Report (PDF)"
        ][0]
        return win, tree, report_button

    def _iids_for(self, tree, sscc, column=6):
        return [iid for iid in tree.get_children() if tree.item(iid, "values")[column] == sscc]

    def test_report_for_checked_pallet_row_is_written_and_opened(self, app, tmp_path, monkeypatch):
        _, opened = self._setup(app, tmp_path, monkeypatch)
        win, tree, report_button = self._open_history(app)

        _click_checkbox_cell(tree, self._iids_for(tree, self.PALLET_SSCC)[0])
        win.update()
        report_button.invoke()

        expected = tmp_path / "output" / f"Pallet_report_{self.PALLET_SSCC}.pdf"
        assert expected.read_bytes().startswith(b"%PDF")
        assert opened == [expected]
        win.destroy()

    @pytest.mark.parametrize(
        "dsn, expected",
        [("LT64", "Caribbean Label Crafts Ltd."), ("LCJ JAM", "Label Crafts Jamaica Ltd.")],
    )
    def test_report_carries_the_active_plants_company_name(
        self, app, tmp_path, monkeypatch, dsn, expected
    ):
        import barbell_gui

        _, opened = self._setup(app, tmp_path, monkeypatch)
        monkeypatch.setattr(app.settings, "label_traxx_dsn", dsn)
        seen = []
        real = barbell_gui.build_pallet_report_pdf
        monkeypatch.setattr(
            barbell_gui, "build_pallet_report_pdf",
            lambda report, out_path, **kw: (seen.append(kw.get("company_name")), real(report, out_path, **kw))[1],
        )
        win, tree, report_button = self._open_history(app)

        _click_checkbox_cell(tree, self._iids_for(tree, self.PALLET_SSCC)[0])
        win.update()
        report_button.invoke()

        assert seen == [expected]
        win.destroy()

    def test_checking_a_carton_on_the_pallet_resolves_to_its_pallet(self, app, tmp_path, monkeypatch):
        _, opened = self._setup(app, tmp_path, monkeypatch)
        win, tree, report_button = self._open_history(app)

        _click_checkbox_cell(tree, self._iids_for(tree, "008600157112000128")[0])
        win.update()
        report_button.invoke()

        assert len(opened) == 1
        assert opened[0].name == f"Pallet_report_{self.PALLET_SSCC}.pdf"
        win.destroy()

    def test_nothing_checked_shows_info_and_writes_nothing(self, app, tmp_path, monkeypatch):
        _, opened = self._setup(app, tmp_path, monkeypatch)
        infos = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: infos.append(msg))
        win, _, report_button = self._open_history(app)

        report_button.invoke()

        assert len(infos) == 1
        assert opened == []
        assert not (tmp_path / "output").exists()
        win.destroy()

    def test_carton_not_on_a_pallet_is_rejected(self, app, tmp_path, monkeypatch):
        from src.db.local_store import void_pallet

        db_path, opened = self._setup(app, tmp_path, monkeypatch)
        void_pallet(self.PALLET_SSCC, db_path)  # frees both cartons
        errors = []
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: errors.append(msg))
        win, tree, report_button = self._open_history(app)

        _click_checkbox_cell(tree, self._iids_for(tree, "008600157112000128")[0])
        win.update()
        report_button.invoke()

        assert len(errors) == 1
        assert opened == []
        win.destroy()

    def test_voided_pallet_shows_error(self, app, tmp_path, monkeypatch):
        from src.db.local_store import void_pallet

        db_path, opened = self._setup(app, tmp_path, monkeypatch)
        void_pallet(self.PALLET_SSCC, db_path)
        errors = []
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: errors.append((title, msg)))
        win, tree, report_button = self._open_history(app)

        _click_checkbox_cell(tree, self._iids_for(tree, self.PALLET_SSCC)[0])
        win.update()
        report_button.invoke()

        assert len(errors) == 1
        assert errors[0][0] == "Pallet report failed"
        assert "voided" in errors[0][1]
        assert opened == []
        win.destroy()


class TestGenerateCsvWriteFailure:
    """A CSV write failure (locked file, permissions, disk full, etc.) must
    never be silent - the DB row is already logged by this point, so at
    minimum the operator needs to know the CSV didn't happen."""

    def test_generate_shows_error_and_does_not_crash_when_csv_write_fails(
        self, app, tmp_path, monkeypatch
    ):
        from src.db.local_store import fetch_label_history
        from src.demo_data import DemoConnection
        from src.labels import get_product_info, list_packing_slip_line_items

        monkeypatch.setattr(app.settings, "demo_mode", True)
        monkeypatch.setattr(app.settings, "local_db_file", str(tmp_path / "barbell.db"))
        monkeypatch.setattr(app.settings, "demo_db_file", str(tmp_path / "barbell_demo.db"))
        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
        monkeypatch.setattr(app.settings, "demo_audit_log_file", str(tmp_path / "demo_audit.jsonl"))

        conn = DemoConnection()
        line_item = list_packing_slip_line_items(conn, "DEMO-PS-5001")[0]
        product = get_product_info(conn, line_item.product_number)

        app.job_number_var.set("DEMO-1001")
        app._selected_line_item = line_item
        app._product = product
        app.gtin_entry_var.set(product.gtin_raw or "")
        app.units_per_package_var.set("27000")
        app.labels_per_package_var.set("1")
        app.production_date_var.set("260925")
        app.test_mode_var.set(True)

        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        errors = []
        monkeypatch.setattr(
            "tkinter.messagebox.showerror", lambda title, msg: errors.append((title, msg))
        )
        monkeypatch.setattr(
            "src.label_files.write_flat_csv",
            lambda rows, out_path: (_ for _ in ()).throw(
                PermissionError("[Errno 13] Permission denied")
            ),
        )

        app._generate()  # must not raise

        assert len(errors) == 1
        assert errors[0][0] == "CSV write failed"
        assert "Permission denied" in errors[0][1]

        history = fetch_label_history(app.settings.demo_db_file, job_number="DEMO-1001")
        assert len(history) > 0  # DB write still succeeded despite the CSV failure


# --- 1.1.7: menu bar, Setup access levels, Test Mode setting, date format, logos ---------------


def _menu_labels(menu):
    last = menu.index("end")
    return [menu.entrycget(i, "label") for i in range(last + 1)] if last is not None else []


def _invoke_menu(menu, label):
    for i, name in enumerate(_menu_labels(menu)):
        if name == label:
            menu.invoke(i)
            return
    raise AssertionError(f"no menu entry {label!r} in {_menu_labels(menu)}")


def _home_menu(app):
    return app.nametowidget(app._menubar.entrycget(0, "menu"))


def _help_menu(app):
    return app.nametowidget(app._menubar.entrycget(1, "menu"))


def _all_button_texts(widget):
    texts = []
    for child in widget.winfo_children():
        if child.winfo_class() in ("TButton", "Button"):
            texts.append(child.cget("text"))
        texts.extend(_all_button_texts(child))
    return texts


class TestMenuBar:
    def test_top_level_items_are_home_then_help(self, app):
        assert _menu_labels(app._menubar) == ["Home", "Help"]

    def test_home_menu_holds_setup_back_up_now_and_exit(self, app):
        assert _menu_labels(_home_menu(app)) == ["Job Report...", "Setup", "Back Up Now", "Exit"]

    def test_help_menu_has_help_contacts_about(self, app):
        assert _menu_labels(_help_menu(app)) == ["Help", "Contacts", "About"]

    def test_main_form_no_longer_has_an_about_button(self, app):
        assert "About" not in _all_button_texts(app)

    def test_contacts_opens_its_own_screen(self, app):
        before = set(app.winfo_children())
        _invoke_menu(_help_menu(app), "Contacts")
        new = next(iter(set(app.winfo_children()) - before))
        assert new.title() == "Contacts"
        new.destroy()

    def test_about_menu_item_opens_the_existing_about_screen(self, app):
        before = set(app.winfo_children())
        _invoke_menu(_help_menu(app), "About")
        about = next(iter(set(app.winfo_children()) - before))
        assert about.title() == "About BarBell"
        assert f"Version: {version_string()}" in _all_label_texts(about)
        about.destroy()


class TestExitMenu:
    def test_yes_closes_the_app(self, app, monkeypatch):
        closed, asked = [], []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda title, msg, **k: (asked.append(msg), True)[1]
        )
        monkeypatch.setattr(app, "destroy", lambda: closed.append(True))

        _invoke_menu(_home_menu(app), "Exit")

        assert asked == ["Are you sure you want to exit BarBell?"]
        assert closed == [True]

    def test_no_returns_to_the_app_with_nothing_changed(self, app, monkeypatch):
        closed = []
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: False)
        monkeypatch.setattr(app, "destroy", lambda: closed.append(True))
        windows_before = set(app.winfo_children())
        job_before = app.job_number_var.get()

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == []
        assert set(app.winfo_children()) == windows_before
        assert app.job_number_var.get() == job_before


class TestSetupEntryAndPasswords:
    """The Setup menu item and the About screen's Setup button must go through
    the same code (BarBellApp._prompt_setup_password) and behave identically."""

    STANDARD = "change4GOOD"
    ADMIN = "42Novell@1430$"

    def _arrange(self, app, monkeypatch, typed):
        popen_calls, infos, errors = [], [], []
        monkeypatch.setattr("barbell_gui.load_settings", lambda *a, **k: Settings(setup_password=self.STANDARD))
        monkeypatch.setattr("barbell_gui.simpledialog.askstring", lambda *a, **k: typed)
        monkeypatch.setattr("barbell_gui.subprocess.Popen", lambda args, **k: popen_calls.append(args))
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: infos.append(msg))
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: errors.append(msg))
        return popen_calls, infos, errors

    def _via_menu(self, app):
        _invoke_menu(_home_menu(app), "Setup")

    def _via_about_button(self, app):
        before = set(app.winfo_children())
        app._show_about()
        about = next(iter(set(app.winfo_children()) - before))
        next(
            b for b in _all_buttons(about) if b.cget("text") == "Setup..."
        ).invoke()
        about.destroy()

    @pytest.mark.parametrize("entry", ["_via_menu", "_via_about_button"])
    def test_standard_password_opens_setup_as_standard_without_welcome(self, app, monkeypatch, entry):
        popen_calls, infos, errors = self._arrange(app, monkeypatch, self.STANDARD)

        getattr(self, entry)(app)

        assert len(popen_calls) == 1
        assert popen_calls[0][-2:] == ["--access-level", "standard"]
        assert popen_calls[0][1].endswith("setup_gui.py")
        assert infos == [] and errors == []  # no welcome, no error

    @pytest.mark.parametrize("entry", ["_via_menu", "_via_about_button"])
    def test_admin_password_opens_setup_as_admin_and_welcomes_greg(self, app, monkeypatch, entry):
        popen_calls, infos, errors = self._arrange(app, monkeypatch, self.ADMIN)

        getattr(self, entry)(app)

        assert len(popen_calls) == 1
        assert popen_calls[0][-2:] == ["--access-level", "admin"]
        assert infos == ["Welcome Greg"]
        assert errors == []

    @pytest.mark.parametrize("entry", ["_via_menu", "_via_about_button"])
    def test_wrong_password_is_refused_and_never_echoed(self, app, monkeypatch, entry):
        popen_calls, infos, errors = self._arrange(app, monkeypatch, "not-the-password")

        getattr(self, entry)(app)

        assert popen_calls == [] and infos == []
        assert errors == ["That password is incorrect."]
        assert "not-the-password" not in errors[0]

    @pytest.mark.parametrize("entry", ["_via_menu", "_via_about_button"])
    def test_cancelling_the_prompt_does_nothing(self, app, monkeypatch, entry):
        popen_calls, infos, errors = self._arrange(app, monkeypatch, None)

        getattr(self, entry)(app)

        assert popen_calls == [] and infos == [] and errors == []

    def test_neither_password_is_logged_or_shown_on_success_or_failure(self, app, monkeypatch, caplog):
        import logging

        caplog.set_level(logging.DEBUG)
        for typed in (self.STANDARD, self.ADMIN, "wrong"):
            popen_calls, infos, errors = self._arrange(app, monkeypatch, typed)
            self._via_menu(app)
            for message in infos + errors:
                assert self.STANDARD not in message and self.ADMIN not in message
        assert self.STANDARD not in caplog.text and self.ADMIN not in caplog.text

    def test_the_existing_check_setup_password_function_is_unchanged(self):
        assert check_setup_password("change4GOOD", Settings(setup_password="change4GOOD")) is True
        assert check_setup_password("42Novell@1430$", Settings(setup_password="change4GOOD")) is False


class TestDisableTestModeCheckboxSetting:
    def _apply(self, app, monkeypatch, demo, disable):
        monkeypatch.setattr(app.settings, "demo_mode", demo)
        monkeypatch.setattr(app.settings, "disable_test_mode_checkbox", disable)
        app.test_mode_var.set(True)  # start from a ticked box so "turned off" is observable
        app._apply_demo_mode_ui()

    def test_checked_setting_turns_the_box_off_and_disables_it(self, app, monkeypatch):
        self._apply(app, monkeypatch, demo=False, disable=True)
        assert app.test_mode_var.get() is False
        assert str(app.test_mode_checkbox.cget("state")) == "disabled"
        self._apply(app, monkeypatch, demo=False, disable=False)  # leave the shared app tidy

    def test_unchecked_setting_leaves_the_box_usable_as_before(self, app, monkeypatch):
        self._apply(app, monkeypatch, demo=False, disable=False)
        assert str(app.test_mode_checkbox.cget("state")) == "normal"
        assert app.test_mode_var.get() is True  # not forced either way

    def test_demo_mode_still_forces_test_mode_on_and_locked(self, app, monkeypatch):
        self._apply(app, monkeypatch, demo=True, disable=True)
        assert app.test_mode_var.get() is True
        assert str(app.test_mode_checkbox.cget("state")) == "disabled"
        self._apply(app, monkeypatch, demo=False, disable=False)


class TestProductionDateEntry:
    def _prime(self, app, tmp_path, monkeypatch, production_date):
        from src.demo_data import DemoConnection
        from src.labels import get_product_info, list_packing_slip_line_items

        monkeypatch.setattr(app.settings, "demo_mode", True)
        monkeypatch.setattr(app.settings, "demo_db_file", str(tmp_path / "barbell_demo.db"))
        monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
        monkeypatch.setattr(app.settings, "demo_audit_log_file", str(tmp_path / "demo_audit.jsonl"))
        conn = DemoConnection()
        line_item = list_packing_slip_line_items(conn, "DEMO-PS-5001")[0]
        product = get_product_info(conn, line_item.product_number)
        app.job_number_var.set("DEMO-1001")
        app._selected_line_item = line_item
        app._product = product
        app.gtin_entry_var.set(product.gtin_raw or "")
        app.units_per_package_var.set("27000")
        app.labels_per_package_var.set("1")
        app.production_date_var.set(production_date)
        app.test_mode_var.set(True)
        errors = []
        monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, msg, **k: errors.append((title, msg)))
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        return errors

    def test_yymmdd_is_accepted_and_flows_to_database_csv_and_barcode(self, app, tmp_path, monkeypatch):
        import csv

        from src.db.local_store import fetch_label_history

        errors = self._prime(app, tmp_path, monkeypatch, "261104")
        app._generate()

        assert errors == []
        history = fetch_label_history(app.settings.demo_db_file, job_number="DEMO-1001")
        assert history and {r.production_date for r in history} == {"261104"}
        csv_files = list((tmp_path / "output").glob("*.csv"))
        assert len(csv_files) == 1
        with open(csv_files[0], newline="", encoding="utf-8") as f:
            assert {row["ProductionDate"] for row in csv.DictReader(f)} == {"261104"}
        info = app._gather_preview_inputs()
        assert "(11)261104" in build_contents_element_string(
            info["gtin"], info["production_date"], info["first_package_qty"], info["batch"]
        )

    @pytest.mark.parametrize("bad", ["2026-11-04", "26-11-04", "261304", "261132", "26110", "abcdef", ""])
    def test_anything_but_a_real_yymmdd_date_is_refused(self, app, tmp_path, monkeypatch, bad):
        errors = self._prime(app, tmp_path, monkeypatch, bad)

        assert app._gather_preview_inputs() is None

        assert len(errors) == 1 and errors[0][0] == "Invalid date"
        assert "YYMMDD" in errors[0][1]

    def test_the_entry_and_history_filter_are_labelled_yymmdd(self, app):
        assert any("Production date (YYMMDD" in t for t in _all_label_texts(app))


class TestHeaderLogos:
    """The main screen's header shows ONLY the "Making Ideas Take Shape!"
    wordmark - the CLC and LCJ logos now live on the About screen."""

    def test_only_the_making_ideas_logo_is_in_the_header(self, app):
        assert app._header_making_ideas_logo is not None
        assert set(app._header_logo_widgets) == {"center", "making_ideas"}
        assert not hasattr(app, "_header_clc_logo") and not hasattr(app, "_header_lcj_logo")

    def test_tagline_keeps_its_aspect_ratio_and_fits_the_existing_header_height(self, app):
        from PIL import Image

        import barbell_gui as g

        photo = app._header_making_ideas_logo
        with Image.open(g.MAKING_IDEAS_LOGO_PATH) as source:
            source_ratio = source.width / source.height
        assert abs(photo.width() / photo.height() - source_ratio) / source_ratio < 0.02
        assert photo.height() == g.HEADER_MAKING_IDEAS_HEIGHT_PX <= g.HEADER_BARBELL_HEIGHT_PX

    def test_tagline_sits_at_the_right_inside_the_header_clear_of_the_barbell_logo(self, app):
        app.update()
        tag = app._header_logo_widgets["making_ideas"]
        center = app._header_logo_widgets["center"]
        header = tag.master

        assert tag.winfo_y() >= 0 and tag.winfo_y() + tag.winfo_height() <= header.winfo_height()
        assert tag.winfo_x() > center.winfo_x() + center.winfo_width()  # no overlap with BarBell logo
        assert abs((tag.winfo_x() + tag.winfo_width()) - header.winfo_width()) <= 12  # at the right edge

    def test_no_company_logos_remain_on_the_main_screen(self, app):
        images = set()

        def walk(widget):
            for child in widget.winfo_children():
                if child.winfo_class() == "Toplevel":
                    continue
                try:
                    name = str(child.cget("image"))
                except Exception:  # noqa: BLE001 - not every widget has an image option
                    name = ""
                if name:
                    images.add(name)
                walk(child)

        walk(app)
        # BarBell wordmark + tagline only
        assert len(images) == 2


class TestAboutScreenLogos:
    def test_about_shows_both_company_logos_side_by_side(self, app):
        app.update()
        before = set(app.winfo_children())
        app._show_about()
        about = next(iter(set(app.winfo_children()) - before))
        about.update()

        assert app._about_lcj_logo is not None and app._about_clc_logo is not None
        def image_name(label):  # ttk labels report their image as a 1-tuple
            value = label.cget("image")
            return str(value[0]) if isinstance(value, tuple) and value else str(value)

        photo_names = {str(app._about_clc_logo), str(app._about_lcj_logo)}
        labels = []

        def collect(widget):
            for child in widget.winfo_children():
                if child.winfo_class() == "TLabel" and image_name(child) in photo_names:
                    labels.append(child)
                collect(child)

        collect(about)
        assert len(labels) == 2
        clc = next(l for l in labels if image_name(l) == str(app._about_clc_logo))
        lcj = next(l for l in labels if image_name(l) == str(app._about_lcj_logo))
        assert clc.winfo_x() + clc.winfo_width() <= lcj.winfo_x()  # CLC then LCJ, in one row
        assert abs(clc.winfo_y() - lcj.winfo_y()) <= 12
        about.destroy()

    def test_lcj_logo_on_about_keeps_its_aspect_ratio(self, app):
        from PIL import Image

        import barbell_gui as g

        with Image.open(g.LCJ_LOGO_PATH) as source:
            source_ratio = source.width / source.height
        photo = app._about_lcj_logo
        assert abs(photo.width() / photo.height() - source_ratio) / source_ratio < 0.02
        assert photo.width() <= g.ABOUT_LCJ_TARGET_PX


class TestBackupOnExit:
    """Closing BarBell (Home > Exit, or the window's X) backs up first when a
    backup directory is set in Setup."""

    def _arrange(self, app, tmp_path, monkeypatch, backup_dir="set", demo=False):
        from pathlib import Path

        from src.db.local_store import record_generation_run
        from src.labels import LabelRow
        from src.sscc import _atomic_write_last_serial

        live = tmp_path / "live"
        live.mkdir()
        db = live / "barbell.db"
        record_generation_run(
            [LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="JWN", product_no="47388", item_number="233458", item_description="d",
                quantity=1000, batch="12298447388", production_date="260323",
                sscc="008600157112000012", gtin="00051096184921", package_index=1, label_copy_index=1,
            )],
            units_per_package=1000, labels_per_package=1, test_mode=False, db_path=db,
        )
        _atomic_write_last_serial(live / "sscc_state.json", 12)
        monkeypatch.setattr(app.settings, "local_db_file", str(db))
        monkeypatch.setattr(app.settings, "sscc_state_file", str(live / "sscc_state.json"))
        monkeypatch.setattr(app.settings, "jamaica_sscc_state_file", str(live / "sscc_state_jamaica.json"))
        monkeypatch.setattr(app.settings, "audit_log_file", str(live / "audit.jsonl"))
        monkeypatch.setattr(app.settings, "demo_mode", demo)
        backups = tmp_path / "backups"
        monkeypatch.setattr(app.settings, "backup_dir", str(backups) if backup_dir == "set" else "")
        closed = []
        monkeypatch.setattr(app, "destroy", lambda: closed.append(True))
        return backups, closed

    def test_exit_yes_backs_up_then_closes(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == [True]
        made = sorted(p.name for p in backups.iterdir())
        assert len(made) == 1 and made[0].startswith("barbell_backup_")
        assert (backups / made[0] / "barbell.db").is_file()
        assert (backups / made[0] / "sscc_state.json").is_file()

    def test_exit_no_neither_backs_up_nor_closes(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: False)

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == [] and not backups.exists()

    def test_closing_with_the_window_x_also_backs_up(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)

        app.tk.call(app.protocol("WM_DELETE_WINDOW"))  # what the X button runs

        assert closed == [True]
        assert len(list(backups.iterdir())) == 1

    def test_no_backup_directory_means_no_backup_and_a_normal_close(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch, backup_dir="")
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == [True] and not backups.exists()

    def test_demo_mode_never_backs_up(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch, demo=True)
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == [True] and not backups.exists()

    def test_a_failed_backup_asks_before_closing_and_no_keeps_the_app_open(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)
        (tmp_path / "blocker").write_text("a file, not a folder")
        monkeypatch.setattr(app.settings, "backup_dir", str(tmp_path / "blocker" / "sub"))
        prompts = []

        def ask(title, message, **k):
            prompts.append(title)
            return title != "Backup failed"  # yes to "are you sure", NO to "exit anyway?"

        monkeypatch.setattr("tkinter.messagebox.askyesno", ask)

        _invoke_menu(_home_menu(app), "Exit")

        assert prompts == ["Exit BarBell", "Backup failed"]
        assert closed == []  # the user said no to exiting without a backup

    def test_a_failed_backup_can_still_be_overridden_so_you_are_never_trapped(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)
        (tmp_path / "blocker").write_text("a file, not a folder")
        monkeypatch.setattr(app.settings, "backup_dir", str(tmp_path / "blocker" / "sub"))
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)

        _invoke_menu(_home_menu(app), "Exit")

        assert closed == [True]

    def test_back_up_now_makes_a_backup_and_reports_it(self, app, tmp_path, monkeypatch):
        backups, closed = self._arrange(app, tmp_path, monkeypatch)
        infos = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: infos.append(msg))

        _invoke_menu(_home_menu(app), "Back Up Now")
        _invoke_menu(_home_menu(app), "Back Up Now")  # nothing changed in between

        assert closed == []  # backing up never closes the app
        assert len(list(backups.iterdir())) == 1
        assert infos[0].startswith("Backed up to") and "Nothing has changed" in infos[1]

    def test_back_up_now_without_a_backup_directory_points_to_setup(self, app, tmp_path, monkeypatch):
        backups, _ = self._arrange(app, tmp_path, monkeypatch, backup_dir="")
        infos = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: infos.append(msg))

        _invoke_menu(_home_menu(app), "Back Up Now")

        assert len(infos) == 1 and "Setup" in infos[0]
        assert not backups.exists()


class TestCartonContentsAIs:
    """The main screen's Preview and confirmation boxes are about CARTON
    labels, so they show the carton form: (01) GTIN and (37) count - the same
    as the printed carton label. (The pallet screen keeps (02)/(37).)"""

    def _label_texts(self, widget):
        texts = []
        for child in widget.winfo_children():
            if child.winfo_class() in ("TLabel", "Label"):
                texts.append(str(child.cget("text")))
            texts.extend(self._label_texts(child))
        return texts

    def test_preview_barcode_window_shows_ai_01_and_ai_37(self, app, tmp_path, monkeypatch):
        TestProductionDateEntry()._prime(app, tmp_path, monkeypatch, "260505")
        before = set(app.winfo_children())

        app._preview_barcode()

        window = next(iter(set(app.winfo_children()) - before))
        texts = self._label_texts(window)
        contents = [t for t in texts if t.startswith("(0") and "(37)" in t]
        assert len(contents) == 1
        assert contents[0].startswith("(01)00099999000016(11)260505(37)27000(10)")
        assert not any(t.startswith("(02)") for t in texts)
        window.destroy()

    def test_generate_confirmation_box_shows_ai_01_and_ai_37(self, app, tmp_path, monkeypatch):
        TestProductionDateEntry()._prime(app, tmp_path, monkeypatch, "260505")
        seen = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda title, message, **k: (seen.append(message), False)[1]
        )  # look at the message, then decline so nothing is generated

        app._generate()

        assert len(seen) == 1
        contents_line = next(line for line in seen[0].splitlines() if "Contents:" in line)
        assert "(01)00099999000016(11)260505(37)27000(10)" in contents_line
        assert "(02)" not in contents_line


class TestHelpOpensTheGuide:
    """Help > Help opens the BarBell Operator Guide in the web browser."""

    def test_help_opens_the_built_in_guide_address(self, app, monkeypatch):
        from src.help_link import HELP_URL

        opened = []
        monkeypatch.setattr("barbell_gui.webbrowser.open", lambda url, *a, **k: (opened.append(url), True)[1])
        monkeypatch.setattr(app.settings, "help_url", "")
        windows_before = set(app.winfo_children())

        _invoke_menu(_help_menu(app), "Help")

        assert opened == [HELP_URL]
        assert set(app.winfo_children()) == windows_before  # no placeholder window any more

    def test_a_machine_can_point_help_somewhere_else(self, app, monkeypatch):
        opened = []
        monkeypatch.setattr("barbell_gui.webbrowser.open", lambda url, *a, **k: (opened.append(url), True)[1])
        monkeypatch.setattr(app.settings, "help_url", "https://intranet.example/barbell-guide")

        _invoke_menu(_help_menu(app), "Help")

        assert opened == ["https://intranet.example/barbell-guide"]

    def test_an_unsafe_override_is_ignored(self, app, monkeypatch):
        from src.help_link import HELP_URL

        opened = []
        monkeypatch.setattr("barbell_gui.webbrowser.open", lambda url, *a, **k: (opened.append(url), True)[1])
        monkeypatch.setattr(app.settings, "help_url", "file:///C:/Windows/System32/calc.exe")

        _invoke_menu(_help_menu(app), "Help")

        assert opened == [HELP_URL]

    @pytest.mark.parametrize("failure", ["returns_false", "raises"])
    def test_if_no_browser_opens_the_address_is_shown_and_copied(self, app, monkeypatch, failure):
        from src.help_link import HELP_URL

        def fake_open(url, *a, **k):
            if failure == "raises":
                raise OSError("no browser")
            return False

        monkeypatch.setattr("barbell_gui.webbrowser.open", fake_open)
        monkeypatch.setattr(app.settings, "help_url", "")
        shown = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: shown.append((title, msg)))

        _invoke_menu(_help_menu(app), "Help")

        assert len(shown) == 1 and shown[0][0] == "Help"
        assert HELP_URL in shown[0][1] and "couldn't open a web browser" in shown[0][1]
        assert app.clipboard_get() == HELP_URL

    def test_a_working_browser_shows_no_message(self, app, monkeypatch):
        monkeypatch.setattr("barbell_gui.webbrowser.open", lambda *a, **k: True)
        shown = []
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda title, msg, **k: shown.append(msg))

        _invoke_menu(_help_menu(app), "Help")

        assert shown == []
