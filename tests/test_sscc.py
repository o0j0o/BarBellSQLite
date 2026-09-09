import json

import pytest

from src.sscc import (
    SSCC_LENGTH,
    SSCCGenerator,
    archive_and_reset_state_file,
    build_sscc,
    build_test_sscc,
    get_counter_status,
    gs1_check_digit,
    serial_reference_width,
)

CLC_PREFIX = "08600157112"  # CLC's real GS1 Company Prefix


def test_check_digit_matches_known_gs1_worked_examples():
    """
    Independent verification against two worked examples that are widely
    cited in GS1's own documentation (not derived from this module), so a
    bug in the weighting/direction of the algorithm would show up here even
    if it happened to be self-consistent with build_sscc's own math.
    """
    assert gs1_check_digit("400638133393") == "1"  # -> EAN-13 4006381333931
    assert gs1_check_digit("629104150021") == "3"  # -> GTIN-13 6291041500213


def test_serial_reference_width_leaves_16_minus_prefix_digits():
    assert serial_reference_width(CLC_PREFIX) == 5  # 16 - 11
    assert serial_reference_width("123456") == 10  # 16 - 6


def test_serial_reference_width_rejects_prefix_too_long():
    with pytest.raises(ValueError):
        serial_reference_width("1234567890123456789")  # way more than 16 digits


def test_build_sscc_matches_hand_verified_example():
    """
    008600157112000012 was independently computed with a standalone script
    using the same algorithm before this module was written, to catch bugs
    in build_sscc's assembly (ordering, padding, widths) separately from the
    check-digit math itself.
    """
    assert build_sscc(CLC_PREFIX, "0", 1) == "008600157112000012"


def test_build_sscc_is_18_digits_and_all_numeric():
    sscc = build_sscc(CLC_PREFIX, "0", 42)
    assert len(sscc) == 18
    assert sscc.isdigit()


def test_build_sscc_rejects_serial_reference_overflow():
    max_serial = 10 ** serial_reference_width(CLC_PREFIX) - 1  # 99999
    build_sscc(CLC_PREFIX, "0", max_serial)  # should not raise
    with pytest.raises(ValueError):
        build_sscc(CLC_PREFIX, "0", max_serial + 1)


def test_build_sscc_rejects_bad_extension_digit():
    with pytest.raises(ValueError):
        build_sscc(CLC_PREFIX, "10", 1)  # two digits, not one
    with pytest.raises(ValueError):
        build_sscc(CLC_PREFIX, "x", 1)  # not a digit


class TestSSCCGenerator:
    def test_next_sscc_raises_if_never_initialized(self, tmp_path):
        gen = SSCCGenerator(CLC_PREFIX, "0", tmp_path / "sscc_state.json")
        with pytest.raises(FileNotFoundError):
            gen.next_sscc()

    def test_initialize_then_next_sscc_starts_at_requested_value(self, tmp_path):
        state_file = tmp_path / "sscc_state.json"
        gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
        gen.initialize(start_at=1)
        assert gen.next_sscc() == build_sscc(CLC_PREFIX, "0", 1)
        assert gen.next_sscc() == build_sscc(CLC_PREFIX, "0", 2)

    def test_initialize_refuses_to_overwrite_existing_state_file(self, tmp_path):
        state_file = tmp_path / "sscc_state.json"
        gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
        gen.initialize(start_at=1)
        with pytest.raises(FileExistsError):
            gen.initialize(start_at=1)

    def test_state_persists_across_separate_generator_instances(self, tmp_path):
        """
        The never-reuse guarantee depends on the counter surviving a process
        restart - simulate that by using a fresh SSCCGenerator instance
        pointed at the same state file, rather than reusing one in memory.
        """
        state_file = tmp_path / "sscc_state.json"
        SSCCGenerator(CLC_PREFIX, "0", state_file).initialize(start_at=1)

        first = SSCCGenerator(CLC_PREFIX, "0", state_file).next_sscc()
        second = SSCCGenerator(CLC_PREFIX, "0", state_file).next_sscc()

        assert first == build_sscc(CLC_PREFIX, "0", 1)
        assert second == build_sscc(CLC_PREFIX, "0", 2)
        assert first != second


class TestGetCounterStatus:
    def test_uninitialized_state_file(self, tmp_path):
        status = get_counter_status(tmp_path / "sscc_state.json")
        assert status.initialized is False
        assert status.last_serial is None
        assert status.next_serial is None

    def test_initialized_state_file_reflects_last_and_next_serial(self, tmp_path):
        state_file = tmp_path / "sscc_state.json"
        gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
        gen.initialize(start_at=10)
        gen.next_sscc()  # issues serial 10
        gen.next_sscc()  # issues serial 11

        status = get_counter_status(state_file)
        assert status.initialized is True
        assert status.last_serial == 11
        assert status.next_serial == 12

    def test_get_counter_status_never_issues_a_number(self, tmp_path):
        """Calling this for display purposes must not advance the counter."""
        state_file = tmp_path / "sscc_state.json"
        SSCCGenerator(CLC_PREFIX, "0", state_file).initialize(start_at=10)

        get_counter_status(state_file)
        get_counter_status(state_file)
        get_counter_status(state_file)

        assert get_counter_status(state_file).next_serial == 10


class TestArchiveAndResetStateFile:
    def test_raises_if_nothing_to_reset(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            archive_and_reset_state_file(tmp_path / "sscc_state.json", start_at=0)

    def test_archives_old_file_and_starts_fresh_counter(self, tmp_path):
        state_file = tmp_path / "sscc_state.json"
        gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
        gen.initialize(start_at=10)
        gen.next_sscc()  # issues serial 10, so last_serial=10 before reset

        archive_path = archive_and_reset_state_file(state_file, start_at=100)

        assert archive_path.exists()
        assert json.loads(archive_path.read_text())["last_serial"] == 10

        status = get_counter_status(state_file)
        assert status.initialized is True
        assert status.next_serial == 100  # fresh counter, not continuing from 11

    def test_reset_state_file_can_issue_new_ssccs(self, tmp_path):
        state_file = tmp_path / "sscc_state.json"
        SSCCGenerator(CLC_PREFIX, "0", state_file).initialize(start_at=10)
        archive_and_reset_state_file(state_file, start_at=500)

        gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
        assert gen.next_sscc() == build_sscc(CLC_PREFIX, "0", 500)


class TestBuildTestSscc:
    def test_format_is_obviously_not_a_real_sscc(self):
        value = build_test_sscc(1)
        assert value == "TEST-SSCC-00001"
        assert len(value) != SSCC_LENGTH  # can never be mistaken for a real 18-digit SSCC
        assert not value.isdigit()

    def test_sequence_numbers_are_unique_and_stable(self):
        assert build_test_sscc(0) == "TEST-SSCC-00000"
        assert build_test_sscc(20) == "TEST-SSCC-00020"
        assert build_test_sscc(1) != build_test_sscc(2)
