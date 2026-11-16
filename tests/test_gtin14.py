"""
The GTIN is always carried as 14 digits including its check digit (1.1.21 Beta).

BarTender's template discards the last digit, recalculates the check digit and
then demands exactly 13 characters - so BarBell must hand it 14 digits, and must
never hand it a GTIN that fails validation (BarTender would quietly "fix" it).
One helper, src.gtin.normalize_gtin14, does all of it.
"""

import csv

import pytest

from src.db.local_store import (
    LABEL_TYPE_CARTON,
    LABEL_TYPE_PALLET,
    create_pallet,
    create_reprint_rows,
    fetch_label_history,
    record_generation_run,
    write_flat_csv,
)
from src.gtin import InvalidGTINError, checked_gtin14, gtin14_or_none, normalize_gtin, normalize_gtin14
from src.labels import LabelRow
from src.sscc import build_sscc, build_test_sscc

JWN_UPC = "636191036407"  # the real J. Wray & Nephew value in Label Traxx's Barcode Start
JWN_GTIN14 = "00636191036407"


# --- the helper --------------------------------------------------------------


def test_12_digit_upc_is_padded_to_14():
    assert normalize_gtin14(JWN_UPC) == JWN_GTIN14


def test_the_worked_check_digit_example():
    """Data 0063619103640, weighted 3,1,3,1,... from the right, sums to 93 -> check digit 7."""
    data = "0063619103640"
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(data)))
    assert total == 93
    assert (10 - total % 10) % 10 == 7
    assert normalize_gtin14(data + "7") == JWN_GTIN14


def test_13_digit_ean_with_valid_check_digit_is_padded_to_14():
    assert normalize_gtin14("0636191036407") == JWN_GTIN14
    assert normalize_gtin14("4006381333931") == "04006381333931"


def test_valid_14_digit_gtin_with_indicator_digit_1_passes_unchanged():
    assert normalize_gtin14("10636191036404") == "10636191036404"


@pytest.mark.parametrize("indicator", "12345678")
def test_every_indicator_digit_1_to_8_is_validated_on_its_own_check_digit(indicator):
    body = indicator + "063619103640"
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body)))
    good = body + str((10 - total % 10) % 10)
    assert normalize_gtin14(good) == good
    bad = body + str((int(good[-1]) + 1) % 10)
    with pytest.raises(InvalidGTINError, match="check digit"):
        normalize_gtin14(bad)


def test_the_indicator_digit_changes_the_check_digit():
    """10636191036407 just puts a 1 in front of the UPC - its check digit is 4, not 7."""
    with pytest.raises(InvalidGTINError, match="check digit"):
        normalize_gtin14("10636191036407")


def test_spaces_and_hyphens_are_removed_first():
    assert normalize_gtin14(" 6 36191 03640 7 ") == JWN_GTIN14
    assert normalize_gtin14("6-36191-03640-7") == JWN_GTIN14


def test_wrong_check_digit_is_rejected_with_a_clear_message():
    with pytest.raises(InvalidGTINError) as excinfo:
        normalize_gtin14("636191036408")
    message = str(excinfo.value)
    assert "check digit" in message
    assert "636191036408" in message
    assert "expected 7" in message


@pytest.mark.parametrize(
    "bad",
    [
        "63619103640",  # 11 digits - short
        "12345670",  # 8 digits - a GTIN-8 is not accepted
        "006361910364070",  # 15 digits - long
        "",  # blank
        "   ",  # blank
        None,
        "63619103640A",  # not numeric
        "ABCDEFGHIJKL",
        "63619103640O",  # letter O for a zero
        "636191036407.0",  # a number that has been through a spreadsheet
    ],
)
def test_short_long_blank_and_non_numeric_values_are_rejected(bad):
    with pytest.raises(InvalidGTINError):
        normalize_gtin14(bad)
    assert gtin14_or_none(bad) is None


def test_the_old_name_is_the_same_helper():
    assert normalize_gtin is normalize_gtin14


def test_a_refusal_names_the_job_the_product_and_the_bad_value():
    with pytest.raises(InvalidGTINError) as excinfo:
        checked_gtin14("636191036408", job_number="123125", product="JWN White O/P Rum (P/N 41820)")
    message = str(excinfo.value)
    assert "Job 123125" in message
    assert "JWN White O/P Rum (P/N 41820)" in message
    assert "636191036408" in message
    assert "Nothing was exported or printed" in message


