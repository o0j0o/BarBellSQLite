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

normalize_gtin14() is the ONE place a GTIN is validated or padded. Everything
that reads, stores, exports, shows or barcodes a GTIN goes through it (or
through checked_gtin14()/gtin14_or_none() below, which only wrap it) - no
other code builds or repairs a GTIN.

Why always 14 digits WITH the check digit: the BarTender template discards the
last digit and works the check digit out again itself, then insists on exactly
13 characters. 14 in -> 13 left, nothing to pad. And because BarTender would
quietly "correct" a wrong check digit, a GTIN that fails here must never reach
a CSV or a barcode - see write_flat_csv() in src/db/local_store.py.
"""

from src.sscc import gs1_check_digit

VALID_GTIN_LENGTHS = (12, 13, 14)


class InvalidGTINError(ValueError):
    pass


def normalize_gtin14(raw: str | None) -> str:
    """
    Validate a GTIN and return it as 14 digits including its check digit.

    Accepts 12, 13 or 14 digits (UPC-A, EAN-13, GTIN-14 - a GTIN-14 may carry
    an indicator digit 1-8 in front, e.g. 10636191036404, and is checked the
    same way). Shorter valid forms are left-padded with zeros: 636191036407 ->
    00636191036407. The GS1 mod-10 check digit (the last digit) is verified, so
    a typo is caught here rather than printed on a label.

    Spaces and hyphens are removed first - real Label Traxx values use spaces
    as UPC/EAN grouping separators, e.g. '0 51096 18492 1'. Anything else that
    is not a digit (a letter O typed for a zero, say) is refused, not removed:
    silently dropping it would turn a typo into a different, shorter number.
    """
    if raw is None:
        raise InvalidGTINError("GTIN is empty (no value)")

    digits = "".join(str(raw).split()).replace("-", "")
    if not digits:
        raise InvalidGTINError("GTIN is empty (no value)")
    if not (digits.isascii() and digits.isdigit()):
        raise InvalidGTINError(
            f"GTIN must be all digits (after removing spaces and hyphens), got {raw!r}"
        )
    if len(digits) not in VALID_GTIN_LENGTHS:
        raise InvalidGTINError(
            f"GTIN must be 12, 13 or 14 digits, got {len(digits)} digits: {raw!r}"
        )

    body, check_digit = digits[:-1], digits[-1]
    expected = gs1_check_digit(body)
    if check_digit != expected:
        raise InvalidGTINError(
            f"GTIN check digit looks wrong: {raw!r} ends in {check_digit}, expected "
            f"{expected} - double-check for a typo before re-entering."
        )

    return digits.zfill(14)


normalize_gtin = normalize_gtin14  # the helper's earlier name - same function


def checked_gtin14(raw: str | None, *, job_number: str | None, product: str | None) -> str:
    """normalize_gtin14(), but a refusal names the job, the customer product and
    the bad value - for the places that are about to export, print or barcode."""
    try:
        return normalize_gtin14(raw)
    except InvalidGTINError as exc:
        shown = "" if raw is None else raw
        raise InvalidGTINError(
            f"Job {job_number or '(unknown)'}, product {product or '(unknown)'}: "
            f"the GTIN {shown!r} cannot be used - {exc}\n\n"
            "Nothing was exported or printed with this GTIN. Correct the GTIN (Barcode Start in "
            "Label Traxx) and try again."
        ) from exc


def gtin14_or_none(raw: str | None) -> str | None:
    """The 14-digit GTIN, or None if `raw` is blank or fails validation - for
    reports, which show "no valid GTIN" rather than draw a wrong barcode."""
    try:
        return normalize_gtin14(raw)
    except InvalidGTINError:
        return None


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
