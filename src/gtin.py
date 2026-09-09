"""
GTIN validation/normalization for GTINs entered manually into BarBell (see
QUESTIONS.md #4 - Label Traxx has no confirmed GTIN column yet).
"""

from src.sscc import gs1_check_digit

VALID_GTIN_LENGTHS = (8, 12, 13, 14)


class InvalidGTINError(ValueError):
    pass


def normalize_gtin(raw: str) -> str:
    """
    Validate a GTIN and normalize it to 14 digits, zero-padding shorter valid
    forms (GTIN-8/12/13). Verifies the embedded GS1 check digit so a typo is
    caught here rather than printed on a label (see the CLC briefing's own
    "Incorrect GTIN on Label -> Traceability breakdown" risk).
    """
    digits = raw.strip()
    if not digits.isdigit():
        raise InvalidGTINError(f"GTIN must be all digits, got {raw!r}")
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
