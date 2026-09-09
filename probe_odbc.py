"""
Phase 4 probe script for the Label Traxx (4D) database.

Goes through ReadOnlyConnection exclusively (src/db/readonly_connection.py) -
never calls pyodbc.connect directly. Produces:

  docs/label_traxx_schema.md  - full table/column inventory + what SQL
                                 dialect (LIMIT vs TOP, quoting, value typing)
                                 the server actually accepts
  docs/field_mapping.md       - column -> business-field mapping, backed by
                                 the real ground-truth rows below
  QUESTIONS.md                 - open questions for the user to confirm
                                 (batch format, ambiguous date column, etc.)

Confirmed field mapping (see docs/field_mapping.md for full reasoning):
  job number             -> Ticket.Number
  item number (internal) -> Product.ProdNum   (Label Traxx's own key, e.g. '47388')
  item number (customer) -> Product.Name4     (e.g. '233458' - what the label prints)
  item description       -> Product.Description
  customer                -> Ticket.CustomerNum / Ticket.CustomerName
  quantity ordered        -> TicketItem.OrderQuantity
  production date (decided, for now) -> Ticket.PressStat (text date, e.g. '3/23/2026')
  batch number            -> job number + item number, no separator (src/batch.py)

All ID-like columns are CLOB (text) even when the values look numeric - every
query below quotes values as strings. No double-quoted identifiers are
needed anywhere in Ticket/Product/TicketItem/CustomerProduct.

Run with:
    python probe_odbc.py [job_number] [customer_item_number]

Defaults to the sample-label ground truth: job 122984, item 233458.
"""

import sys
from pathlib import Path

from src.db.readonly_connection import ReadOnlyConnection

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)

SCHEMA_MD = DOCS_DIR / "label_traxx_schema.md"

DEFAULT_JOB_NUMBER = "122984"
DEFAULT_ITEM_NUMBER = "233458"  # Product.Name4, not Product.ProdNum


def log(msg):
    print(msg)


# --------------------------------------------------------------------------
# Step 1 & 2: enumerate all accessible tables and columns
# --------------------------------------------------------------------------

def enumerate_schema(conn):
    log("Enumerating tables via SQLTables ...")
    tables = conn.list_tables()
    table_names = [t.table_name for t in tables if t.table_type in ("TABLE", "VIEW")]
    log(f"Found {len(table_names)} tables/views.")

    schema = {}
    unreachable = []

    for name in table_names:
        try:
            schema[name] = conn.list_columns(table=name)
        except Exception as exc:  # noqa: BLE001 - record any driver error, keep going
            unreachable.append((name, str(exc)))

    return tables, schema, unreachable


def write_schema_doc(tables, schema, unreachable):
    lines = ["# Label Traxx (LT64) Schema Inventory", ""]
    lines.append(f"Total tables/views reported by SQLTables: {len(tables)}")
    lines.append(f"Columns successfully enumerated for: {len(schema)} table(s)")
    lines.append(f"Not reachable (SQLColumns failed): {len(unreachable)} table(s)")
    lines.append("")

    lines.append("## Server SQL dialect notes")
    lines.append("")
    lines.append("- **Row limiting: `LIMIT` is accepted** (`SELECT * FROM Ticket LIMIT 1`); "
                  "`TOP` was never needed.")
    lines.append("- **Every ID-like column is CLOB (text)**, even where values look numeric "
                  "(e.g. `'122984'`). A bare numeric literal in a WHERE clause fails "
                  "(`08004 ... Failed to execute statement (1108)`) - always quote values "
                  "as strings.")
    lines.append("- **No double-quoted identifiers were needed** - every table/column name "
                  "encountered is a plain CamelCase token, no spaces or reserved words.")
    lines.append("- Complex joins/subqueries were avoided as expected for the 4D SQL subset - "
                  "`Ticket`, `Product`, `TicketItem` were queried separately and joined in "
                  "Python.")
    lines.append("")

    if unreachable:
        lines.append("## Tables NOT reachable via SQLColumns")
        lines.append("")
        lines.append("| table_name | error |")
        lines.append("|---|---|")
        for name, err in unreachable:
            lines.append(f"| {name} | {err} |")
        lines.append("")

    lines.append("## All tables reported by SQLTables")
    lines.append("")
    lines.append("| table_cat | table_schem | table_name | table_type |")
    lines.append("|---|---|---|---|")
    for t in tables:
        lines.append(f"| {t.table_cat} | {t.table_schem} | {t.table_name} | {t.table_type} |")
    lines.append("")

    lines.append("## Columns per reachable table")
    lines.append("")
    for name in sorted(schema.keys()):
        cols = schema[name]
        lines.append(f"### {name}")
        lines.append("")
        lines.append("| column_name | type_name | column_size | nullable |")
        lines.append("|---|---|---|---|")
        for c in cols:
            lines.append(
                f"| {c.column_name} | {c.type_name} | {c.column_size} | {c.nullable} |"
            )
        lines.append("")

    SCHEMA_MD.write_text("\n".join(lines), encoding="utf-8")
    log(f"Wrote {SCHEMA_MD}")


# --------------------------------------------------------------------------
# Step 3: ground-truth rows, using the confirmed real column names
# --------------------------------------------------------------------------

def fetch_ticket(conn, job_number):
    cur = conn.execute(f"SELECT * FROM Ticket WHERE Number = '{job_number}' LIMIT 1")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, rows[0])) if rows else {}


def fetch_ticket_item(conn, job_number):
    cur = conn.execute(f"SELECT * FROM TicketItem WHERE TicketNumber = '{job_number}' LIMIT 1")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, rows[0])) if rows else {}


def fetch_product_by_internal_num(conn, prod_num):
    cur = conn.execute(f"SELECT * FROM Product WHERE ProdNum = '{prod_num}' LIMIT 1")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, rows[0])) if rows else {}


def fetch_product_by_customer_item_num(conn, item_number):
    """Product.Name4 holds the customer-facing item number (e.g. 233458)."""
    cur = conn.execute(f"SELECT * FROM Product WHERE Name4 = '{item_number}' LIMIT 1")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, rows[0])) if rows else {}


def print_row(label, row):
    log(f"\n--- {label} ---")
    if not row:
        log("  no rows found")
        return
    for k, v in row.items():
        log(f"  {k} = {v!r}")


def main():
    job_number = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JOB_NUMBER
    item_number = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_ITEM_NUMBER

    with ReadOnlyConnection() as conn:
        tables, schema, unreachable = enumerate_schema(conn)
        write_schema_doc(tables, schema, unreachable)

        ticket = fetch_ticket(conn, job_number)
        ticket_item = fetch_ticket_item(conn, job_number)
        product = fetch_product_by_customer_item_num(conn, item_number)

        print_row(f"Ticket (job {job_number})", ticket)
        print_row(f"TicketItem (job {job_number})", ticket_item)
        print_row(f"Product (customer item number {item_number}, via Name4)", product)

        if not product and ticket_item.get("ProductNumber"):
            # Fall back: look the product up by its internal ProdNum from the
            # ticket line, in case Name4 doesn't hold this item's number.
            internal_num = ticket_item["ProductNumber"]
            product = fetch_product_by_internal_num(conn, internal_num)
            print_row(f"Product (internal ProdNum {internal_num}, fallback)", product)

        log("\nSee docs/field_mapping.md for the confirmed mapping and "
            "QUESTIONS.md for open questions (batch format, production date).")


if __name__ == "__main__":
    sys.exit(main())
