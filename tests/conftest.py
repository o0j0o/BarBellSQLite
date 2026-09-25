import pytest

from barbell_gui import BarBellApp


@pytest.fixture(scope="session")
def app():
    """
    One shared BarBellApp (one Tk root) for every GUI-dependent test in the
    whole suite - Tkinter doesn't reliably support creating a fresh Tk()
    root per test/module within the same process (a second root after the
    first is destroyed can leave the Tcl interpreter in a broken state).
    Session-scoped (not module-scoped) so every test file that needs a live
    BarBellApp - test_barbell_gui.py, test_pallet_screen_gui.py - shares
    this single root instead of each trying to create its own.
    """
    app = BarBellApp()
    yield app
    app.destroy()
