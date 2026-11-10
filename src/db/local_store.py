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

Pallets (create_reprint_rows()'s label_type='PALLET' sibling,
find_carton_by_sscc()/create_pallet()/void_pallet()): a pallet is a row in
this SAME labels table, not a separate table - label_type distinguishes
CARTON from PALLET, pallet_sscc (carton rows only) links a carton to the
pallet it's been scanned onto, carton_count (pallet rows only) records how
many cartons it actually carries. See QUESTIONS.md #18 and
barbell_gui.py's Pallet screen.

Production dates are stored as YYMMDD (src/dates.py). Databases from before
that hold YYYY-MM-DD; _migrate_production_dates() rewrites them in place the
first time such a database is opened (after backing the file up), and every
write path below normalises its input, so the two forms never coexist.

labels.production_date/packing_slip_number are per-row snapshots, separate
from jobs.production_date/packing_slip_number (which stay the current,
possibly-since-overwritten value for a job_number, unchanged in behaviour
for CSV/history). The per-row copies exist because the pallet screen needs
to compare what was actually true for EACH scanned carton at the time it
was printed - jobs' one-value-per-job-number, last-write-wins storage can't
represent that once a job's been regenerated. Existing code (CSV export,
the history viewer's own columns) keeps reading the jobs-joined values
unchanged; only pallet logic reads the new per-row columns.
"""

import csv
import getpass
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.dates import normalize_production_date

STATUS_ORIGINAL = "original"
STATUS_VOID = "void"
STATUS_REPRINT = "reprint"
VALID_STATUSES = (STATUS_ORIGINAL, STATUS_VOID, STATUS_REPRINT)

LABEL_TYPE_CARTON = "CARTON"
LABEL_TYPE_PALLET = "PALLET"
VALID_LABEL_TYPES = (LABEL_TYPE_CARTON, LABEL_TYPE_PALLET)

# The one flat CSV column list every BarBell CSV writer uses (BarTender's
# expected format) - shared so record-generation, reprint-export, and
# pallet CSVs can never drift apart.
CSV_FIELDNAMES = [
    "JobNumber", "PackingSlipNumber", "CustomerNumber", "CustomerName", "ProductNo",
    "ItemNumber", "ItemDescription", "Quantity", "Batch", "ProductionDate",
    "SSCC", "GTIN", "PackageIndex", "LabelCopyIndex", "CartonCount", "LabelType",
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
    created_at TEXT NOT NULL,
    label_type TEXT NOT NULL DEFAULT 'CARTON' CHECK (label_type IN ('CARTON', 'PALLET')),
    pallet_sscc TEXT,
    carton_count INTEGER,
    production_date TEXT,
    packing_slip_number TEXT
);

CREATE TABLE IF NOT EXISTS setup_credentials (
    name TEXT PRIMARY KEY,
    password_hash TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

# (column, DDL for ALTER TABLE ... ADD COLUMN) for labels columns added after
# the table's original release - see _migrate_labels_table(). New databases
# get these straight from _SCHEMA above; this is only exercised against a
# barbell.db/barbell_demo.db from before this column existed.
_LABELS_MIGRATION_COLUMNS = [
    ("label_type", "TEXT NOT NULL DEFAULT 'CARTON' CHECK (label_type IN ('CARTON', 'PALLET'))"),
    ("pallet_sscc", "TEXT"),
    ("carton_count", "INTEGER"),
    ("production_date", "TEXT"),
    ("packing_slip_number", "TEXT"),
]

_JOIN_SELECT = """
SELECT
    j.job_number, j.packing_slip_number, j.customer_number, j.customer_name,
    j.product_no, j.item_number, j.item_description, l.quantity, j.batch,
    j.production_date, l.sscc, j.gtin, l.carton_sequence, l.label_copy_index,
    l.id, l.status, l.superseded_id, l.created_at, j.test_mode,
    l.label_type, l.pallet_sscc, l.carton_count
