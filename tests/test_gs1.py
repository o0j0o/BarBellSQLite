import pytest

from src.gs1 import (
    FNC1,
    GTIN_AI_CARTON,
    GTIN_AI_PALLET,
    build_contents_barcode_data,
    build_contents_element_string,
    build_sscc_element_string,
    format_ai11_date,
)


def test_format_ai11_date_converts_iso_to_yymmdd():
    assert format_ai11_date("2026-05-15") == "260515"
    assert format_ai11_date("2026-03-23") == "260323"


def test_build_contents_element_string_matches_users_real_example():
    """
    Directly verified against a real GS1-128 string the user pasted:
    (02)00721059000635(11)260515(37)5000(10)122984
    """
    assert (
        build_contents_element_string(
            gtin="00721059000635",
            production_date="260515",
            quantity=5000,
            batch="122984",
        )
        == "(02)00721059000635(11)260515(37)5000(10)122984"
    )


def test_build_sscc_element_string():
    assert build_sscc_element_string("008600157112000104") == "(00)008600157112000104"


# --- carton label (01) vs pallet label (02): the customer's rules -------------------------

def test_carton_label_uses_ai_01_for_the_gtin_and_ai_37_for_the_count():
    assert build_contents_element_string(
        "00636191205407", "260505", 12000, "12311841185", gtin_ai=GTIN_AI_CARTON
    ) == "(01)00636191205407(11)260505(37)12000(10)12311841185"


def test_pallet_label_uses_ai_02_for_the_gtin_and_ai_37_for_the_total_product_count():
    expected = "(02)00636191205407(11)260505(37)60000(10)12311841185"
    assert build_contents_element_string(
        "00636191205407", "260505", 60000, "12311841185", gtin_ai=GTIN_AI_PALLET
    ) == expected
    # (02) is the default, so existing pallet callers are unchanged
    assert build_contents_element_string("00636191205407", "260505", 60000, "12311841185") == expected


def test_carton_and_pallet_forms_differ_only_in_the_gtin_ai():
    carton = build_contents_element_string("00636191205407", "260505", 12000, "B1", gtin_ai=GTIN_AI_CARTON)
    pallet = build_contents_element_string("00636191205407", "260505", 12000, "B1", gtin_ai=GTIN_AI_PALLET)
    assert carton.replace("(01)", "(02)", 1) == pallet
    assert "(37)" in carton and "(37)" in pallet and "(30)" not in carton  # always (37), never (30)


def test_only_01_and_02_are_accepted_as_the_gtin_ai():
    for bad in ("00", "03", "30", "37", ""):
        with pytest.raises(ValueError):
            build_contents_element_string("00636191205407", "260505", 12000, "B1", gtin_ai=bad)
        with pytest.raises(ValueError):
            build_contents_barcode_data("00636191205407", "260505", 12000, "B1", gtin_ai=bad)


def test_barcode_data_carries_the_chosen_ai_with_an_fnc1_before_the_batch():
    carton = build_contents_barcode_data("00636191205407", "260505", 12000, "B1", gtin_ai=GTIN_AI_CARTON)
    pallet = build_contents_barcode_data("00636191205407", "260505", 12000, "B1")
    assert carton == "01006361912054071126050537" + "12000" + FNC1 + "10B1"
    assert pallet == "02006361912054071126050537" + "12000" + FNC1 + "10B1"
