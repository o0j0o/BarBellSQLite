import webbrowser

import pytest

from src.help_link import HELP_URL, resolve_help_url
from src.settings import Settings


def test_the_built_in_address_is_the_operator_guide():
    assert HELP_URL == "https://claude.ai/artifact/H5yXBB29Aq899C8i6eVfBu"


def test_no_override_means_the_built_in_address():
    assert resolve_help_url("") == HELP_URL
    assert resolve_help_url("   ") == HELP_URL
    assert resolve_help_url() == HELP_URL


def test_a_usable_http_or_https_override_is_used():
    assert resolve_help_url("https://intranet.example/barbell-guide") == "https://intranet.example/barbell-guide"
    assert resolve_help_url("  http://server/guide  ") == "http://server/guide"


@pytest.mark.parametrize(
    "unsafe",
    [
        "file:///C:/Windows/System32/calc.exe",
        "C:/Windows/System32/calc.exe",
        "calc.exe",
        "ftp://server/guide",
        "javascript:alert(1)",
        "https://has a space.example",
        "not a url",
    ],
)
def test_anything_that_is_not_a_plain_web_address_is_ignored(unsafe):
    """Help must never be a way to launch a file or a program."""
    assert resolve_help_url(unsafe) == HELP_URL


def test_help_url_setting_defaults_to_empty_so_the_built_in_address_applies():
    assert Settings().help_url == ""


def test_this_machine_has_a_default_web_browser_registered():
    """Not a unit test of our code: proves Python can find a browser here, which is
    what Help relies on. Opens nothing."""
    assert webbrowser.get() is not None
