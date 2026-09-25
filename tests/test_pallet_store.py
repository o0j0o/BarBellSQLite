import sqlite3

import pytest

from src.db.local_store import (
    create_pallet,
    fetch_label_history,
    find_carton_by_sscc,
    record_generation_run,
    void_pallet,
)
from src.labels import LabelRow


def make_carton_rows(job_number="122984", ssccs=("086001571120000012", "086001571120000029")):
    """Two cartons under one job/batch/GTIN, one copy each - mirrors a real
    assemble_label_rows() run, small enough to build pallets from directly."""
    return [
        LabelRow(
            job_number=job_number, packing_slip_number="100495", customer_number="J00005",
            customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
            item_description="233458 - JWN White O/P Rum B 750Ml USA - PS", quantity=10000,
            batch="12298447388", production_date="2026-03-23", sscc=sscc,
            gtin="00051096184921", package_index=i, label_copy_index=1,
        )
        for i, sscc in enumerate(ssccs, start=1)
    ]


def seed(db_path, job_number="122984", ssccs=("086001571120000012", "086001571120000029")):
    record_generation_run(
        make_carton_rows(job_number, ssccs),
        units_per_package=10000, labels_per_package=1, test_mode=False, db_path=db_path,
    )
    return ssccs


# --- find_carton_by_sscc ----------------------------------------------------

def test_find_carton_by_sscc_returns_full_info(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)

    carton = find_carton_by_sscc(ssccs[0], db_path)

    assert carton is not None
    assert carton.sscc == ssccs[0]
    assert carton.job_number == "122984"
    assert carton.product_no == "47388"
    assert carton.gtin == "00051096184921"
    assert carton.batch == "12298447388"
    assert carton.quantity == 10000
    assert carton.production_date == "2026-03-23"
    assert carton.packing_slip_number == "100495"
    assert carton.status == "original"
    assert carton.pallet_sscc is None
    assert carton.label_type == "CARTON"
    assert carton.test_mode is False
    assert carton.extension_digit == ssccs[0][0]


def test_find_carton_by_sscc_returns_none_for_unknown_sscc(tmp_path):
    db_path = tmp_path / "barbell.db"
    seed(db_path)
    assert find_carton_by_sscc("999999999999999999", db_path) is None


def test_find_carton_by_sscc_never_returns_a_pallet_row(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)
    pallet = create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )
    assert pallet  # sanity

    assert find_carton_by_sscc("086001571120099999", db_path) is None


# --- create_pallet -----------------------------------------------------------

def test_create_pallet_inserts_two_identical_rows_and_links_cartons(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)

    pallet_rows = create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )

    assert len(pallet_rows) == 2  # 2 identical print copies
    for row in pallet_rows:
        assert row.sscc == "086001571120099999"
        assert row.label_type == "PALLET"
        assert row.carton_count == 2
        assert row.quantity == 20000
        assert row.job_number == "122984"
        assert row.product_no == "47388"
        assert row.gtin == "00051096184921"
        assert row.batch == "12298447388"
        assert row.status == "original"
        assert row.pallet_sscc is None  # not meaningful on a pallet row itself
    assert {row.label_copy_index for row in pallet_rows} == {1, 2}

    for sscc in ssccs:
        carton = find_carton_by_sscc(sscc, db_path)
        assert carton.pallet_sscc == "086001571120099999"


def test_create_pallet_links_every_print_copy_of_a_scanned_carton(tmp_path):
    """A physical carton can have more than one label row (multiple print
    copies sharing the same SSCC) - linking it to a pallet must stamp
    pallet_sscc on all of them, not just the one find_carton_by_sscc()
    happens to return."""
    db_path = tmp_path / "barbell.db"
    two_copies = [
        LabelRow(
            job_number="122984", packing_slip_number="100495", customer_number="J00005",
            customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
            item_description="desc", quantity=10000, batch="12298447388",
            production_date="2026-03-23", sscc="086001571120000012", gtin="00051096184921",
            package_index=1, label_copy_index=copy,
        )
        for copy in (1, 2)
    ]
    record_generation_run(
        two_copies, units_per_package=10000, labels_per_package=2, test_mode=False, db_path=db_path
    )

    create_pallet(
        carton_ssccs=["086001571120000012"], job_number="122984", quantity=10000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=1, db_path=db_path,
    )

    rows = [r for r in fetch_label_history(db_path, job_number="122984") if r.label_type == "CARTON"]
    assert len(rows) == 2
    assert all(r.pallet_sscc == "086001571120099999" for r in rows)


