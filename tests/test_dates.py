import datetime

import pytest

from src import dates
from src.dates import (
    ProductionDateRangeError,
    format_production_date,
    normalize_production_date,
    parse_production_date,
    validate_production_date,
)
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


# --- the rules for a date an operator types ------------------------------------------------------------
# today is 13 Nov 2026 here: up to 7 days ahead (261120), and 26xxxx or 25xxxx (this year or last year)

TODAY = datetime.date(2026, 11, 13)


@pytest.mark.parametrize(
    "ok",
    [
        "261113",  # today
        "261120",  # exactly 7 days ahead - the last allowed day
        "261114",  # tomorrow
        "261104",  # last week
        "260101",  # earlier this year
        "251231",  # last year, the last day
        "251101",  # last year, more than 12 months ago by the calendar: still last year, so accepted
        "250101",  # last year, the first day - the earliest allowed
    ],
)
def test_dates_inside_the_window_are_accepted(ok):
    assert validate_production_date(ok, on=TODAY) == parse_production_date(ok)


@pytest.mark.parametrize("too_far_ahead", ["261121", "261201", "270101", "280101", "991231"])
def test_a_date_more_than_7_days_ahead_is_refused(too_far_ahead):
    with pytest.raises(ProductionDateRangeError) as exc:
        validate_production_date(too_far_ahead, on=TODAY)
    assert "261120" in str(exc.value)  # tells the operator the latest date they can use
    assert "future" in str(exc.value)


@pytest.mark.parametrize("too_old", ["241231", "240101", "200101", "000101"])
def test_a_date_older_than_last_year_is_refused(too_old):
    with pytest.raises(ProductionDateRangeError) as exc:
        validate_production_date(too_old, on=TODAY)
    assert "past" in str(exc.value) and "26" in str(exc.value) and "25" in str(exc.value)


@pytest.mark.parametrize("not_a_date", ["", "26110", "2611044", "26-11-04", "2026-11-04", "26110a", "261301", "261132", "260230", "261104 "])
def test_anything_that_is_not_a_real_yymmdd_date_is_refused_first(not_a_date):
    with pytest.raises(ValueError) as exc:
        validate_production_date(not_a_date, on=TODAY)
    assert not isinstance(exc.value, ProductionDateRangeError)  # a different message: "not a valid date"


def test_the_range_error_is_a_value_error_so_old_callers_still_catch_it():
    assert issubclass(ProductionDateRangeError, ValueError)


def test_the_window_moves_with_the_calendar_across_new_year():
    new_year_eve = datetime.date(2026, 12, 28)
    assert validate_production_date("270104", on=new_year_eve)  # +7 days, into next year: fine
    with pytest.raises(ProductionDateRangeError):
        validate_production_date("270105", on=new_year_eve)  # +8
    early_january = datetime.date(2027, 1, 3)
    assert validate_production_date("260101", on=early_january)  # last year is still allowed ...
    with pytest.raises(ProductionDateRangeError):
        validate_production_date("251231", on=early_january)  # ... but the year before that is not


def test_leap_day_is_a_real_date():
    assert validate_production_date("240229", on=datetime.date(2024, 3, 1)) == datetime.date(2024, 2, 29)


def test_with_no_date_given_it_uses_todays_date():
    # conftest pins dates.today() to 13 Nov 2026 for every test
    assert dates.today() == TODAY
    assert validate_production_date("261120")
    with pytest.raises(ProductionDateRangeError):
        validate_production_date("261121")