# --- the exported CSV --------------------------------------------------------


def _carton_rows(gtin, ssccs, job_number="123125"):
    return [
        LabelRow(
            job_number=job_number,
            packing_slip_number="100522",
            customer_number="J00005",
            customer_name="J. Wray & Nephew Ltd.",
            product_no="41820",
            item_number="228627",
            item_description="228627 - JWN White O/P Rum B 750Ml JAM/EXP - PS",
            quantity=180000,
            batch="12312541820",
            production_date="260505",
            sscc=sscc,
            gtin=gtin,
            package_index=index,
            label_copy_index=1,
        )
        for index, sscc in enumerate(ssccs, start=1)
    ]


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _saved_cartons(db, test_mode=False):
    build = build_test_sscc if test_mode else (lambda n: build_sscc("08600157112", "0", n))
    ssccs = [build(1), build(2)]
    return ssccs, record_generation_run(
        _carton_rows(JWN_GTIN14, ssccs), units_per_package=180000, labels_per_package=1,
        test_mode=test_mode, db_path=db,
    )


@pytest.mark.parametrize("test_mode", [False, True])
def test_carton_csv_row_carries_the_14_digit_gtin(tmp_path, test_mode):
    _ssccs, flat = _saved_cartons(tmp_path / "barbell.db", test_mode)
    rows = _read(write_flat_csv(flat, tmp_path / "carton.csv"))
    assert [r["GTIN"] for r in rows] == [JWN_GTIN14, JWN_GTIN14]
    assert {r["LabelType"] for r in rows} == {LABEL_TYPE_CARTON}


@pytest.mark.parametrize("test_mode", [False, True])
def test_pallet_csv_row_carries_the_same_14_digit_gtin(tmp_path, test_mode):
    db = tmp_path / "barbell.db"
    ssccs, _flat = _saved_cartons(db, test_mode)
    pallet_sscc = build_test_sscc(9) if test_mode else build_sscc("08600157112", "0", 9)
    pallet_rows = create_pallet(
        carton_ssccs=ssccs, job_number="123125", quantity=360000, production_date="260505",
        packing_slip_number="100522", pallet_sscc=pallet_sscc, carton_count=2, db_path=db,
    )
    rows = _read(write_flat_csv(pallet_rows, tmp_path / "pallet.csv"))
    assert rows
    assert {r["GTIN"] for r in rows} == {JWN_GTIN14}
    assert {r["LabelType"] for r in rows} == {LABEL_TYPE_PALLET}


def test_a_12_digit_gtin_reaching_the_csv_writer_is_still_written_as_14(tmp_path):
    """Belt and braces: the writer itself normalizes, so the column can never be 12 digits."""
    rows = _read(write_flat_csv(_carton_rows(JWN_UPC, [build_sscc("08600157112", "0", 1)]), tmp_path / "c.csv"))
    assert rows[0]["GTIN"] == JWN_GTIN14


@pytest.mark.parametrize("bad", ["636191036408", "", None, "63619103640", "ABC"])
def test_a_bad_gtin_is_never_exported_and_no_file_is_written(tmp_path, bad):
    out = tmp_path / "carton.csv"
    good = _carton_rows(JWN_GTIN14, [build_sscc("08600157112", "0", 1)])
    with pytest.raises(InvalidGTINError) as excinfo:
        write_flat_csv(good + _carton_rows(bad, [build_sscc("08600157112", "0", 2)]), out)
    assert not out.exists()  # not even the good row is written
    message = str(excinfo.value)
    assert "Job 123125" in message and "JWN White O/P Rum" in message and "P/N 41820" in message
    if bad:
        assert bad in message


def test_a_reprint_of_a_label_with_a_bad_stored_gtin_is_refused_and_not_logged(tmp_path):
    db = tmp_path / "barbell.db"
    flat = record_generation_run(
        _carton_rows("636191036408", [build_sscc("08600157112", "0", 1)]),
        units_per_package=180000, labels_per_package=1, test_mode=False, db_path=db,
    )
    before = len(fetch_label_history(db))
    with pytest.raises(InvalidGTINError, match="Job 123125"):
        create_reprint_rows([flat[0].id], db_path=db)
    assert len(fetch_label_history(db)) == before  # no 'reprint' row was left behind
