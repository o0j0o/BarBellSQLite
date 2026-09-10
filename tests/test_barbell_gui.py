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


def test_about_dialog_shows_version_and_build_date_from_version_module():
    """Guards against the About dialog drifting from src/version.py - the
    single source of truth - by hardcoding its own version string instead."""
    app = BarBellApp()
    try:
        app._show_about()
        about_window = app.winfo_children()[-1]  # the About Toplevel, just created
        texts = _all_label_texts(about_window)
        assert f"Version: {version_string()}" in texts
        assert f"Build date: {BUILD_DATE}" in texts
    finally:
        app.destroy()