FROM labels l
JOIN jobs j ON j.job_number = l.job_number
"""


def _backup_db_file(db_path: Path) -> Path | None:
    """Timestamped copy, never overwritten, alongside the original - same
    treatment src/sscc.py's archive_and_reset_state_file() gives the SSCC
    counter file. Returns None if there's nothing to back up yet (a
    brand-new database - schema creation isn't a migration)."""
    if not db_path.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = db_path.with_name(f"{db_path.stem}.backup-{timestamp}{db_path.suffix}")
    shutil.copy2(db_path, backup_path)
    return backup_path


def _migrate_labels_table(conn: sqlite3.Connection, db_path: Path) -> bool:
    """
    Adds any labels columns missing from an existing database (one from
    before the Pallet Labels feature). Safe to call every time a connection
    is opened: a no-op, and no backup taken, once the columns already
    exist - so running it repeatedly (every app start) never re-backs-up or
    re-alters anything. Backs up the .db file only when it's actually about
    to change the schema. Returns True if it took that backup.
    """
    existing_columns = {row[1] for row in conn.execute("PRAGMA table_info(labels)").fetchall()}
    missing = [
        (name, ddl) for name, ddl in _LABELS_MIGRATION_COLUMNS if name not in existing_columns
    ]
    if not missing:
        return False

    _backup_db_file(db_path)
    for name, ddl in missing:
        conn.execute(f"ALTER TABLE labels ADD COLUMN {name} {ddl}")

    # Best-effort backfill for pre-existing rows, from the CURRENT jobs
    # values - the best available guess, not necessarily the historical
    # truth if that job's been regenerated since (see the module docstring).
    # Rows inserted from here on get their own accurate per-row value at
    # insert time instead (record_generation_run()/create_reprint_rows()).
    if "production_date" in dict(missing):
        conn.execute(
            "UPDATE labels SET production_date = "
            "(SELECT production_date FROM jobs WHERE jobs.job_number = labels.job_number) "
            "WHERE production_date IS NULL"
        )
    if "packing_slip_number" in dict(missing):
        conn.execute(
            "UPDATE labels SET packing_slip_number = "
            "(SELECT packing_slip_number FROM jobs WHERE jobs.job_number = labels.job_number) "
            "WHERE packing_slip_number IS NULL"
        )
    conn.commit()
    return True


_LEGACY_ISO_DATE_LIKE = "____-__-__"  # SQL LIKE: YYYY-MM-DD, '_' = any one character


def _migrate_production_dates(
    conn: sqlite3.Connection, db_path: Path, already_backed_up: bool = False
) -> None:
    """
    Rewrites any production_date still in the old YYYY-MM-DD form (jobs and
    labels) to YYMMDD. A no-op - and no backup taken - once none are left, so
    it's safe to run every time a connection opens. Backs up the .db file
    only when it's actually about to change data, and not again if this same
    open already backed it up for the labels schema migration.
    """
    has_legacy = any(
        conn.execute(
            f"SELECT 1 FROM {table} WHERE production_date LIKE ? LIMIT 1", (_LEGACY_ISO_DATE_LIKE,)
        ).fetchone()
        for table in ("jobs", "labels")
    )
    if not has_legacy:
        return

    if not already_backed_up:
        _backup_db_file(db_path)
    for table in ("jobs", "labels"):
        # 'YYYY-MM-DD' -> characters 3-4 (YY), 6-7 (MM), 9-10 (DD)
        conn.execute(
            f"UPDATE {table} SET production_date = "
            "substr(production_date, 3, 2) || substr(production_date, 6, 2) || substr(production_date, 9, 2) "
            "WHERE production_date LIKE ?",
            (_LEGACY_ISO_DATE_LIKE,),
        )
    conn.commit()


