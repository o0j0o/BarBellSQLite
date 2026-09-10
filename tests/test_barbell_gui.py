import tkinter.font as tkfont
from tkinter import ttk

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


def test_gtin_entered_for_this_run_renders_digits_bold_rest_plain(app):
    """
    Item 1: only the GTIN digits on this line are bold - the prefix and the
    "(not saved to Label Traxx)" suffix stay in the normal label font, and
    the combined text must read exactly as before (no layout/wording change).
    """
    app._set_gtin_status_with_bold_digits(
        "GTIN entered for this run: ", "06291041500213", " (not saved to Label Traxx)"
    )
    children = app.gtin_status_label.winfo_children()
    assert [c.cget("text") for c in children] == [
        "GTIN entered for this run: ",
        "06291041500213",
        " (not saved to Label Traxx)",
    ]
    # combined text reads identically to the original single-label string
    assert "".join(c.cget("text") for c in children) == (
        "GTIN entered for this run: 06291041500213 (not saved to Label Traxx)"
    )

    prefix_label, digits_label, suffix_label = children
    assert str(digits_label.cget("font")) == str(app._bold_font)
    assert str(prefix_label.cget("font")) != str(app._bold_font)
    assert str(suffix_label.cget("font")) != str(app._bold_font)

    # family/size unchanged, only weight differs
    default_font = tkfont.nametofont(ttk.Style().lookup("TLabel", "font") or "TkDefaultFont")
    assert app._bold_font.actual("family") == default_font.actual("family")
    assert app._bold_font.actual("size") == default_font.actual("size")
    assert app._bold_font.actual("weight") == "bold"


def test_about_dialog_shows_version_and_build_date_from_version_module(app):
    """Guards against the About dialog drifting from src/version.py - the
    single source of truth - by hardcoding its own version string instead."""
    app._show_about()
    about_window = app.winfo_children()[-1]  # the About Toplevel, just created
    texts = _all_label_texts(about_window)
    assert f"Version: {version_string()}" in texts
    assert f"Build date: {BUILD_DATE}" in texts
    about_window.destroy()
