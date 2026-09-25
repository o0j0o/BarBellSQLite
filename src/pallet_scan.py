"""
Cleans up and validates one raw SSCC barcode scan for the Pallet screen -
see barbell_gui.py's Pallet screen and QUESTIONS.md #18.

The Bluetooth scanner acts as a keyboard wedge: whatever the barcode
decodes to gets typed into the scan box, then Enter. What lands there needs
cleanup before it's usable as an SSCC:
  - a leading AIM symbology identifier, e.g. "]C1" - present if the scanner
    is configured to send one, harmless to strip if not
  - GS/FNC1 control characters - GS1-128 barcodes can decode to include
    these as field separators (see src/gs1.py's FNC1 - the same codepoint)
  - a literal "(00)" or bare "00" AI prefix - the printed SSCC barcode
    itself encodes AI (00) + the 18-digit SSCC (see
    src.gs1.build_sscc_barcode_data), so a clean scan of it typically
    arrives as "00" + 18 digits = 20 characters total

After cleanup, a valid scan is exactly 18 digits with a correct GS1 mod-10
check digit (src.sscc.gs1_check_digit) - or, in test_mode only, the exact
TEST-SSCC-##### placeholder format src.sscc.build_test_sscc() produces
(not a real barcode - there's nothing to scan for it - but recognized as
typed input so the rest of the pallet-building flow can still be exercised
in test mode without a real scannable SSCC to print). A scan that looks
like the (02)... contents barcode (commonly mis-scanned instead of the
SSCC barcode below it) gets a specific, actionable message instead of a
generic one.
"""

import re
from dataclasses import dataclass, field

from src.db.local_store import CartonInfo
from src.sscc import gs1_check_digit

_AIM_PREFIX_RE = re.compile(r"^\][A-Za-z]\d")
_GS_FNC1_CHARS = "\x1d\xf1"  # ASCII Group Separator, and the FNC1 codepoint src/gs1.py uses
_TEST_SSCC_RE = re.compile(r"^TEST-SSCC-\d{5}$")

CONTENTS_BARCODE_MESSAGE = "That is the contents barcode. Scan the lower SSCC barcode."


class ScanError(ValueError):
    """Raised for any scan that can't be used as an SSCC - str(exc) is the
    operator-facing message."""


class ContentsBarcodeScannedError(ScanError):
    """Raised specifically when the scan looks like the (02)... contents
    barcode, not the (00)... SSCC barcode - the common mis-scan."""


def clean_scanned_sscc(raw: str, test_mode: bool = False) -> str:
    """
    Cleans up one raw scan and returns a validated SSCC string (18 digits,
    or the TEST-SSCC-##### placeholder while test_mode=True), or raises
    ScanError/ContentsBarcodeScannedError with an operator-facing message.
    """
    text = raw.strip()

    if test_mode and _TEST_SSCC_RE.match(text):
        return text

    text = _AIM_PREFIX_RE.sub("", text)
    for ch in _GS_FNC1_CHARS:
        text = text.replace(ch, "")
    text = text.strip()

    if not text:
        raise ScanError("Nothing was scanned.")

    if text.startswith("(00)"):
        text = text[4:]
    elif text.startswith("("):
        # Any other parenthesized AI - (02), (11), (37), (10), etc.
        raise ContentsBarcodeScannedError(CONTENTS_BARCODE_MESSAGE)
    elif text.isdigit() and len(text) == 20 and text.startswith("00"):
        text = text[2:]
    elif text.isdigit() and len(text) == 18:
        pass  # a bare SSCC, nothing to strip
    elif text.startswith("02"):
        # An un-parenthesized contents barcode (AI digits run straight into
        # the data, same as what's actually encoded - see src/gs1.py).
        raise ContentsBarcodeScannedError(CONTENTS_BARCODE_MESSAGE)

    if not text.isdigit():
        raise ScanError(f"That doesn't look like a barcode scan: {raw!r}")
    if len(text) != 18:
        raise ScanError(f"SSCC must be 18 digits, got {len(text)}: {text!r}")

    body, check_digit = text[:-1], text[-1]
    expected = gs1_check_digit(body)
    if check_digit != expected:
        raise ScanError(
            f"SSCC check digit looks wrong: {text} ends in {check_digit}, expected {expected}."
        )

    return text