def _connect(db_path: Path | str) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(_SCHEMA)
    backed_up = _migrate_labels_table(conn, db_path)
    _migrate_production_dates(conn, db_path, already_backed_up=backed_up)
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
    label_type: str = LABEL_TYPE_CARTON
    pallet_sscc: str | None = None
    carton_count: int | None = None


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
        label_type=row[19],
        pallet_sscc=row[20],
        carton_count=row[21],
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
    first_production_date = normalize_production_date(first.production_date)
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
                first_production_date,
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
                    quantity, status, superseded_id, created_at,
                    production_date, packing_slip_number
                ) VALUES (?, ?, ?, ?, ?, 'original', NULL, ?, ?, ?)
                """,
                (
                    r.job_number, r.sscc, r.package_index, r.label_copy_index, r.quantity, now,
                    normalize_production_date(r.production_date), r.packing_slip_number,
                ),
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


def _history_filters(
    job_number: str | None,
    date: str | None,
    sscc_contains: str | None,
    since_days: int | None,
    hide_test: bool,
    now: datetime | None = None,
) -> tuple[list[str], list]:
    """The WHERE clauses (and their values) shared by fetch_label_history() and
    count_label_history(), so what the list shows and what the 'N hidden' line
    counts can never disagree."""
    clauses: list[str] = []
    params: list = []
    if job_number:
        clauses.append("j.job_number = ?")
        params.append(job_number)
    if date:
        try:
            date = normalize_production_date(date)  # accepts YYMMDD (or the old YYYY-MM-DD)
        except ValueError:
            pass  # not a valid date - match it as typed (finds nothing)
        clauses.append("j.production_date = ?")
        params.append(date)
    if sscc_contains:
        # Escape LIKE wildcards so what the user types is matched literally.
        escaped = sscc_contains.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        clauses.append("(l.sscc LIKE ? ESCAPE '\\' OR l.pallet_sscc LIKE ? ESCAPE '\\')")
        params.append(f"%{escaped}%")
        params.append(f"%{escaped}%")
    if since_days is not None:
        # created_at is stored as a UTC ISO-8601 string, which sorts the same as time does
        cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=since_days)
        clauses.append("l.created_at >= ?")
        params.append(cutoff.astimezone(timezone.utc).isoformat(timespec="microseconds"))
    if hide_test:
        clauses.append("j.test_mode = 0")
    return clauses, params


def fetch_label_history(
    db_path: Path | str,
    job_number: str | None = None,
    date: str | None = None,
    sscc_contains: str | None = None,
    since_days: int | None = None,
    hide_test: bool = False,
) -> list[FlatLabelRow]:
    """For the GUI history viewer - every logged label, optionally filtered
    to an exact job number and/or production date, and/or to SSCCs containing
    `sscc_contains` anywhere (substring, so a prefix, a sequence number, or a
    fragment spanning both all work - the full SSCC is never required).
    Matches against a pallet's OWN sscc and, separately, against carton
    rows' pallet_sscc - so searching a pallet's SSCC brings back the pallet
    row and every carton scanned onto it. SQLite's LIKE is case-insensitive
    for ASCII, covering SSCCs with letters (e.g. TEST-SSCC-#####). Most
    recent first.

    since_days limits the list to labels logged in the last N days, and
    hide_test drops test-mode labels. Both only change what is LISTED - nothing
    is ever deleted - and the history viewer turns both off whenever the user
    is searching, so an old or test label can always be found."""
    conn = _connect(db_path)
    try:
        query = _JOIN_SELECT
        clauses, params = _history_filters(job_number, date, sscc_contains, since_days, hide_test)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY l.id DESC"
        cur = conn.execute(query, params)
        return [_row_to_flat(row) for row in cur.fetchall()]
    finally:
        conn.close()


def count_label_history(
    db_path: Path | str,
    job_number: str | None = None,
    date: str | None = None,
    sscc_contains: str | None = None,
    since_days: int | None = None,
    hide_test: bool = False,
) -> int:
    """How many rows fetch_label_history() would return for the same filters
    (used for the 'N hidden' line in the history viewer)."""
    conn = _connect(db_path)
    try:
        clauses, params = _history_filters(job_number, date, sscc_contains, since_days, hide_test)
        query = "SELECT COUNT(*) FROM labels l JOIN jobs j ON j.job_number = l.job_number"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        return conn.execute(query, params).fetchone()[0]
    finally:
        conn.close()


def write_flat_csv(rows, out_path: Path | str) -> Path:
    """Writes `rows` (FlatLabelRow-shaped) to out_path in BarTender's flat
    format. The one place that format is written, so record-generation,
    reprint-export, and pallet CSVs can never drift apart. CartonCount is
    blank for carton rows (only pallet rows carry one); LabelType is always
    CARTON or PALLET."""
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
                    getattr(r, "carton_count", None) or "",
                    getattr(r, "label_type", LABEL_TYPE_CARTON),
                ]
            )
    return out_path


def create_reprint_rows(label_ids: list[int], db_path: Path | str) -> list[FlatLabelRow]:
    """
    For each given labels.id, appends a NEW 'reprint' row copying that
    label's job_number/sscc/carton_sequence/label_copy_index/quantity,
    label_type/carton_count, and production_date/packing_slip_number
    snapshot - the original row is never modified or deleted. Works
    unchanged for a pallet row (label_type='PALLET', carton_count copied
    through) - "reprint" means the same thing either way: the same SSCC,
    printed again. Returns the newly created rows, flattened via the same
    Jobs+Labels join used everywhere else, in the same order label_ids was
    given (so index 0 of the result is the reprint of label_ids[0], etc).
    """
    if not label_ids:
        raise ValueError("label_ids is empty - nothing to reprint")

    now = datetime.now(timezone.utc).isoformat()
    conn = _connect(db_path)
    try:
        new_ids = []
        for original_id in label_ids:
            cur = conn.execute(
                "SELECT job_number, sscc, carton_sequence, label_copy_index, quantity, "
                "label_type, pallet_sscc, carton_count, production_date, packing_slip_number "
                "FROM labels WHERE id = ?",
                (original_id,),
            )
            original = cur.fetchone()
            if original is None:
                raise ValueError(f"No labels row found for id {original_id!r} - nothing to reprint")
            (
                job_number, sscc, carton_sequence, label_copy_index, quantity,
                label_type, pallet_sscc, carton_count, production_date, packing_slip_number,
            ) = original

            cur = conn.execute(
                """
                INSERT INTO labels (
                    job_number, sscc, carton_sequence, label_copy_index,
                    quantity, status, superseded_id, created_at, label_type,
                    pallet_sscc, carton_count, production_date, packing_slip_number
                ) VALUES (?, ?, ?, ?, ?, 'reprint', ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_number, sscc, carton_sequence, label_copy_index, quantity, original_id, now,
                    label_type, pallet_sscc, carton_count, production_date, packing_slip_number,
                ),
            )
            new_ids.append(cur.lastrowid)
        conn.commit()

        placeholders = ",".join("?" * len(new_ids))
        cur = conn.execute(f"{_JOIN_SELECT} WHERE l.id IN ({placeholders})", new_ids)
        rows_by_id = {row[14]: _row_to_flat(row) for row in cur.fetchall()}  # column 14 is l.id
        return [rows_by_id[new_id] for new_id in new_ids]
    finally:
        conn.close()


