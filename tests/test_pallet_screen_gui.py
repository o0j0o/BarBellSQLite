import pytest

from src.db.local_store import fetch_label_history, find_carton_by_sscc, record_generation_run
from src.labels import LabelRow
from src.sscc import SSCCGenerator


def _find_treeview(widget, exclude=()):
    """Same helper as test_barbell_gui.py's, but with an exclude list since
    the Pallet screen has only one Treeview - included here so this module
    doesn't need to import a private helper from another test file."""
    for child in widget.winfo_children():
        if child.winfo_class() == "Treeview" and child not in exclude:
            return child
        found = _find_treeview(child, exclude)
        if found is not None:
            return found
    return None


def _entries(widget):
    result = []
    for child in widget.winfo_children():
        if child.winfo_class() in ("TEntry", "Entry"):
            result.append(child)
        result.extend(_entries(child))
    return result


def _buttons(widget):
    result = []
    for child in widget.winfo_children():
        if child.winfo_class() in ("TButton", "Button"):
            result.append(child)
        result.extend(_buttons(child))
    return result


def _button(widget, text_contains):
    for b in _buttons(widget):
        if text_contains in b.cget("text"):
            return b
    raise AssertionError(f"no button containing {text_contains!r}")


def make_carton_row(sscc, job_number="122984", **overrides):
    defaults = dict(
        job_number=job_number, packing_slip_number="100495", customer_number="J00005",
        customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
        item_description="desc", quantity=10000, batch="12298447388",
        production_date="2026-03-23", sscc=sscc, gtin="00051096184921",
        package_index=1, label_copy_index=1,
    )
    defaults.update(overrides)
    return LabelRow(**defaults)


def seed_cartons(db_path, rows):
    record_generation_run(rows, units_per_package=10000, labels_per_package=1, test_mode=False, db_path=db_path)


@pytest.fixture
def pallet_win(app, tmp_path, monkeypatch):
    """Opens a fresh Pallet screen against an isolated local DB for one
    test, and closes it afterward."""
    db_path = tmp_path / "barbell.db"
    monkeypatch.setattr(app.settings, "local_db_file", str(db_path))
    monkeypatch.setattr(app.settings, "demo_mode", False)
    monkeypatch.setattr(app.settings, "output_dir", str(tmp_path / "output"))
    monkeypatch.setattr(app.settings, "gs1_company_prefix", "08600157112")
    monkeypatch.setattr(app.settings, "sscc_extension_digit", "0")
    state_file = tmp_path / "sscc_state.json"
    monkeypatch.setattr(app.settings, "sscc_state_file", str(state_file))
    # Mirrors a real, already-configured install (Setup's Initialize Counter) -
    # generate_pallet_label() defaults to the real SSCC path (pallet_test_mode
    # unchecked), which requires an initialized counter, same as the main
    # screen's Generate Labels already does.
    SSCCGenerator("08600157112", "0", state_file).initialize(start_at=0)
    monkeypatch.setattr("barbell_gui.winsound.MessageBeep", lambda *_a, **_k: None)

    before = set(app.winfo_children())
    app._show_pallet_screen()
    after = set(app.winfo_children())
    win = next(iter(after - before))
    win.update()
    yield win, db_path
    if win.winfo_exists():
        win.destroy()


def scan(win, text):
    entries = _entries(win)
    scan_entry = entries[1]  # expected-count entry, then scan entry
    # <Return> is a keyboard event - Tk only delivers it to a widget that
    # actually holds focus. Only the FIRST Toplevel created in a test run
    # gets real OS focus by default, so later windows need it forced, or
    # the synthetic event is silently never dispatched (no exception either).
    win.focus_force()
    scan_entry.focus_force()
    win.update()
    scan_entry.insert(0, text)
    scan_entry.event_generate("<Return>")
    win.update()


