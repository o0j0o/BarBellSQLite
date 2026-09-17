"""
Local SQLite store for BarBell's own generation history - separate from
Label Traxx, which stays read-only (see src/db/readonly_connection.py). This
is BarBell's own writable data, not Label Traxx's.

Two tables:
  - jobs: one row per job number, holding the job-level control data
    (packing slip, P/N, item number, batch, production date, customer, the
    GTIN actually used, package sizing, test-mode flag) - upserted on every
    generation run against that job number, so it always reflects the most
    recent run. See QUESTIONS.md #14: this assumes one product per job
    number in practice; re-running the same job number for a different
    product overwrites its Jobs row.
  - labels: one row per individual label actually written to a CSV - SSCC,
    carton sequence (which physical package), label copy index, quantity,
    a status (original/void/reprint), and superseded_id linking a reprint
    row back to the row it replaces. The auto-increment id is the primary
    key - NOT the SSCC or batch - since an SSCC can legitimately repeat
    across a correction/reprint of the same carton. Void/reprint is
    schema-only for now: every row record_generation_run() writes is
    'original' with no superseded_id - there's no GUI action yet to create
    a void or reprint (see QUESTIONS.md #14).

CSV export sources its rows from a JOIN of these two tables (see
record_generation_run() and fetch_label_history() below), not directly from
the in-memory rows assemble_label_rows() returns - so a CSV always reflects
what's actually logged, and the GUI history viewer is reading the same data
a BarTender run would have used. FlatLabelRow deliberately reuses
src.labels.LabelRow's field names for the CSV-shaped fields, so
write_csv()/BarBellApp._write_csv() work unchanged on either type.

Reprints (create_reprint_rows()): selecting rows in the GUI history viewer
and exporting them again appends a NEW 'reprint' Labels row per selection -
same job_number/sscc/carton_sequence/label_copy_index/quantity as the
original, superseded_id pointing back at it - and never touches the
original row. See QUESTIONS.md #16.
"""

import csv
import getpass
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

STATUS_ORIGINAL = "original"
STATUS_VOID = "void"
STATUS_REPRINT = "reprint"
VALID_STATUSES = (STATUS_ORIGINAL, STATUS_VOID, STATUS_REPRINT)

# The one flat CSV column list every BarBell CSV writer uses (BarTender's
# expected format) - shared so record-generation and reprint-export CSVs
# can never drift apart.
CSV_FIELDNAMES = [
    "JobNumber", "PackingSlipNumber", "CustomerNumber", "CustomerName", "ProductNo",
    "ItemNumber", "ItemDescription", "Quantity", "Batch", "ProductionDate",
    "SSCC", "GTIN", "PackageIndex", "LabelCopyIndex",
]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
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