# --- Pallets: cartons scanned onto a pallet row - see barbell_gui.py's
# Pallet screen and QUESTIONS.md #18. -----------------------------------

_CARTON_LOOKUP_SELECT = """
SELECT
    l.id, l.sscc, l.job_number, j.product_no, j.item_number, j.gtin, j.batch,
    l.quantity, l.production_date, l.packing_slip_number, l.status,
    l.pallet_sscc, l.label_type, j.test_mode, l.created_at
FROM labels l
JOIN jobs j ON j.job_number = l.job_number
"""


@dataclass
class CartonInfo:
    """One carton, as looked up by its scanned SSCC - the fields the Pallet
    screen needs to validate a scan. GTIN/batch come from the jobs join
    (stable per job_number+product_no - see the module docstring);
    production_date/packing_slip_number are the carton's OWN per-row
    snapshot, since those two can legitimately vary carton-to-carton even
    under the same job_number (a job re-run on a later date/packing slip)."""

    id: int
    sscc: str
    job_number: str
    product_no: str
    item_number: str
    gtin: str | None
    batch: str
    quantity: int
    production_date: str | None
    packing_slip_number: str | None
    status: str
    pallet_sscc: str | None
    label_type: str
    test_mode: bool
    created_at: str

    @property
    def extension_digit(self) -> str:
        """The plant that issued this SSCC - its first digit (see
        src.sscc.build_sscc). Not meaningful for a TEST-SSCC-##### placeholder."""
        return self.sscc[0]


