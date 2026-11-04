from src.settings import Settings
from src.setup_access import (
    ADMIN_SETUP_PASSWORD,
    ADMIN_WELCOME_MESSAGE,
    STANDARD_SETUP_PASSWORD_DEFAULT,
    SetupAccessLevel,
    resolve_setup_access,
)


def test_standard_password_still_grants_standard_access():
    assert resolve_setup_access("change4GOOD", "change4GOOD") is SetupAccessLevel.Standard


def test_admin_password_grants_admin_access():
    assert resolve_setup_access("42Novell@1430$", "change4GOOD") is SetupAccessLevel.Admin


def test_anything_else_is_refused_including_near_misses_and_empty():
    for wrong in ("", "wrong", "Change4GOOD", "42novell@1430$", "42Novell@1430", "42Novell@1430$ ", " change4GOOD"):
        assert resolve_setup_access(wrong, "change4GOOD") is None, wrong


def test_standard_password_comes_from_settings_so_it_can_still_be_changed_there():
    assert resolve_setup_access("newpass", "newpass") is SetupAccessLevel.Standard
    assert resolve_setup_access("change4GOOD", "newpass") is None  # old default no longer valid
    assert resolve_setup_access("42Novell@1430$", "newpass") is SetupAccessLevel.Admin


def test_a_fresh_install_defaults_to_the_documented_standard_password():
    assert Settings().setup_password == STANDARD_SETUP_PASSWORD_DEFAULT == "change4GOOD"


def test_welcome_message_text_and_the_two_levels_exist():
    assert ADMIN_WELCOME_MESSAGE == "Welcome Greg"
    assert {level.name for level in SetupAccessLevel} == {"Standard", "Admin"}
    assert ADMIN_SETUP_PASSWORD != STANDARD_SETUP_PASSWORD_DEFAULT


def test_passwords_are_defined_in_exactly_one_source_file():
    """Both passwords live only in src/setup_access.py - not scattered
    through the code base (tests excluded: they have to know them)."""
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    offenders = []
    for path in list(root.glob("*.py")) + list((root / "src").rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        if path.name != "setup_access.py" and ("42Novell" in text or "change4GOOD" in text):
            offenders.append(path.name)
    assert offenders == []
