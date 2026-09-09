from src.gs1 import build_contents_element_string, build_sscc_element_string, format_ai11_date


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
            production_date_iso="2026-05-15",
            quantity=5000,
            batch="122984",
        )
        == "(02)00721059000635(11)260515(37)5000(10)122984"
    )


def test_build_sscc_element_string():
    assert build_sscc_element_string("008600157112000104") == "(00)008600157112000104"