def find_carton_by_sscc(sscc: str, db_path: Path | str) -> CartonInfo | None:
    """
    Looks up a scanned SSCC among CARTON rows (never PALLET rows - the
    Pallet screen checks label_type itself to give the "that's a pallet,
    not a carton" message). A carton with more than one row sharing this
    SSCC (multiple print copies, or a reprint) always agrees on
    job/status/pallet_sscc/etc, since they're written together and
    create_pallet()/void_pallet() update every matching row - so the
    earliest (lowest id) is as representative as any other. Returns None
    if the SSCC isn't in the table at all.
    """
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            f"{_CARTON_LOOKUP_SELECT} WHERE l.sscc = ? AND l.label_type = 'CARTON' "
            "ORDER BY l.id LIMIT 1",
            (sscc,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return CartonInfo(
            id=row[0], sscc=row[1], job_number=row[2], product_no=row[3], item_number=row[4],
            gtin=row[5], batch=row[6], quantity=row[7], production_date=row[8],
            packing_slip_number=row[9], status=row[10], pallet_sscc=row[11], label_type=row[12],
            test_mode=bool(row[13]), created_at=row[14],
        )
    finally:
        conn.close()


@dataclass
class AvailableCarton:
    """One carton that could still go onto a pallet - what the Pallet
    screen's "Select Carton SSCC" list shows for each row."""

    sscc: str
    job_number: str
    item_number: str
    description: str
    batch: str
    gtin: str | None
    quantity: int
    production_date: str | None


def list_available_cartons(
    db_path: Path | str,
    test_mode: bool,
    job_number: str | None = None,
    sscc_contains: str | None = None,
    batch: str | None = None,
    gtin: str | None = None,
    exclude_ssccs=(),
) -> list[AvailableCarton]:
    """
    Cartons not yet on any pallet and not voided, one entry per SSCC (print
    copies and reprints collapse), for picking by hand instead of scanning.
    Only cartons of the given test/production kind are listed, since the two
    can never share a pallet. batch/gtin narrow the list to what could join
    a pallet that already has cartons on it; exclude_ssccs hides cartons
    already picked on the screen but not yet saved to a pallet. Newest run
    first, cartons in sequence order within a run.
    """
    conn = _connect(db_path)
    try:
        clauses = [
            "l.label_type = 'CARTON'", "l.pallet_sscc IS NULL", "l.status != 'void'",
            "j.test_mode = ?",
        ]
        params: list = [int(test_mode)]
        if job_number:
            clauses.append("j.job_number = ?")
            params.append(job_number)
        if sscc_contains:
            escaped = (
                sscc_contains.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            )
            clauses.append("l.sscc LIKE ? ESCAPE '\\'")
            params.append(f"%{escaped}%")
        if batch:
            clauses.append("j.batch = ?")
            params.append(batch)
        if gtin:
            clauses.append("j.gtin = ?")
            params.append(gtin)
        exclude = list(exclude_ssccs)
        if exclude:
            clauses.append(f"l.sscc NOT IN ({','.join('?' * len(exclude))})")
            params.extend(exclude)

        cur = conn.execute(
            f"""
            SELECT l.sscc, j.job_number, j.item_number, j.item_description, j.batch, j.gtin,
                   l.quantity, COALESCE(l.production_date, j.production_date)
            FROM labels l JOIN jobs j ON j.job_number = l.job_number
            WHERE {' AND '.join(clauses)}
            GROUP BY l.sscc
            ORDER BY MIN(l.created_at) DESC, MIN(l.id) ASC
            """,
            params,
        )
        return [
            AvailableCarton(
                sscc=r[0], job_number=r[1], item_number=r[2], description=r[3], batch=r[4],
                gtin=r[5], quantity=r[6], production_date=r[7],
            )
            for r in cur.fetchall()
        ]
    finally:
        conn.close()


def count_pallets(db_path: Path | str) -> int:
    """Distinct pallet SSCCs logged so far (both print copies of the same
    pallet count once) - used to pick a never-repeated sequence number for
    build_test_sscc() when generating a pallet in test mode, since (unlike
    a carton run's package_index) a pallet is one single item per Generate
    action with nothing else to derive a sequence from."""
    conn = _connect(db_path)
    try:
        cur = conn.execute("SELECT COUNT(DISTINCT sscc) FROM labels WHERE label_type = 'PALLET'")
        return cur.fetchone()[0]
    finally:
        conn.close()


def create_pallet(
    *,
    carton_ssccs: list[str],
    job_number: str,
    quantity: int,
    production_date: str,
    packing_slip_number: str | None,
    pallet_sscc: str,
    carton_count: int,
    db_path: Path | str,
) -> list[FlatLabelRow]:
    """
    One transaction: inserts 2 identical PALLET rows (both print copies,
    same pallet_sscc - "identical" the same way two copies of one carton's
    label already are), then stamps pallet_sscc on every labels row sharing
    each of carton_ssccs (every print copy of every scanned carton, not
    just one row each). GTIN/batch/item_number are read from the jobs row
    for job_number - the caller (the Pallet screen) has already confirmed
    every scanned carton shares one job/batch/GTIN before calling this.
    carton_sequence is set to 1 - not meaningful for a pallet, just
    satisfying the NOT NULL constraint it shares with carton rows. Returns
    the 2 new pallet rows, flattened via the usual Jobs+Labels join.
    """
    if not carton_ssccs:
        raise ValueError("carton_ssccs is empty - nothing to build a pallet from")

    production_date = normalize_production_date(production_date)
    now = datetime.now(timezone.utc).isoformat()
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT product_no, item_number, gtin, batch FROM jobs WHERE job_number = ?",
            (job_number,),
        )
        job_row = cur.fetchone()
        if job_row is None:
            raise ValueError(f"No jobs row found for job_number {job_number!r}")

        new_ids = []
        for copy_index in (1, 2):
            cur = conn.execute(
                """
                INSERT INTO labels (
                    job_number, sscc, carton_sequence, label_copy_index, quantity,
                    status, superseded_id, created_at, label_type, pallet_sscc,
                    carton_count, production_date, packing_slip_number
                ) VALUES (?, ?, 1, ?, ?, 'original', NULL, ?, 'PALLET', NULL, ?, ?, ?)
                """,
                (job_number, pallet_sscc, copy_index, quantity, now, carton_count,
                 production_date, packing_slip_number),
            )
            new_ids.append(cur.lastrowid)

        placeholders = ",".join("?" * len(carton_ssccs))
        conn.execute(
            f"UPDATE labels SET pallet_sscc = ? WHERE sscc IN ({placeholders}) AND label_type = 'CARTON'",
            [pallet_sscc, *carton_ssccs],
        )
        conn.commit()

        id_placeholders = ",".join("?" * len(new_ids))
        cur = conn.execute(f"{_JOIN_SELECT} WHERE l.id IN ({id_placeholders}) ORDER BY l.id", new_ids)
        return [_row_to_flat(row) for row in cur.fetchall()]
    finally:
        conn.close()


