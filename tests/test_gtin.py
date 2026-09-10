import pytest

from src.gtin import (
    GTIN_SOURCE_LABEL_TRAXX,
    GTIN_SOURCE_MANUAL_EMPTY,
    GTIN_SOURCE_MANUAL_OVERRIDE,
    InvalidGTINError,
    classify_gtin_source,
    normalize_gtin,
)


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


def test_normalize_gtin_strips_leading_and_trailing_whitespace():
    assert normalize_gtin("  12345670  ") == "00000012345670"


def test_normalize_gtin_strips_internal_whitespace_too():
    """
    Real Product.BC_Start values in Label Traxx use spaces as UPC/EAN
    grouping separators, e.g. '0 51096 18492 1' - this is a real value
    pulled from the live database, and it's a genuinely valid UPC-A
    (verified check digit), so it must be accepted, not rejected as
    "non-numeric".
    """
    assert normalize_gtin("0 51096 18492 1") == "00051096184921"


def test_normalize_gtin_rejects_wrong_check_digit():
    with pytest.raises(InvalidGTINError, match="check digit"):
        normalize_gtin("12345671")  # last digit should be 0, not 1


def test_normalize_gtin_rejects_non_digit_characters():
    with pytest.raises(InvalidGTINError, match="all digits"):
        normalize_gtin("1234567O")  # letter O, not zero


def test_normalize_gtin_rejects_invalid_length():
    with pytest.raises(InvalidGTINError, match="8, 12, 13, or 14"):
        normalize_gtin("123456789")  # 9 digits - not a valid GTIN length


def test_normalize_gtin_rejects_invalid_length_after_stripping_real_short_value():
    """
    Another real Product.BC_Start value from the live database: '0 12061'
    despaces to '012061' - only 6 digits, an incomplete/garbage entry that
    must be caught, not silently accepted.
    """
    with pytest.raises(InvalidGTINError, match="8, 12, 13, or 14"):
        normalize_gtin("0 12061")


def test_normalize_gtin_rejects_empty_string():
    with pytest.raises(InvalidGTINError, match="empty"):
        normalize_gtin("")


def test_normalize_gtin_rejects_whitespace_only_string():
    with pytest.raises(InvalidGTINError, match="empty"):
        normalize_gtin("   ")


def test_normalize_gtin_rejects_none():
    with pytest.raises(InvalidGTINError, match="empty"):
        normalize_gtin(None)


# --- classify_gtin_source ---------------------------------------------------

def test_classify_source_label_traxx_when_used_matches_bc_start():
    """Covers both 'accepted the prefilled value' and 'retyped the identical
    value' - either way, nothing was actually changed from Label Traxx."""
    assert (
        classify_gtin_source("00051096184921", "00051096184921") == GTIN_SOURCE_LABEL_TRAXX
    )


def test_classify_source_manual_override_when_used_differs_from_bc_start():
    assert (
        classify_gtin_source("00051096184921", "00000012345670")
        == GTIN_SOURCE_MANUAL_OVERRIDE
    )


def test_classify_source_manual_empty_when_bc_start_was_none():
    """BC_Start was empty or itself invalid (get_product_info already turned
    that into gtin=None) - there was nothing to override."""
    assert classify_gtin_source(None, "00000012345670") == GTIN_SOURCE_MANUAL_EMPTY
