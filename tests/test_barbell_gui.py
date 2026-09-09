from barbell_gui import check_setup_password
from src.settings import Settings


def test_check_setup_password_accepts_correct_password():
    settings = Settings(setup_password="change4GOOD")
    assert check_setup_password("change4GOOD", settings) is True


def test_check_setup_password_rejects_wrong_password():
    settings = Settings(setup_password="change4GOOD")
    assert check_setup_password("wrong", settings) is False
    assert check_setup_password("", settings) is False
    assert check_setup_password("Change4GOOD", settings) is False  # case-sensitive