@dataclass
class PalletReportCarton:
    """One carton on a pallet, as the Pallet Report prints it - the same
    fields the carton's own label carries, so the report's small contents
    barcode is built from exactly what the label's was."""

    sscc: str
    item_number: str
    description: str
    quantity: int
    batch: str
    gtin: str | None
    production_date: str


@dataclass
class PalletReport:
    pallet_sscc: str
    job_number: str
    packing_slip_number: str | None
    production_date: str | None
    test_mode: bool
    created_at: str
    cartons: list[PalletReportCarton]

    @property
    def total_quantity(self) -> int:
        return sum(c.quantity for c in self.cartons)


def fetch_pallet_report(pallet_sscc: str, db_path: Path | str) -> PalletReport:
    """
    Everything the Pallet Report needs for one pallet: the pallet's own row
    plus one entry per carton linked to it (cartons.pallet_sscc), in the
    order they were originally generated. A carton with several print copies
    or a reprint appears once, not once per copy. Raises ValueError if
    pallet_sscc isn't a pallet, or has been voided (a void frees every
    carton, so there'd be nothing left to list).
    """
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            """
            SELECT l.status, l.job_number, l.packing_slip_number,
                   COALESCE(l.production_date, j.production_date), j.test_mode, l.created_at
            FROM labels l JOIN jobs j ON j.job_number = l.job_number
            WHERE l.sscc = ? AND l.label_type = 'PALLET'
            ORDER BY l.id LIMIT 1
            """,
            (pallet_sscc,),
        )
        pallet = cur.fetchone()
        if pallet is None:
            raise ValueError(f"No pallet found with SSCC {pallet_sscc!r}")
        status, job_number, packing_slip_number, production_date, test_mode, created_at = pallet
        if status == STATUS_VOID:
            raise ValueError(f"Pallet {pallet_sscc} has been voided - it no longer holds any cartons")

        cur = conn.execute(
            """
            SELECT l.sscc, j.item_number, j.item_description, l.quantity, j.batch, j.gtin,
                   COALESCE(l.production_date, j.production_date)
            FROM labels l JOIN jobs j ON j.job_number = l.job_number
            WHERE l.pallet_sscc = ? AND l.label_type = 'CARTON'
            GROUP BY l.sscc
            ORDER BY MIN(l.id)
            """,
            (pallet_sscc,),
        )
        cartons = [
            PalletReportCarton(
                sscc=row[0], item_number=row[1], description=row[2], quantity=row[3],
                batch=row[4], gtin=row[5], production_date=row[6],
            )
            for row in cur.fetchall()
        ]
        return PalletReport(
            pallet_sscc=pallet_sscc, job_number=job_number,
            packing_slip_number=packing_slip_number, production_date=production_date,
            test_mode=bool(test_mode), created_at=created_at, cartons=cartons,
        )
    finally:
        conn.close()


