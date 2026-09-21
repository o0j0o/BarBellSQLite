import csv

import pytest

from generate_labels import write_csv
from src.db.local_store import create_reprint_rows, fetch_label_history, record_generation_run
from src.labels import LabelRow


def make_rows(job_number="122984", sscc_prefix="086001571120000001"):
    """Two packages, two copies each - mirrors a real assemble_label_rows() run."""
    rows = []
    for package_index, (sscc, qty) in enumerate(
        [(f"{sscc_prefix}", 27000), (f"{sscc_prefix[:-1]}2", 7000)], start=1
    ):
        for copy_index in (1, 2):
            rows.append(
                LabelRow(
                    job_number=job_number,
                    packing_slip_number="100495",
                    customer_number="J00005",
                    customer_name="J. Wray & Nephew Ltd.",
                    product_no="47388",
                    item_number="233458",
                    item_description="233458 - JWN White O/P Rum B 750Ml USA - PS",
                    quantity=qty,
                    batch="12298447388",
                    production_date="2026-03-23",
                    sscc=sscc,
                    gtin="00051096184921",
                    package_index=package_index,
                    label_copy_index=copy_index,
                )
            )
    return rows


def test_record_generation_run_writes_job_and_label_rows(tmp_path):
    db_path = tmp_path / "barbell.db"
    rows = make_rows()

    flat_rows = record_generation_run(
        rows, units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    assert len(flat_rows) == 4  # 2 packages x 2 copies, same as rows
    assert db_path.exists()

    first = flat_rows[0]
    assert first.job_number == "122984"
    assert first.packing_slip_number == "100495"
    assert first.product_no == "47388"
    assert first.item_number == "233458"
    assert first.batch == "12298447388"
    assert first.gtin == "00051096184921"
    assert first.status == "original"
    assert first.superseded_id is None
    assert first.id is not None
    assert first.created_at  # non-empty timestamp


def test_record_generation_run_rejects_empty_rows(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="empty"):
        record_generation_run(
            [], units_per_package=1, labels_per_package=1, test_mode=False, db_path=tmp_path / "x.db"
        )


def test_rerunning_same_job_upserts_job_and_appends_new_labels(tmp_path):
    """A correction/reprint run against the SAME job number must not lose the
    original Labels history - Jobs is upserted (latest wins), but every
    Labels row from every run stays in the table."""
    db_path = tmp_path / "barbell.db"

    first_rows = make_rows()
    record_generation_run(
        first_rows, units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    # Second run: same job, different batch/description (simulating a corrected re-run)
    second_rows = make_rows()
    for r in second_rows:
        r.batch = "12298447388-CORRECTED"
        r.item_description = "CORRECTED DESCRIPTION"
        r.sscc = r.sscc + "X"

    record_generation_run(
        second_rows, units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    all_history = fetch_label_history(db_path, job_number="122984")
    assert len(all_history) == 8  # 4 from first run + 4 from second run, nothing lost

    # Jobs row now reflects the latest run
    assert all(r.batch == "12298447388-CORRECTED" for r in all_history)
    assert all(r.item_description == "CORRECTED DESCRIPTION" for r in all_history)


def test_fetch_label_history_filters_by_job_number(tmp_path):
    db_path = tmp_path / "barbell.db"
    record_generation_run(
        make_rows(job_number="111111"),
        units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path,
    )
    record_generation_run(
        make_rows(job_number="222222"),
        units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path,
    )

    only_111111 = fetch_label_history(db_path, job_number="111111")
    assert len(only_111111) == 4
    assert all(r.job_number == "111111" for r in only_111111)

    everything = fetch_label_history(db_path)
    assert len(everything) == 8


def test_fetch_label_history_filters_by_date(tmp_path):
    db_path = tmp_path / "barbell.db"
    rows = make_rows()
    for r in rows:
        r.production_date = "2026-05-01"
    record_generation_run(
        rows, units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    assert len(fetch_label_history(db_path, date="2026-05-01")) == 4
    assert len(fetch_label_history(db_path, date="2026-05-02")) == 0


def test_fetch_label_history_on_fresh_db_is_empty(tmp_path):
    db_path = tmp_path / "does_not_exist_yet.db"
    assert fetch_label_history(db_path) == []
    assert db_path.exists()  # schema is created on first touch


def test_flat_rows_feed_write_csv_unchanged_and_match_expected_columns(tmp_path):
    """The whole point of record_generation_run() returning FlatLabelRow -
    write_csv() (unchanged) must produce the same flat CSV it always has."""
    db_path = tmp_path / "barbell.db"
    rows = make_rows()
    flat_rows = record_generation_run(
        rows, units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    out_dir = tmp_path / "output"
    out_path = write_csv(flat_rows, out_dir, "122984", "100495", test_mode=False)

    with open(out_path, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert reader[0] == [
        "JobNumber", "PackingSlipNumber", "CustomerNumber", "CustomerName", "ProductNo",
        "ItemNumber", "ItemDescription", "Quantity", "Batch", "ProductionDate",
        "SSCC", "GTIN", "PackageIndex", "LabelCopyIndex",
    ]
    assert len(reader) == 5  # header + 4 label rows
    first_data_row = reader[1]
    assert first_data_row[0] == "122984"  # JobNumber
    assert first_data_row[4] == "47388"  # ProductNo
    assert first_data_row[7] == "27000"  # Quantity


# --- create_reprint_rows: reprint/void design (QUESTIONS.md #16) -----------

def test_create_reprint_rows_copies_original_data_and_links_superseded_id(tmp_path):
    db_path = tmp_path / "barbell.db"
    original_rows = record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    original = original_rows[0]

    reprints = create_reprint_rows([original.id], db_path=db_path)

    assert len(reprints) == 1
    reprint = reprints[0]
    assert reprint.status == "reprint"
    assert reprint.superseded_id == original.id
    assert reprint.id != original.id
    # same physical carton data as the original - job_number, sscc, carton
    # sequence, copy index, quantity are all unchanged
    assert reprint.job_number == original.job_number
    assert reprint.sscc == original.sscc
    assert reprint.package_index == original.package_index
    assert reprint.label_copy_index == original.label_copy_index
    assert reprint.quantity == original.quantity
    # job-level fields (from the Jobs join) carry through too
    assert reprint.batch == original.batch
    assert reprint.gtin == original.gtin


def test_create_reprint_rows_does_not_alter_or_delete_the_original(tmp_path):
    db_path = tmp_path / "barbell.db"
    original_rows = record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    original = original_rows[0]

    create_reprint_rows([original.id], db_path=db_path)

    still_there = [r for r in fetch_label_history(db_path) if r.id == original.id]
    assert len(still_there) == 1
    assert still_there[0].status == "original"
    assert still_there[0].superseded_id is None


def test_create_reprint_rows_handles_multiple_ids_in_given_order(tmp_path):
    db_path = tmp_path / "barbell.db"
    originals = record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    ids = [originals[0].id, originals[2].id, originals[1].id]  # deliberately out of order

    reprints = create_reprint_rows(ids, db_path=db_path)

    assert len(reprints) == 3
    assert [r.superseded_id for r in reprints] == ids  # same order as requested
    assert all(r.status == "reprint" for r in reprints)


def test_create_reprint_rows_appends_to_history_total_count(tmp_path):
    db_path = tmp_path / "barbell.db"
    originals = record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    create_reprint_rows([originals[0].id, originals[1].id], db_path=db_path)

    all_rows = fetch_label_history(db_path, job_number="122984")
    assert len(all_rows) == 6  # 4 original + 2 reprints, nothing lost


def test_create_reprint_rows_rejects_empty_list(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        create_reprint_rows([], db_path=tmp_path / "barbell.db")


def test_create_reprint_rows_rejects_unknown_id(tmp_path):
    db_path = tmp_path / "barbell.db"
    record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    with pytest.raises(ValueError, match="99999"):
        create_reprint_rows([99999], db_path=db_path)


def test_reprint_rows_feed_write_csv_in_the_same_flat_format(tmp_path):
    db_path = tmp_path / "barbell.db"
    originals = record_generation_run(
        make_rows(), units_per_package=27000, labels_per_package=2, test_mode=False, db_path=db_path
    )
    reprints = create_reprint_rows([originals[0].id], db_path=db_path)

    out_path = write_csv(reprints, tmp_path / "output", "reprint", "batch", test_mode=False)
    with open(out_path, newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    assert reader[0] == [
        "JobNumber", "PackingSlipNumber", "CustomerNumber", "CustomerName", "ProductNo",
        "ItemNumber", "ItemDescription", "Quantity", "Batch", "ProductionDate",
        "SSCC", "GTIN", "PackageIndex", "LabelCopyIndex",
    ]
    assert reader[1][10] == originals[0].sscc  # SSCC column unchanged from the original


# --- fetch_label_history: SSCC substring search ------------------------------

def _seed_ssccs(db_path, ssccs):
    rows = []
    for i, sscc in enumerate(ssccs, start=1):
        rows.append(
            LabelRow(
                job_number="122984", packing_slip_number="100495", customer_number="J00005",
                customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
                item_description="desc", quantity=100, batch="batch", production_date="2026-03-23",
                sscc=sscc, gtin="00051096184921", package_index=i, label_copy_index=1,
            )
        )
    record_generation_run(
        rows, units_per_package=100, labels_per_package=1, test_mode=False, db_path=db_path
    )


REAL_SSCCS = ["008600157112000000108", "008600157112000000115", "008600157112000001234"]


def test_sscc_search_matches_full_number(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    result = fetch_label_history(db_path, sscc_contains="008600157112000000115")
    assert [r.sscc for r in result] == ["008600157112000000115"]


def test_sscc_search_matches_company_prefix_fragment_anywhere(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    assert len(fetch_label_history(db_path, sscc_contains="86001571")) == 3


def test_sscc_search_matches_sequence_only_fragment(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    result = fetch_label_history(db_path, sscc_contains="1234")
    assert [r.sscc for r in result] == ["008600157112000001234"]


def test_sscc_search_matches_fragment_spanning_prefix_and_sequence(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    # "7112" (end of the GS1 prefix) + "0000001" (start of the sequence)
    result = fetch_label_history(db_path, sscc_contains="71120000001")
    assert {r.sscc for r in result} == {"008600157112000000108", "008600157112000000115"}


def test_sscc_search_is_case_insensitive(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, ["TEST-SSCC-00001", "TEST-SSCC-00002"])
    assert len(fetch_label_history(db_path, sscc_contains="test-sscc-00001")) == 1
    assert len(fetch_label_history(db_path, sscc_contains="SsCc")) == 2


def test_sscc_search_treats_like_wildcards_literally(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    assert fetch_label_history(db_path, sscc_contains="%") == []
    assert fetch_label_history(db_path, sscc_contains="_") == []


def test_sscc_search_combines_with_job_filter(tmp_path):
    db_path = tmp_path / "barbell.db"
    _seed_ssccs(db_path, REAL_SSCCS)
    assert len(fetch_label_history(db_path, job_number="122984", sscc_contains="1234")) == 1
    assert fetch_label_history(db_path, job_number="999999", sscc_contains="1234") == []
