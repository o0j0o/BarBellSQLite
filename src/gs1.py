"""
GS1-128 element string formatting, for showing the actual barcode content on
screen before any label is generated (per the user's request) - not just the
raw field values in a table, but the same (AI)data(AI)data string that gets
encoded into the barcode.

The Contents barcode carries GTIN, production date, count, and batch. Which AI
carries the GTIN depends on the label (the customer's rules):

  - CARTON label: (01) GTIN, (11) production date, (37) count in the carton,
    (10) batch. (37) is used because the customer asked for it.
  - PALLET label: (02) GTIN, (11) production date, (37) TOTAL count of product
    on the pallet - product, not cartons - (10) batch. A pallet label is only
    ever made for a pallet holding all the same product; that is the only
    pallet the customer wants a label for (the Pallet screen enforces it).

The pallet form was confirmed against a real example the user provided:
(02)00721059000635(11)260515(37)5000(10)122984. SSCC (00) is always its own
separate barcode, never combined with the contents string - see
docs/gs1_label_requirements.md.
"""

from src.dates import normalize_production_date

GTIN_AI_CARTON = "01"  # GTIN of the trade item - the carton label
GTIN_AI_PALLET = "02"  # GTIN of the items contained - the (mono-product) pallet label
_GTIN_AIS = (GTIN_AI_CARTON, GTIN_AI_PALLET)


def format_ai11_date(production_date: str) -> str:
    """The production date as AI (11) requires it: YYMMDD. That is also how
    BarBell stores and shows it, so this is normally a pass-through; a legacy
    YYYY-MM-DD value is converted (see src/dates.py)."""
    return normalize_production_date(production_date)


def build_contents_element_string(
    gtin: str, production_date: str, quantity: int, batch: str, gtin_ai: str = GTIN_AI_PALLET
) -> str:
    """GTIN + (11) production date + (37) count + (10) batch, with the GTIN under
    gtin_ai: GTIN_AI_CARTON "01" for a carton label, GTIN_AI_PALLET "02" for a
    pallet label (the default - callers that mean a carton must say so)."""
    if gtin_ai not in _GTIN_AIS:
        raise ValueError(f"gtin_ai must be one of {_GTIN_AIS}, got {gtin_ai!r}")
    return f"({gtin_ai}){gtin}(11){format_ai11_date(production_date)}(37){quantity}(10){batch}"


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


def build_contents_barcode_data(
    gtin: str, production_date: str, quantity: int, batch: str, gtin_ai: str = GTIN_AI_PALLET
) -> str:
    """Raw GS1-128 data (no parens) for the contents barcode: <gtin_ai>(11)(37)(10),
    with gtin_ai "01" for a carton label or "02" (the default) for a pallet label."""
    if gtin_ai not in _GTIN_AIS:
        raise ValueError(f"gtin_ai must be one of {_GTIN_AIS}, got {gtin_ai!r}")
    yymmdd = format_ai11_date(production_date)
    return f"{gtin_ai}{gtin}11{yymmdd}37{quantity}{FNC1}10{batch}"


def build_sscc_barcode_data(sscc: str) -> str:
    """Raw GS1-128 data (no parens) for the (00) SSCC barcode - single fixed
    field, so no FNC1 separator is needed anywhere."""
    return f"00{sscc}"