def void_pallet(pallet_sscc: str, db_path: Path | str) -> int:
    """
    One transaction: marks every labels row for this pallet SSCC (both
    print copies) status='void' IN PLACE - unlike a reprint, a void has
    nothing to replace, so no new row is inserted - and clears pallet_sscc
    on every carton currently linked to it, freeing them to be scanned onto
    a rebuilt pallet. The voided SSCC itself is never reused (nothing here
    returns it to the counter). Returns how many carton rows were freed.
    Raises ValueError if pallet_sscc doesn't match any PALLET row.
    """
    conn = _connect(db_path)
    try:
        cur = conn.execute(
            "SELECT COUNT(*) FROM labels WHERE sscc = ? AND label_type = 'PALLET'",
            (pallet_sscc,),
        )
        if cur.fetchone()[0] == 0:
            raise ValueError(f"No pallet found with SSCC {pallet_sscc!r}")

        conn.execute(
            "UPDATE labels SET status = 'void' WHERE sscc = ? AND label_type = 'PALLET'",
            (pallet_sscc,),
        )
        cur = conn.execute(
            "UPDATE labels SET pallet_sscc = NULL WHERE pallet_sscc = ? AND label_type = 'CARTON'",
            (pallet_sscc,),
        )
        freed = cur.rowcount
        conn.commit()
        return freed
    finally:
        conn.close()


# --- Setup password (hash only - see src/setup_access.py) -------------------

SETUP_PASSWORD_NAME = "standard_setup_password"


