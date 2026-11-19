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


@pytest.fixture(autouse=True)
def _pinned_today(monkeypatch):
    """The production-date rules (at most 7 days ahead, this year or last) depend on today's date, so
    every test sees the same "today" - the suite's sample dates (260323, 260925, 261104...) then stay
    valid whenever the tests are run. Tests of the rules themselves pass their own date."""
    import datetime

    import src.dates

    monkeypatch.setattr(src.dates, "today", lambda: datetime.date(2026, 11, 13))


@pytest.fixture(autouse=True)
def _fresh_guardrails(request):
    """The shared main window remembers the last job looked up (for the red 'labels have been generated'
    messages), and a test that looked up a job must not make the next test's Preview/Generate stop at the
    Product No. block. Cleared before every test that uses the shared window."""
    if "app" in request.fixturenames:
        window = request.getfixturevalue("app")
        window._looked_up_job = None
        window._guardrail_cleared_key = None
        window._refresh_guardrails()
    yield
