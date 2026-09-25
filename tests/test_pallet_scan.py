import pytest

from src.pallet_scan import (
    CONTENTS_BARCODE_MESSAGE,
    ContentsBarcodeScannedError,
    ScanError,
    clean_scanned_sscc,
)
from src.sscc import build_sscc, gs1_check_digit

VALID_SSCC = build_sscc("08600157112", "0", 42)  # a real, validly-checksummed 18-digit SSCC


def test_bare_18_digit_sscc_passes_through():
    assert clean_scanned_sscc(VALID_SSCC) == VALID_SSCC


def test_strips_whitespace():
    assert clean_scanned_sscc(f"  {VALID_SSCC}  ") == VALID_SSCC


def test_strips_aim_symbology_identifier():
    assert clean_scanned_sscc(f"]C1{VALID_SSCC}") == VALID_SSCC


def test_strips_gs_fnc1_control_characters():
    assert clean_scanned_sscc(f"\x1d{VALID_SSCC}\x1d") == VALID_SSCC
    assert clean_scanned_sscc(f"\xf1{VALID_SSCC}") == VALID_SSCC


def test_strips_00_prefix_on_20_digit_scan():
    """The printed SSCC barcode encodes AI (00) + the 18-digit SSCC, so a
    clean scan typically arrives as 20 digits starting with 00."""
    assert clean_scanned_sscc(f"00{VALID_SSCC}") == VALID_SSCC


def test_strips_parenthesized_00_prefix():
    assert clean_scanned_sscc(f"(00){VALID_SSCC}") == VALID_SSCC


def test_combined_realistic_scan():
    raw = f"]C1\x1d(00){VALID_SSCC}\x1d"
    assert clean_scanned_sscc(raw) == VALID_SSCC


def test_empty_scan_raises_scan_error():
    with pytest.raises(ScanError, match="Nothing was scanned"):
        clean_scanned_sscc("   ")


def test_contents_barcode_parenthesized_raises_specific_error():
    with pytest.raises(ContentsBarcodeScannedError) as exc_info:
        clean_scanned_sscc("(02)00721059000635(11)260515(37)5000(10)122984")
    assert str(exc_info.value) == CONTENTS_BARCODE_MESSAGE


def test_contents_barcode_bare_ai_raises_specific_error():
    with pytest.raises(ContentsBarcodeScannedError):
        clean_scanned_sscc("0200721059000635111105153750001012298")


def test_contents_barcode_error_is_a_scan_error_too():
    """Callers that just want to catch 'any bad scan' can catch ScanError."""
    assert issubclass(ContentsBarcodeScannedError, ScanError)


def test_wrong_length_raises_scan_error():
    with pytest.raises(ScanError, match="18 digits"):
        clean_scanned_sscc(VALID_SSCC[:-1])  # 17 digits


def test_non_digit_garbage_raises_scan_error():
    with pytest.raises(ScanError, match="doesn't look like a barcode scan"):
        clean_scanned_sscc("not-a-barcode-at-all")


def test_bad_check_digit_raises_scan_error():
    body = VALID_SSCC[:-1]
    wrong_check_digit = str((int(gs1_check_digit(body)) + 1) % 10)
    bad_sscc = body + wrong_check_digit
    with pytest.raises(ScanError, match="check digit looks wrong"):
        clean_scanned_sscc(bad_sscc)


# --- test_mode: TEST-SSCC-##### placeholder ---------------------------------

def test_test_sscc_placeholder_accepted_in_test_mode():
    assert clean_scanned_sscc("TEST-SSCC-00007", test_mode=True) == "TEST-SSCC-00007"


def test_test_sscc_placeholder_rejected_outside_test_mode():
    """Production mode must never accept the obviously-fake test format -
    it isn't 18 digits, so it fails the normal validation."""
    with pytest.raises(ScanError):
        clean_scanned_sscc("TEST-SSCC-00007", test_mode=False)


def test_real_sscc_still_accepted_in_test_mode():
    """test_mode doesn't stop a real-format 18-digit SSCC from validating -
    only adds the placeholder as an extra accepted shape."""
    assert clean_scanned_sscc(VALID_SSCC, test_mode=True) == VALID_SSCC


def test_test_sscc_wrong_digit_count_not_treated_as_placeholder():
    with pytest.raises(ScanError):
        clean_scanned_sscc("TEST-SSCC-007", test_mode=True)  # only 3 digits, not 5