def get_setup_password_hash(db_path: Path | str) -> str | None:
    """The stored hash of the changed standard setup password, or None if it
    has never been changed (or was reset) - then the default applies."""
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT password_hash FROM setup_credentials WHERE name = ?", (SETUP_PASSWORD_NAME,)
        ).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def set_setup_password_hash(password_hash: str, db_path: Path | str) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            "INSERT INTO setup_credentials (name, password_hash, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(name) DO UPDATE SET password_hash = excluded.password_hash, "
            "updated_at = excluded.updated_at",
            (SETUP_PASSWORD_NAME, password_hash, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()


def clear_setup_password_hash(db_path: Path | str) -> None:
    """Removes the changed password, so the default applies again."""
    conn = _connect(db_path)
    try:
        conn.execute("DELETE FROM setup_credentials WHERE name = ?", (SETUP_PASSWORD_NAME,))
        conn.commit()
    finally:
        conn.close()


# --- Job Report: every pallet and carton logged for one job -----------------


@dataclass
class JobReportCarton:
    sscc: str
    description: str
    production_date: str
    quantity: int
    batch: str
    pallet_sscc: str | None


@dataclass
class JobReportPallet:
    sscc: str
    gtin: str | None
    description: str
    production_date: str
    quantity: int  # total product on the pallet (AI 37)
    batch: str
    carton_count: int  # as recorded when the pallet was made
    cartons: list[JobReportCarton]


@dataclass
class JobReport:
    job_number: str
    packing_slip_number: str | None
    customer_name: str | None
    item_number: str
    description: str
    batch: str
    gtin: str | None
    test_mode: bool
    pallets: list[JobReportPallet]
    unassociated_cartons: list[JobReportCarton]

    @property
    def carton_total(self) -> int:
        return sum(len(p.cartons) for p in self.pallets) + len(self.unassociated_cartons)


def fetch_job_report(job_number: str, db_path: Path | str) -> JobReport | None:
    """
    Everything the Job Report prints for one job, read only from BarBell's own
    SQLite data (no Label Traxx / ODBC). job_number must match exactly (only
    leading/trailing spaces are ignored). Returns None if BarBell has no such
    job.

    Voided labels are left out: a pallet counts unless every one of its rows is
    void, a carton likewise. A carton on no (live) pallet is listed in
    unassociated_cartons. Print copies and reprints of one SSCC appear once.
    """
    job_number = job_number.strip()
    conn = _connect(db_path)
    try:
        job = conn.execute(
            "SELECT job_number, packing_slip_number, customer_name, item_number, item_description, "
            "batch, gtin, test_mode, production_date FROM jobs WHERE job_number = ?",
            (job_number,),
        ).fetchone()
        if job is None:
            return None
        (stored_job, slip, customer, item_number, item_description, batch, gtin, test_mode,
         job_production_date) = job

        def rows(label_type: str):
            return conn.execute(
                """
                SELECT sscc, quantity, COALESCE(production_date, ?), pallet_sscc, carton_count
                FROM labels
                WHERE job_number = ? AND label_type = ?
                GROUP BY sscc
                HAVING SUM(status != 'void') > 0
                ORDER BY MIN(id)
                """,
                (job_production_date, stored_job, label_type),
            ).fetchall()

        pallet_rows = rows(LABEL_TYPE_PALLET)
        live_pallets = {r[0] for r in pallet_rows}

        cartons_by_pallet: dict[str, list[JobReportCarton]] = {}
        unassociated: list[JobReportCarton] = []
        for sscc, quantity, production_date, pallet_sscc, _ in rows(LABEL_TYPE_CARTON):
            carton = JobReportCarton(
                sscc=sscc, description=item_description, production_date=production_date,
                quantity=quantity, batch=batch, pallet_sscc=pallet_sscc,
            )
            if pallet_sscc and pallet_sscc in live_pallets:
                cartons_by_pallet.setdefault(pallet_sscc, []).append(carton)
            else:
                unassociated.append(carton)

        pallets = [
            JobReportPallet(
                sscc=sscc, gtin=gtin, description=item_description, production_date=production_date,
                quantity=quantity, batch=batch,
                carton_count=carton_count if carton_count is not None else len(cartons_by_pallet.get(sscc, [])),
                cartons=cartons_by_pallet.get(sscc, []),
            )
            for sscc, quantity, production_date, _, carton_count in pallet_rows
        ]
        return JobReport(
            job_number=stored_job, packing_slip_number=slip, customer_name=customer,
            item_number=item_number, description=item_description, batch=batch, gtin=gtin,
            test_mode=bool(test_mode), pallets=pallets, unassociated_cartons=unassociated,
        )
    finally:
        conn.close()
