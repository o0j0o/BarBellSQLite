import datetime
import re
from pathlib import Path

from src.version import BETA, BUILD_DATE, MAJOR, MINOR, PATCH, version_string

CHANGELOG_PATH = Path(__file__).resolve().parent.parent / "CHANGELOG.md"


def test_version_string_includes_beta_suffix_while_in_beta():
    assert BETA is True  # sanity check the fixture below still matches reality
    assert version_string() == f"{MAJOR}.{MINOR}.{PATCH} Beta"


def test_version_components_are_non_negative_ints():
    assert isinstance(MAJOR, int) and MAJOR >= 0
    assert isinstance(MINOR, int) and MINOR >= 0
    assert isinstance(PATCH, int) and PATCH >= 0


def test_build_date_is_a_valid_iso_date():
    datetime.date.fromisoformat(BUILD_DATE)  # raises if malformed


def test_changelog_top_entry_matches_the_current_version():
    """
    Guards the "never hardcode the version in more than one place" rule -
    src/version.py is the source of truth, but CHANGELOG.md's most recent
    heading must always describe that exact version, so this catches a
    forgotten changelog entry.
    """
    text = CHANGELOG_PATH.read_text(encoding="utf-8")
    heading_lines = [line for line in text.splitlines() if line.startswith("## ")]
    assert heading_lines, "CHANGELOG.md has no version headings"

    top = heading_lines[0]
    match = re.match(r"## (\d+\.\d+\.\d+)( Beta)? - (\d{4}-\d{2}-\d{2})", top)
    assert match, f"Unexpected CHANGELOG.md heading format: {top!r}"

    changelog_version, changelog_beta, changelog_date = match.groups()
    assert changelog_version == f"{MAJOR}.{MINOR}.{PATCH}"
    assert bool(changelog_beta) == BETA
    assert changelog_date == BUILD_DATE