CREATE TABLE IF NOT EXISTS labels (
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

_JOIN_SELECT = """
SELECT
    j.job_number, j.packing_slip_number, j.customer_number, j.customer_name,
    j.product_no, j.item_number, j.item_description, l.quantity, j.batch,
    j.production_date, l.sscc, j.gtin, l.carton_sequence, l.label_copy_index,
    l.id, l.status, l.superseded_id, l.created_at, j.test_mode
FROM labels l
JOIN jobs j ON j.job_number = l.job_number
"""


def _connect(db_path: Path | str) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    return conn


@dataclass
class FlatLabelRow:
    """One flattened Jobs+Labels row. The first 14 fields are exactly
    src.labels.LabelRow's shape (same names), so anything that writes a CSV
    from a list of LabelRow works unchanged on a list of these. The rest are
    history-only fields the GUI viewer shows and the CSV doesn't need."""

    job_number: str
    packing_slip_number: str
    customer_number: str
    customer_name: str
    product_no: str
    item_number: str
    item_description: str
    quantity: int
    batch: str
    production_date: str
    sscc: str
    gtin: str | None
    package_index: int
    label_copy_index: int
    id: int | None = None
    status: str = STATUS_ORIGINAL
    superseded_id: int | None = None
    created_at: str = ""
    test_mode: bool = False


def _row_to_flat(row) -> FlatLabelRow:
    return FlatLabelRow(
        job_number=row[0],
        packing_slip_number=row[1],
        customer_number=row[2],
        customer_name=row[3],
        product_no=row[4],
        item_number=row[5],
        item_description=row[6],
        quantity=row[7],
        batch=row[8],
        production_date=row[9],
        sscc=row[10],
        gtin=row[11],
        package_index=row[12],
        label_copy_index=row[13],
        id=row[14],
        status=row[15],
        superseded_id=row[16],
        created_at=row[17],
        test_mode=bool(row[18]),
    )


def record_generation_run(
    rows,  # list[src.labels.LabelRow]
    *,
    units_per_package: int,
    labels_per_package: int,
    test_mode: bool,
    db_path: Path | str,
) -> list[FlatLabelRow]:
    """
    Upserts the Jobs row for rows[0].job_number (every row in a single run
    shares the same job/packing slip/product) and appends one Labels row per
    entry in `rows`, all in one transaction. Then re-reads exactly those rows
    back via the Jobs+Labels join, so what's returned - and therefore the
    CSV built from it - reflects what's actually in the database.
    """
    if not rows:
        raise ValueError("rows is empty - nothing to record")

    first = rows[0]
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO jobs (
                job_number, packing_slip_number, product_no, item_number,
                item_description, customer_number, customer_name, batch,
                production_date, gtin, units_per_package, labels_per_package,
                test_mode, created_by, created_at, updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(job_number) DO UPDATE SET
                packing_slip_number = excluded.packing_slip_number,
                product_no = excluded.product_no,
                item_number = excluded.item_number,
                item_description = excluded.item_description,
                customer_number = excluded.customer_number,
                customer_name = excluded.customer_name,
                batch = excluded.batch,
                production_date = excluded.production_date,
                gtin = excluded.gtin,
                units_per_package = excluded.units_per_package,
                labels_per_package = excluded.labels_per_package,
                test_mode = excluded.test_mode,
                created_by = excluded.created_by,
                updated_at = excluded.updated_at
            """,
            (
                first.job_number,
                first.packing_slip_number,
                first.product_no,
                first.item_number,
                first.item_description,
                first.customer_number,
                first.customer_name,
                first.batch,
                first.production_date,
                first.gtin,
                units_per_package,
                labels_per_package,
                int(test_mode),
                getpass.getuser(),
                now,
                now,
            ),
        )

        label_ids = []
        for r in rows:
            cur = conn.execute(
                """
                INSERT INTO labels (
                    job_number, sscc, carton_sequence, label_copy_index,
                    quantity, status, superseded_id, created_at
                ) VALUES (?, ?, ?, ?, ?, 'original', NULL, ?)
                """,
                (r.job_number, r.sscc, r.package_index, r.label_copy_index, r.quantity, now),
            )
            label_ids.append(cur.lastrowid)
        conn.commit()

        placeholders = ",".join("?" * len(label_ids))
        cur = conn.execute(
            f"{_JOIN_SELECT} WHERE l.id IN ({placeholders}) ORDER BY l.id", label_ids
        )
        return [_row_to_flat(row) for row in cur.fetchall()]
    finally:
        conn.close()


def fetch_label_history(
    db_path: Path | str,
    job_number: str | None = None,
    date: str | None = None,
) -> list[FlatLabelRow]:
    """For the GUI history viewer - every logged label, optionally filtered
    to an exact job number and/or production date, most recent first."""
    conn = _connect(db_path)
    try:
        query = _JOIN_SELECT
        clauses = []
        params = []
        if job_number:
            clauses.append("j.job_number = ?")
            params.append(job_number)
        if date:
            clauses.append("j.production_date = ?")
            params.append(date)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY l.id DESC"
        cur = conn.execute(query, params)
        return [_row_to_flat(row) for row in cur.fetchall()]
    finally:
        conn.close()


def write_flat_csv(rows, out_path: Path | str) -> Path:
    """Writes `rows` (LabelRow- or FlatLabelRow-shaped - anything with the
    14 CSV_FIELDNAMES-matching attributes) to out_path in BarTender's flat
    format. The one place that format is written, so record-generation and
    reprint-export CSVs can never drift apart."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_FIELDNAMES)
        for r in rows:
            writer.writerow(
                [
                    r.job_number, r.packing_slip_number, r.customer_number, r.customer_name,
                    r.product_no, r.item_number, r.item_description, r.quantity, r.batch,
                    r.production_date, r.sscc, r.gtin or "", r.package_index, r.label_copy_index,
                ]
            )
    return out_path


def create_reprint_rows(label_ids: list[int], db_path: Path | str) -> list[FlatLabelRow]:
    """
    For each given labels.id, appends a NEW 'reprint' row copying that
    label's job_number/sscc/carton_sequence/label_copy_index/quantity -
    the original row is never modified or deleted. Returns the newly
    created rows, flattened via the same Jobs+Labels join used everywhere
    else, in the same order label_ids was given (so index 0 of the result
    is the reprint of label_ids[0], etc).
    """
    if not label_ids:
        raise ValueError("label_ids is empty - nothing to reprint")

    now = datetime.now(timezone.utc).isoformat()
    conn = _connect(db_path)
    try:
        new_ids = []
        for original_id in label_ids:
            cur = conn.execute(
                "SELECT job_number, sscc, carton_sequence, label_copy_index, quantity "
                "FROM labels WHERE id = ?",
                (original_id,),
            )
            original = cur.fetchone()
            if original is None:
                raise ValueError(f"No labels row found for id {original_id!r} - nothing to reprint")
            job_number, sscc, carton_sequence, label_copy_index, quantity = original

            cur = conn.execute(
                """
                INSERT INTO labels (
                    job_number, sscc, carton_sequence, label_copy_index,
                    quantity, status, superseded_id, created_at
                ) VALUES (?, ?, ?, ?, ?, 'reprint', ?, ?)
                """,
                (job_number, sscc, carton_sequence, label_copy_index, quantity, original_id, now),
            )
            new_ids.append(cur.lastrowid)
        conn.commit()

        placeholders = ",".join("?" * len(new_ids))
        cur = conn.execute(f"{_JOIN_SELECT} WHERE l.id IN ({placeholders})", new_ids)
        rows_by_id = {row[14]: _row_to_flat(row) for row in cur.fetchall()}  # column 14 is l.id
        return [rows_by_id[new_id] for new_id in new_ids]
    finally:
        conn.close()