# --- evaluate_scan: what to do with a successfully-cleaned SSCC --------------
#
# Pure and Tkinter-free by design (see barbell_gui.py's Pallet screen for the
# GUI orchestration around it) - takes a CartonInfo (or None, if the SSCC
# wasn't found at all) plus the pallet-building session's own state, and
# decides block / warn-and-confirm / accept. Check order matches the user's
# own spec: not found -> wrong type -> voided -> already on another pallet
# -> duplicate on this pallet -> GTIN differs -> batch differs -> count
# reached -> test/production mismatch -> (warnings).


@dataclass
class PalletScanCheck:
    """blocked_reason set -> reject outright, carton is NOT added.
    blocked_reason None and warnings non-empty -> ask the operator to
    confirm each warning before adding. Both None/empty -> accept
    immediately."""

    carton: CartonInfo | None
    blocked_reason: str | None = None
    warnings: list[str] = field(default_factory=list)


def check_carton_for_pallet(
    carton: CartonInfo | None,
    scanned_so_far: list[CartonInfo],
    expected_count: int,
    pallet_test_mode: bool,
) -> PalletScanCheck:
    if carton is None:
        return PalletScanCheck(
            None, blocked_reason="That SSCC isn't in BarBell's records (Job/Label History)."
        )

    if carton.label_type == "PALLET":
        return PalletScanCheck(
            carton, blocked_reason="That SSCC belongs to a pallet, not a carton."
        )

    if carton.status == "void":
        return PalletScanCheck(carton, blocked_reason="This carton has been voided.")

    if carton.pallet_sscc is not None:
        return PalletScanCheck(
            carton, blocked_reason=f"This carton is already on pallet {carton.pallet_sscc}."
        )

    if any(c.sscc == carton.sscc for c in scanned_so_far):
        return PalletScanCheck(
            carton, blocked_reason="This carton has already been scanned onto this pallet."
        )

    if scanned_so_far:
        reference = scanned_so_far[0]
        if carton.gtin != reference.gtin:
            return PalletScanCheck(
                carton,
                blocked_reason=(
                    f"This carton's GTIN ({carton.gtin}) doesn't match the pallet's "
                    f"GTIN ({reference.gtin})."
                ),
            )
        if carton.batch != reference.batch:
            return PalletScanCheck(
                carton,
                blocked_reason=(
                    f"This carton's batch ({carton.batch}) doesn't match the pallet's "
                    f"batch ({reference.batch})."
                ),
            )

    if len(scanned_so_far) >= expected_count:
        return PalletScanCheck(
            carton,
            blocked_reason=f"Already scanned {expected_count} of {expected_count} expected cartons.",
        )

    if carton.test_mode != pallet_test_mode:
        found_kind = "test" if carton.test_mode else "production"
        expected_kind = "test" if pallet_test_mode else "production"
        return PalletScanCheck(
            carton,
            blocked_reason=(
                f"This is a {found_kind} carton, but this pallet is in {expected_kind} mode - "
                "test and production cartons can never be mixed."
            ),
        )

    warnings = []
    if scanned_so_far:
        reference = scanned_so_far[0]
        if carton.production_date != reference.production_date:
            warnings.append(
                f"Production date {carton.production_date} differs from this pallet's "
                f"{reference.production_date} (from the first carton scanned). "
                "The pallet label will use the earliest date."
            )
        if carton.packing_slip_number != reference.packing_slip_number:
            warnings.append(
                f"Packing slip {carton.packing_slip_number} differs from this pallet's "
                f"{reference.packing_slip_number} (from the first carton scanned)."
            )
        if carton.extension_digit != reference.extension_digit:
            warnings.append(
                f"This carton was printed at a different plant (extension digit "
                f"{carton.extension_digit} vs {reference.extension_digit} for the first "
                "carton scanned)."
            )

    return PalletScanCheck(carton, warnings=warnings)
