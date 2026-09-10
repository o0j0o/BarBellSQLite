import json

from src.audit import build_gtin_audit_record, record_gtin_audit


def test_build_gtin_audit_record_captures_all_required_fields():
    record = build_gtin_audit_record(
        job_number="122984",
        packing_slip_number="100495",
        product_no="47388",
        item_number="233458",
        bc_start_value="",
        gtin_used="00000012345670",
        gtin_source="manual_entry_empty_field",
        test_mode=False,
    )
    assert record.job_number == "122984"
    assert record.packing_slip_number == "100495"
    assert record.product_no == "47388"
    assert record.item_number == "233458"
    assert record.bc_start_value == ""
    assert record.gtin_used == "00000012345670"
    assert record.gtin_source == "manual_entry_empty_field"
    assert record.test_mode is False
    assert record.username  # OS username, non-empty
    assert "T" in record.timestamp  # ISO 8601


def test_record_gtin_audit_appends_one_json_line_per_call(tmp_path):
    log_file = tmp_path / "gtin_audit_log.jsonl"
    record1 = build_gtin_audit_record(
        job_number="122984",
        packing_slip_number="100495",
        product_no="47388",
        item_number="233458",
        bc_start_value=None,
        gtin_used="00000012345670",
        gtin_source="manual_entry_empty_field",
        test_mode=True,
    )
    record2 = build_gtin_audit_record(
        job_number="29056",
        packing_slip_number="30",
        product_no="77",
        item_number="",
        bc_start_value="0 51096 18492 1",
        gtin_used="00051096184921",
        gtin_source="label_traxx",
        test_mode=False,
    )

    record_gtin_audit(record1, log_file)
    record_gtin_audit(record2, log_file)

    lines = log_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["job_number"] == "122984"
    assert json.loads(lines[1])["job_number"] == "29056"


def test_record_gtin_audit_creates_parent_directories(tmp_path):
    log_file = tmp_path / "nested" / "dir" / "gtin_audit_log.jsonl"
    record = build_gtin_audit_record(
        job_number="1",
        packing_slip_number="1",
        product_no="1",
        item_number="1",
        bc_start_value=None,
        gtin_used="00000012345670",
        gtin_source="manual_entry_empty_field",
        test_mode=True,
    )
    record_gtin_audit(record, log_file)
    assert log_file.exists()