class TestScanEntryGating:
    def test_scan_entry_disabled_until_valid_count_entered(self, pallet_win):
        win, _ = pallet_win
        entries = _entries(win)
        count_entry, scan_entry = entries[0], entries[1]

        assert str(scan_entry.cget("state")) == "disabled"

        count_entry.insert(0, "3")
        win.update()
        assert str(scan_entry.cget("state")) == "normal"

    def test_zero_or_non_numeric_count_keeps_scan_disabled(self, pallet_win):
        win, _ = pallet_win
        entries = _entries(win)
        count_entry, scan_entry = entries[0], entries[1]

        count_entry.insert(0, "0")
        win.update()
        assert str(scan_entry.cget("state")) == "disabled"

        count_entry.delete(0, "end")
        count_entry.insert(0, "abc")
        win.update()
        assert str(scan_entry.cget("state")) == "disabled"


class TestScanning:
    def test_valid_scan_adds_row_and_updates_totals(self, pallet_win):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128", quantity=27000)])
        entries = _entries(win)
        entries[0].insert(0, "1")
        win.update()

        scan(win, "008600157112000128")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 1
        assert tree.item("008600157112000128", "values")[1] == "27000"

    def test_unknown_sscc_is_rejected_and_not_added(self, pallet_win):
        win, db_path = pallet_win
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        scan(win, "008600157112999996")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 0

    def test_duplicate_scan_is_rejected(self, pallet_win):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000128")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 1

    def test_batch_mismatch_is_rejected(self, pallet_win):
        win, db_path = pallet_win
        # Two different jobs, seeded separately - record_generation_run()
        # only upserts a jobs row for the job_number of the rows it's given.
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        seed_cartons(
            db_path,
            [make_carton_row("008600157112000296", batch="99999947388", job_number="999999")],
        )
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 1

    def test_count_reached_blocks_further_scans(self, pallet_win):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [make_carton_row("008600157112000128"), make_carton_row("008600157112000296")],
        )
        entries = _entries(win)
        entries[0].insert(0, "1")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 1

    def test_totals_reflect_scanned_count_and_summed_quantity(self, pallet_win):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [
                make_carton_row("008600157112000128", quantity=27000),
                make_carton_row("008600157112000296", quantity=7000),
            ],
        )
        entries = _entries(win)
        entries[0].insert(0, "2")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        # totals_label is the second-to-last-packed child before the tree_frame;
        # simplest robust check: search all label texts for the expected totals.
        texts = []

        def collect(w):
            if w.winfo_class() in ("TLabel", "Label"):
                texts.append(w.cget("text"))
            for c in w.winfo_children():
                collect(c)

        collect(win)
        assert any("Scanned 2 of 2 cartons" in t for t in texts)
        assert any("34,000" in t for t in texts)

    def test_warning_confirmed_adds_the_carton(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [
                make_carton_row("008600157112000128", production_date="2026-03-23"),
                make_carton_row("008600157112000296", production_date="2026-03-24"),
            ],
        )
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 2

    def test_warning_declined_discards_the_carton(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [
                make_carton_row("008600157112000128", production_date="2026-03-23"),
                make_carton_row("008600157112000296", production_date="2026-03-24"),
            ],
        )
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: False)
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 1  # only the first, un-warned scan