def test_create_pallet_rejects_empty_carton_list(tmp_path):
    with pytest.raises(ValueError, match="empty"):
        create_pallet(
            carton_ssccs=[], job_number="122984", quantity=0, production_date="2026-03-23",
            packing_slip_number="100495", pallet_sscc="086001571120099999", carton_count=0,
            db_path=tmp_path / "barbell.db",
        )


def test_create_pallet_rejects_unknown_job(tmp_path):
    db_path = tmp_path / "barbell.db"
    seed(db_path)
    with pytest.raises(ValueError, match="999999"):
        create_pallet(
            carton_ssccs=["086001571120000012"], job_number="999999", quantity=10000,
            production_date="2026-03-23", packing_slip_number="100495",
            pallet_sscc="086001571120099999", carton_count=1, db_path=db_path,
        )


# --- void_pallet --------------------------------------------------------------

def test_void_pallet_marks_pallet_void_and_frees_cartons(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)
    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )

    freed = void_pallet("086001571120099999", db_path)

    assert freed == 2  # both cartons freed
    all_rows = fetch_label_history(db_path, job_number="122984")
    pallet_rows = [r for r in all_rows if r.label_type == "PALLET"]
    carton_rows = [r for r in all_rows if r.label_type == "CARTON"]
    assert len(pallet_rows) == 2
    assert all(r.status == "void" for r in pallet_rows)
    assert all(r.pallet_sscc is None for r in carton_rows)  # freed - can be re-scanned


def test_void_pallet_rejects_unknown_pallet_sscc(tmp_path):
    db_path = tmp_path / "barbell.db"
    seed(db_path)
    with pytest.raises(ValueError, match="086001571120099999"):
        void_pallet("086001571120099999", db_path)


def test_voided_pallet_cartons_can_be_scanned_onto_a_new_pallet(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)
    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )
    void_pallet("086001571120099999", db_path)

    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120088888", carton_count=2, db_path=db_path,
    )

    for sscc in ssccs:
        assert find_carton_by_sscc(sscc, db_path).pallet_sscc == "086001571120088888"


# --- fetch_label_history: searching by pallet SSCC --------------------------

def test_sscc_search_finds_pallet_and_its_cartons(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)
    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )

    results = fetch_label_history(db_path, sscc_contains="086001571120099999")
    label_types = {r.label_type for r in results}
    sccs = {r.sscc for r in results}

    assert label_types == {"CARTON", "PALLET"}
    # 2 pallet copies + the 2 cartons now linked to it
    assert len(results) == 4
    assert ssccs[0] in sccs and ssccs[1] in sccs


# --- migration: old databases from before this feature -----------------------

_OLD_SCHEMA = """
CREATE TABLE jobs (
    job_number TEXT PRIMARY KEY,
    packing_slip_number TEXT NOT NULL,
    product_no TEXT NOT NULL,
    item_number TEXT NOT NULL,
    item_description TEXT NOT NULL,
    customer_number TEXT,
    customer_name TEXT,
    batch TEXT NOT NULL,
    production_date TEXT NOT NULL,
    gtin TEXT,
    units_per_package INTEGER NOT NULL,
    labels_per_package INTEGER NOT NULL,
    test_mode INTEGER NOT NULL DEFAULT 0,
    created_by TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_number TEXT NOT NULL REFERENCES jobs(job_number),
    sscc TEXT NOT NULL,
    carton_sequence INTEGER NOT NULL,
    label_copy_index INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'original' CHECK (status IN ('original', 'void', 'reprint')),
    superseded_id INTEGER REFERENCES labels(id),
    created_at TEXT NOT NULL
);
"""


