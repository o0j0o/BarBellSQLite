import pytest

from src.gtin import InvalidGTINError, normalize_gtin


def test_normalize_gtin_pads_valid_13_digit_gtin_to_14():
    # 4006381333931 is a widely-cited GS1 worked example (correct check digit 1)
    assert normalize_gtin("4006381333931") == "04006381333931"
    # 6291041500213 - another standard GS1 General Specifications worked example
    assert normalize_gtin("6291041500213") == "06291041500213"


def test_normalize_gtin_pads_valid_8_digit_gtin_to_14():
    # Built and check-digit-verified with the same algorithm independently
    # before writing this module - not copied from normalize_gtin itself.
    assert normalize_gtin("12345670") == "00000012345670"


def test_normalize_gtin_accepts_already_14_digit_gtin():
    assert normalize_gtin("00000012345670") == "00000012345670"


def test_normalize_gtin_strips_whitespace():
    assert normalize_gtin("  12345670  ") == "00000012345670"


def test_normalize_gtin_rejects_wrong_check_digit():
    with pytest.raises(InvalidGTINError, match="check digit"):
        normalize_gtin("12345671")  # last digit should be 0, not 1


def test_normalize_gtin_rejects_non_digit_characters():
    with pytest.raises(InvalidGTINError, match="all digits"):
        normalize_gtin("1234567O")  # letter O, not zero


def test_normalize_gtin_rejects_invalid_length():
    with pytest.raises(InvalidGTINError, match="8, 12, 13, or 14"):
        normalize_gtin("123456789")  # 9 digits - not a valid GTIN length