class TestRemoveAndClear:
    def test_remove_selected_removes_the_row(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()
        scan(win, "008600157112000128")

        tree = _find_treeview(win)
        tree.selection_set("008600157112000128")
        _button(win, "Remove Selected").invoke()
        win.update()

        assert len(tree.get_children()) == 0

    def test_clear_pallet_removes_everything(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [make_carton_row("008600157112000128"), make_carton_row("008600157112000296")],
        )
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()
        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        _button(win, "Clear Pallet").invoke()
        win.update()

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 0


class TestGenerate:
    def test_generate_creates_pallet_row_links_cartons_and_writes_csv(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(
            db_path,
            [
                make_carton_row("008600157112000128", quantity=27000),
                make_carton_row("008600157112000296", quantity=7000),
            ],
        )
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
        entries = _entries(win)
        entries[0].insert(0, "2")
        win.update()
        scan(win, "008600157112000128")
        scan(win, "008600157112000296")

        _button(win, "Generate Pallet Label").invoke()
        win.update()

        history = fetch_label_history(db_path, job_number="122984")
        pallet_rows = [r for r in history if r.label_type == "PALLET"]
        carton_rows = [r for r in history if r.label_type == "CARTON"]

        assert len(pallet_rows) == 2  # 2 identical copies
        assert pallet_rows[0].quantity == 34000
        assert pallet_rows[0].carton_count == 2
        assert all(r.pallet_sscc == pallet_rows[0].sscc for r in carton_rows)

        tree = _find_treeview(win)
        assert len(tree.get_children()) == 0  # screen cleared after success

    def test_generate_csv_filename_contains_pallet_and_job(self, pallet_win, monkeypatch, tmp_path):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128", quantity=27000)])
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: True)
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
        entries = _entries(win)
        entries[0].insert(0, "1")
        win.update()
        scan(win, "008600157112000128")

        _button(win, "Generate Pallet Label").invoke()
        win.update()

        history = fetch_label_history(db_path, job_number="122984")
        pallet_sscc = [r for r in history if r.label_type == "PALLET"][0].sscc

        output_dir = tmp_path / "output"
        csvs = list(output_dir.glob("Pallet_labels_122984_*.csv"))
        assert len(csvs) == 1
        assert pallet_sscc in csvs[0].name

    def test_generate_asks_confirmation_when_fewer_than_expected(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        calls = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda title, msg, **k: (calls.append(msg), True)[1]
        )
        monkeypatch.setattr("tkinter.messagebox.showinfo", lambda *a, **k: None)
        entries = _entries(win)
        entries[0].insert(0, "5")  # expecting 5, only scanning 1
        win.update()
        scan(win, "008600157112000128")

        _button(win, "Generate Pallet Label").invoke()
        win.update()

        assert any("Only 1 of 5" in c for c in calls)

    def test_generate_declined_fewer_than_expected_does_not_create_pallet(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        monkeypatch.setattr("tkinter.messagebox.askyesno", lambda *a, **k: False)
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()
        scan(win, "008600157112000128")

        _button(win, "Generate Pallet Label").invoke()
        win.update()

        history = fetch_label_history(db_path, job_number="122984")
        assert not any(r.label_type == "PALLET" for r in history)

    def test_generate_with_nothing_scanned_shows_error_not_crash(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        errors = []
        monkeypatch.setattr(
            "tkinter.messagebox.showerror", lambda title, msg, **k: errors.append(msg)
        )
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()

        _button(win, "Generate Pallet Label").invoke()

        assert len(errors) == 1


class TestPreview:
    def test_preview_does_not_touch_the_sscc_counter_or_database(self, pallet_win, monkeypatch, tmp_path):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        entries = _entries(win)
        entries[0].insert(0, "1")
        win.update()
        scan(win, "008600157112000128")

        from src.sscc import get_counter_status

        state_file = tmp_path / "sscc_state.json"
        before = get_counter_status(state_file).last_serial

        _button(win, "Preview Barcode").invoke()
        win.update()

        after = get_counter_status(state_file).last_serial
        assert after == before  # preview never advances the real counter

        history = fetch_label_history(db_path, job_number="122984")
        assert not any(r.label_type == "PALLET" for r in history)

        preview_windows = [w for w in win.winfo_children() if w.winfo_class() == "Toplevel"]
        assert len(preview_windows) == 1
        preview_windows[0].destroy()


class TestReturnToMainScreen:
    def test_return_with_unsaved_cartons_asks_confirmation(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        seed_cartons(db_path, [make_carton_row("008600157112000128")])
        entries = _entries(win)
        entries[0].insert(0, "5")
        win.update()
        scan(win, "008600157112000128")

        calls = []
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno", lambda title, msg, **k: (calls.append(msg), False)[1]
        )
        _button(win, "Return to Main Screen").invoke()

        assert len(calls) == 1
        assert win.winfo_exists()  # declined - window stays open

    def test_return_with_no_scans_closes_immediately(self, pallet_win, monkeypatch):
        win, db_path = pallet_win
        monkeypatch.setattr(
            "tkinter.messagebox.askyesno",
            lambda *a, **k: (_ for _ in ()).throw(AssertionError("should not be asked")),
        )
        _button(win, "Return to Main Screen").invoke()
        assert not win.winfo_exists()
