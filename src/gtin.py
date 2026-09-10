"""
GTIN validation/normalization. Used both for the CLC-assigned GTIN sourced
from Product.BC_Start ("Barcode Start" in Label Traxx's own UI - see
src/labels.py::get_product_info) and anywhere else a GTIN string needs
checking.

BC_Start is free text in Label Traxx - nothing stops it holding rubbish, an
incomplete number, or the wrong thing entirely. Real values pulled from the
live database include human-readable UPC/EAN grouping spaces, e.g.
'0 51096 18492 1' - so whitespace is stripped throughout the value, not just
at the ends, before validating. Genuinely bad values (wrong length, bad
check digit, non-numeric) are common in this field in practice and must
block, not just warn - see the blocking rules in src/labels.py.
"""

from src.sscc import gs1_check_digit

VALID_GTIN_LENGTHS = (8, 12, 13, 14)


class InvalidGTINError(ValueError):
    pass


def normalize_gtin(raw: str | None) -> str:
    """
    Validate a GTIN and normalize it to 14 digits, zero-padding shorter valid
    forms (GTIN-8/12/13). Verifies the embedded GS1 check digit so a typo is
    caught here rather than printed on a label (see the CLC briefing's own
    "Incorrect GTIN on Label -> Traceability breakdown" risk).

    Whitespace is stripped throughout (not just at the ends) - real Label
    Traxx values use spaces as UPC/EAN grouping separators, e.g.
    '0 51096 18492 1'.
    """
    if raw is None:
        raise InvalidGTINError("GTIN is empty (no value)")

    digits = "".join(raw.split())
    if not digits:
        raise InvalidGTINError("GTIN is empty (no value)")
    if not digits.isdigit():
        raise InvalidGTINError(
            f"GTIN must be all digits (after removing whitespace), got {raw!r}"
        )
    if len(digits) not in VALID_GTIN_LENGTHS:
        raise InvalidGTINError(
            f"GTIN must be 8, 12, 13, or 14 digits, got {len(digits)} digits: {raw!r}"
        )

    body, check_digit = digits[:-1], digits[-1]
    expected = gs1_check_digit(body)
    if check_digit != expected:
        raise InvalidGTINError(
            f"GTIN check digit looks wrong: {raw!r} ends in {check_digit}, expected "
            f"{expected} - double-check for a typo before re-entering."
        )

    return digits.zfill(14)


# --- GTIN source classification, for audit logging (see src/audit.py) ------
#
# While allow_manual_gtin_override is True (the Beta default - see
# Settings.allow_manual_gtin_override), a GTIN can end up being used three
# ways, and every run's audit record says which:

GTIN_SOURCE_LABEL_TRAXX = "label_traxx"
GTIN_SOURCE_MANUAL_EMPTY = "manual_entry_empty_field"
GTIN_SOURCE_MANUAL_OVERRIDE = "manual_override"


def classify_gtin_source(bc_start_gtin: str | None, used_gtin: str) -> str:
    """
    bc_start_gtin: the validated, normalized GTIN from Product.BC_Start
    (None if it was empty or failed validation).
    used_gtin: the final, already-validated normalized GTIN actually used.

    Returns GTIN_SOURCE_LABEL_TRAXX if used_gtin matches BC_Start exactly
    (whether the user typed nothing, or retyped the same value, over the
    prefilled textbox - nothing was actually changed either way);
    GTIN_SOURCE_MANUAL_OVERRIDE if BC_Start had a valid value but a
    different one was used instead; otherwise GTIN_SOURCE_MANUAL_EMPTY
    (BC_Start was empty or itself invalid, so there was nothing to override).
    """
    if bc_start_gtin is not None and used_gtin == bc_start_gtin:
        return GTIN_SOURCE_LABEL_TRAXX
    if bc_start_gtin is not None and used_gtin != bc_start_gtin:
        return GTIN_SOURCE_MANUAL_OVERRIDE
    return GTIN_SOURCE_MANUAL_EMPTY
