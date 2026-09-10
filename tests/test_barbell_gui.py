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
        assert "233458" in warnings[0][1]  # names the item
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
