import datetime

import pytest

from src.dates import format_production_date, normalize_production_date, parse_production_date
from src.gs1 import build_contents_barcode_data, build_contents_element_string, format_ai11_date


def test_parse_reads_yymmdd_as_20yy():
    assert parse_production_date("261104") == datetime.date(2026, 11, 4)
    assert parse_production_date("000101") == datetime.date(2000, 1, 1)
    assert parse_production_date("991231") == datetime.date(2099, 12, 31)


@pytest.mark.parametrize(
    "bad",
    ["", "26110", "2611044", "26-11-04", "2026-11-04", "26110a", "261301", "261132", "260230", " 261104", "261104 "],
)
def test_parse_rejects_anything_that_is_not_a_real_yymmdd_date(bad):
    with pytest.raises(ValueError):
        parse_production_date(bad)


def test_format_is_yymmdd_with_zero_padding():
    assert format_production_date(datetime.date(2026, 11, 4)) == "261104"
    assert format_production_date(datetime.date(2005, 1, 9)) == "050109"


def test_format_rejects_years_outside_2000_2099():
    with pytest.raises(ValueError):
        format_production_date(datetime.date(1999, 12, 31))
    with pytest.raises(ValueError):
        format_production_date(datetime.date(2100, 1, 1))


def test_normalize_passes_yymmdd_through_and_converts_the_legacy_iso_form():
    assert normalize_production_date("261104") == "261104"
    assert normalize_production_date("2026-11-04") == "261104"
    with pytest.raises(ValueError):
        normalize_production_date("11/04/2026")


def test_stored_values_sort_chronologically_as_plain_strings():
    # the pallet screen takes min() of the cartons' stored dates
    dates = ["261104", "260315", "270101", "261231"]
    assert min(dates) == "260315"
    assert sorted(dates) == ["260315", "261104", "261231", "270101"]


def test_barcode_date_is_the_same_yymmdd_string_as_the_stored_one():
    assert format_ai11_date("261104") == "261104"
    assert build_contents_element_string("00051096184921", "261104", 27000, "12298447388") == (
        "(02)00051096184921(11)261104(37)27000(10)12298447388"
    )
    assert "11261104" in build_contents_barcode_data("00051096184921", "261104", 27000, "12298447388")