def _make_old_style_db(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.executescript(_OLD_SCHEMA)
    conn.execute(
        "INSERT INTO jobs (job_number, packing_slip_number, product_no, item_number, "
        "item_description, customer_number, customer_name, batch, production_date, gtin, "
        "units_per_package, labels_per_package, test_mode, created_by, created_at, updated_at) "
        "VALUES ('122984','100495','47388','233458','desc','J00005','JWN','12298447388',"
        "'2026-03-23','00051096184921',27000,1,0,'greg','2026-03-23T00:00:00','2026-03-23T00:00:00')"
    )
    conn.execute(
        "INSERT INTO labels (job_number, sscc, carton_sequence, label_copy_index, quantity, "
        "status, superseded_id, created_at) VALUES "
        "('122984','086001571120000012',1,1,27000,'original',NULL,'2026-03-23T00:00:00')"
    )
    conn.commit()
    conn.close()


def test_migration_adds_columns_to_an_old_database_without_losing_data(tmp_path):
    db_path = tmp_path / "old_barbell.db"
    _make_old_style_db(db_path)

    history = fetch_label_history(db_path)  # any public call opens/migrates the DB

    assert len(history) == 1
    row = history[0]
    assert row.sscc == "086001571120000012"
    assert row.label_type == "CARTON"  # new column, correct default
    assert row.pallet_sscc is None
    assert row.carton_count is None
    # backfilled from the jobs row, since this pre-existing row had no
    # per-row snapshot of its own
    assert find_carton_by_sscc("086001571120000012", db_path).production_date == "2026-03-23"
    assert find_carton_by_sscc("086001571120000012", db_path).packing_slip_number == "100495"


def test_migration_backs_up_the_db_file_before_altering_it(tmp_path):
    db_path = tmp_path / "old_barbell.db"
    _make_old_style_db(db_path)

    assert list(tmp_path.glob("old_barbell.backup-*.db")) == []
    fetch_label_history(db_path)
    backups = list(tmp_path.glob("old_barbell.backup-*.db"))
    assert len(backups) == 1

    # the backup is the OLD schema - no label_type column
    old_conn = sqlite3.connect(str(backups[0]))
    old_columns = {row[1] for row in old_conn.execute("PRAGMA table_info(labels)").fetchall()}
    old_conn.close()
    assert "label_type" not in old_columns


def test_migration_is_idempotent_no_repeat_backup_or_data_loss(tmp_path):
    db_path = tmp_path / "old_barbell.db"
    _make_old_style_db(db_path)

    fetch_label_history(db_path)  # first call: migrates + backs up
    fetch_label_history(db_path)  # second call: must be a no-op
    fetch_label_history(db_path)  # third call: still a no-op

    assert len(list(tmp_path.glob("old_barbell.backup-*.db"))) == 1
    assert len(fetch_label_history(db_path)) == 1  # data still intact


def test_migration_is_a_no_op_on_a_brand_new_database(tmp_path):
    """A fresh database already has every column from _SCHEMA - nothing to
    migrate, so no backup file should ever appear."""
    db_path = tmp_path / "brand_new.db"
    seed(db_path)
    assert list(tmp_path.glob("brand_new.backup-*.db")) == []


# --- count_pallets ------------------------------------------------------------

from src.db.local_store import count_pallets


def test_count_pallets_counts_distinct_pallet_ssccs_not_print_copies(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed(db_path)
    assert count_pallets(db_path) == 0

    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=20000,
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc="086001571120099999", carton_count=2, db_path=db_path,
    )
    assert count_pallets(db_path) == 1  # 2 rows (copies), 1 distinct pallet


def test_count_pallets_zero_on_fresh_db(tmp_path):
    assert count_pallets(tmp_path / "fresh.db") == 0