# --- check_carton_for_pallet -------------------------------------------------

from src.db.local_store import CartonInfo
from src.pallet_scan import PalletScanCheck, check_carton_for_pallet


def make_carton(**overrides):
    defaults = dict(
        id=1, sscc="086001571120000012", job_number="122984", product_no="47388",
        item_number="233458", gtin="00051096184921", batch="12298447388", quantity=10000,
        production_date="2026-03-23", packing_slip_number="100495", status="original",
        pallet_sscc=None, label_type="CARTON", test_mode=False, created_at="2026-03-23T00:00:00",
    )
    defaults.update(overrides)
    return CartonInfo(**defaults)


def test_not_found_is_blocked():
    result = check_carton_for_pallet(None, [], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is not None
    assert result.carton is None


def test_pallet_sscc_scanned_as_carton_is_blocked():
    carton = make_carton(label_type="PALLET")
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert "pallet, not a carton" in result.blocked_reason


def test_voided_carton_is_blocked():
    carton = make_carton(status="void")
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert "voided" in result.blocked_reason


def test_carton_already_on_another_pallet_names_it():
    carton = make_carton(pallet_sscc="086001571120099999")
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert "086001571120099999" in result.blocked_reason


def test_duplicate_scan_on_this_pallet_is_blocked():
    carton = make_carton()
    result = check_carton_for_pallet(carton, [carton], expected_count=5, pallet_test_mode=False)
    assert "already been scanned" in result.blocked_reason


def test_different_gtin_is_blocked():
    first = make_carton(sscc="086001571120000012")
    second = make_carton(sscc="086001571120000029", gtin="00099999999999")
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert "GTIN" in result.blocked_reason


def test_different_batch_is_blocked():
    first = make_carton(sscc="086001571120000012")
    second = make_carton(sscc="086001571120000029", batch="99999947388")
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert "batch" in result.blocked_reason


def test_expected_count_reached_is_blocked():
    first = make_carton(sscc="086001571120000012")
    second_scan = make_carton(sscc="086001571120000029")
    result = check_carton_for_pallet(second_scan, [first], expected_count=1, pallet_test_mode=False)
    assert "Already scanned 1 of 1" in result.blocked_reason


def test_production_carton_in_test_mode_pallet_is_blocked():
    carton = make_carton(test_mode=False)
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=True)
    assert "production carton" in result.blocked_reason
    assert "test mode" in result.blocked_reason


def test_test_carton_in_production_mode_pallet_is_blocked():
    carton = make_carton(test_mode=True)
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert "test carton" in result.blocked_reason


def test_clean_scan_no_warnings_is_accepted():
    carton = make_carton()
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is None
    assert result.warnings == []
    assert result.carton is carton


def test_differing_production_date_warns_not_blocks():
    first = make_carton(sscc="086001571120000012", production_date="2026-03-23")
    second = make_carton(sscc="086001571120000029", production_date="2026-03-24")
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is None
    assert len(result.warnings) == 1
    assert "earliest" in result.warnings[0]


def test_differing_packing_slip_warns_not_blocks():
    first = make_carton(sscc="086001571120000012", packing_slip_number="100495")
    second = make_carton(sscc="086001571120000029", packing_slip_number="100600")
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is None
    assert len(result.warnings) == 1
    assert "Packing slip" in result.warnings[0]


def test_different_plant_extension_digit_warns_not_blocks():
    first = make_carton(sscc="086001571120000012")  # extension digit '0'
    second = make_carton(sscc="186001571120000029")  # extension digit '1'
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is None
    assert len(result.warnings) == 1
    assert "different plant" in result.warnings[0]


def test_multiple_warnings_can_combine():
    first = make_carton(
        sscc="086001571120000012", production_date="2026-03-23", packing_slip_number="100495"
    )
    second = make_carton(
        sscc="186001571120000029", production_date="2026-03-24", packing_slip_number="100600"
    )
    result = check_carton_for_pallet(second, [first], expected_count=5, pallet_test_mode=False)
    assert result.blocked_reason is None
    assert len(result.warnings) == 3


def test_first_scanned_carton_never_warns_against_itself():
    carton = make_carton()
    result = check_carton_for_pallet(carton, [], expected_count=5, pallet_test_mode=False)
    assert result.warnings == []
