"""
GS1-128 element string formatting, for showing the actual barcode content on
screen before any label is generated (per the user's request) - not just the
raw field values in a table, but the same (AI)data(AI)data string that gets
encoded into the barcode.

AI order (02)(11)(37)(10) matches CLC's own usage, confirmed against a real
example the user provided: (02)00721059000635(11)260515(37)5000(10)122984.
SSCC (00) is always its own separate barcode, never combined with the
contents string - see docs/gs1_label_requirements.md.
"""

import datetime


def format_ai11_date(production_date_iso: str) -> str:
    """YYYY-MM-DD -> YYMMDD, the format AI (11) Production Date requires."""
    d = datetime.date.fromisoformat(production_date_iso)
    return d.strftime("%y%m%d")


def build_contents_element_string(gtin: str, production_date_iso: str, quantity: int, batch: str) -> str:
    """(02) GTIN + (11) production date + (37) quantity + (10) batch."""
    return f"(02){gtin}(11){format_ai11_date(production_date_iso)}(37){quantity}(10){batch}"


def build_sscc_element_string(sscc: str) -> str:
    """(00) SSCC - always its own separate barcode from the contents string."""
    return f"(00){sscc}"


# --- raw barcode data (no parentheses, real FNC1 separators) ---------------
#
# The (AI)data(AI)data strings above are for on-screen display only -
# parentheses are never actually encoded into a GS1-128 barcode. What gets
# encoded is the AI digits run directly into the data, with an FNC1 control
# character (not a printable character) inserted as a separator wherever a
# variable-length field is followed by more data (GS1 General Specifications
# rule). Fixed-length fields (GTIN N14, date N6) never need a separator.
#
# AI (37) quantity is variable-length (N..8) and is NOT the last field here,
# so it needs an FNC1 separator before AI (10) begins. AI (10) batch is
# variable-length too, but it IS the last field, so no trailing separator.
#
# Verified round-trip with an independent decoder (zxing-cpp) against the
# user's real pasted example - see tests/test_barcode_image.py.

FNC1 = "\xf1"  # recognized by barcode.codex.Gs1_128._is_char_fnc1_char


def build_contents_barcode_data(gtin: str, production_date_iso: str, quantity: int, batch: str) -> str:
    """Raw GS1-128 data (no parens) for the (02)(11)(37)(10) contents barcode."""
    yymmdd = format_ai11_date(production_date_iso)
    return f"02{gtin}11{yymmdd}37{quantity}{FNC1}10{batch}"


def build_sscc_barcode_data(sscc: str) -> str:
    """Raw GS1-128 data (no parens) for the (00) SSCC barcode - single fixed
    field, so no FNC1 separator is needed anywhere."""
    return f"00{sscc}"
