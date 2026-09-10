import pytest

from barbell_gui import BarBellApp, check_setup_password
from src.settings import Settings
from src.version import BUILD_DATE, version_string


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


def test_about_dialog_shows_version_and_build_date_from_version_module(app):
    """Guards against the About dialog drifting from src/version.py - the
    single source of truth - by hardcoding its own version string instead."""
    app._show_about()
    about_window = app.winfo_children()[-1]  # the About Toplevel, just created
    texts = _all_label_texts(about_window)
    assert f"Version: {version_string()}" in texts
    assert f"Build date: {BUILD_DATE}" in texts
    about_window.destroy()
