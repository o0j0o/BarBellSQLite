"""
Self-contained fake Label Traxx data for BarBell's Demo Mode (Settings.demo_mode) -
lets the whole job -> packing slip -> product -> GTIN -> package -> CSV flow run
with zero ODBC/network calls, for demoing BarBell somewhere with no access to
Label Traxx.

DemoConnection is a drop-in stand-in for src.db.readonly_connection.ReadOnlyConnection:
same execute(sql) -> cursor-with-.description-and-.fetchall() shape, so nothing in
src/labels.py needs to know or care which one it's talking to. It answers the simple
single-table `SELECT <cols> FROM <table> [WHERE <col> = '<value>']` queries
src/labels.py issues against the canned tables below, by parsing just enough of the
SQL text to route and filter - never a real socket or ODBC handle.

Every demo identifier is obviously fake (DEMO- prefixed job/packing slip/product
numbers, a fictional customer) so a demo run can never be mistaken for real Label
Traxx data. One product (DEMO-P300) deliberately has no GTIN on file, so demo mode
can also show the "No GTIN on file" / manual-entry flow, not just the happy path.
"""

import re

from src.sscc import gs1_check_digit


def _demo_bc_start(body11: str) -> str:
    """11-digit body -> a validly-checksummed 12-digit UPC-A-shaped code, grouped
    with spaces the way real Product.BC_Start values are (see VALID_BC_START in
    tests/test_labels.py for the real-world shape this mimics) - normalize_gtin()
    zero-pads the result to a full 14-digit GTIN."""
    if len(body11) != 11 or not body11.isdigit():
        raise ValueError(f"body11 must be exactly 11 digits, got {body11!r}")
    digits = body11 + gs1_check_digit(body11)
    return f"{digits[0]} {digits[1:6]} {digits[6:11]} {digits[11]}"


DEMO_CUSTOMER_NUMBER = "DEMO-C01"
DEMO_CUSTOMER_NAME = "Acme Caribbean Beverages Ltd. (DEMO)"
DEMO_CUSTOMER_2_NUMBER = "DEMO-C02"
DEMO_CUSTOMER_2_NAME = "Coastal Spirits Distributors (DEMO)"

_TICKET_COLS = ["Number", "CustomerNum", "CustomerName"]
_TICKET_ROWS = [
    ("DEMO-1001", DEMO_CUSTOMER_NUMBER, DEMO_CUSTOMER_NAME),
    ("DEMO-1002", DEMO_CUSTOMER_2_NUMBER, DEMO_CUSTOMER_2_NAME),
    ("DEMO-1003", DEMO_CUSTOMER_NUMBER, DEMO_CUSTOMER_NAME),
]

_PACKING_SLIP_COLS = ["Number", "Suffix", "ShipDate", "CustomerName", "NoPackage", "TicketNum"]
_PACKING_SLIP_ROWS = [
    ("DEMO-PS-5001", 1, "2026-09-01", DEMO_CUSTOMER_NAME, 2, "DEMO-1001"),
    ("DEMO-PS-5002", 1, "2026-09-05", DEMO_CUSTOMER_2_NAME, 3, "DEMO-1002"),
    ("DEMO-PS-5003", 1, "2026-09-10", DEMO_CUSTOMER_NAME, 1, "DEMO-1003"),
]

# A packing slip can carry multiple products (DEMO-PS-5002 does, below) - real
# BarBell behaviour, so the demo shows the product picker too, not just a
# single-product happy path.
_PACK_SLIP_ITEM_COLS = ["PackSlipNumber", "ProductNumber", "ProdDescr", "TicketItemID", "ShipQuantity"]
_PACK_SLIP_ITEM_ROWS = [
    ("DEMO-PS-5001", "DEMO-P100", "DEMO White Overproof Rum 750ml", "DEMO-TI-01", 54000),
    ("DEMO-PS-5002", "DEMO-P200", "DEMO Spiced Rum 1L", "DEMO-TI-02", 36000),
    ("DEMO-PS-5002", "DEMO-P201", "DEMO Coconut Rum Cream 750ml", "DEMO-TI-03", 24000),
    ("DEMO-PS-5003", "DEMO-P300", "DEMO Dark Rum 1.75L", "DEMO-TI-04", 9000),
]

_PRODUCT_COLS = ["ProdNum", "Name4", "Description", "BC_Start"]
_PRODUCT_ROWS = [
    ("DEMO-P100", "D-100", "DEMO White Overproof Rum 750ml", _demo_bc_start("09999900001")),
    ("DEMO-P200", "D-200", "DEMO Spiced Rum 1L", _demo_bc_start("09999900002")),
    ("DEMO-P201", "D-201", "DEMO Coconut Rum Cream 750ml", _demo_bc_start("09999900003")),
    # Deliberately empty - demonstrates the "No GTIN on file"/manual-entry flow.
    ("DEMO-P300", "D-300", "DEMO Dark Rum 1.75L", ""),
]

DEMO_TABLES = {
    "Ticket": (_TICKET_COLS, _TICKET_ROWS),
    "PackingSlip": (_PACKING_SLIP_COLS, _PACKING_SLIP_ROWS),
    "PackSlipItem": (_PACK_SLIP_ITEM_COLS, _PACK_SLIP_ITEM_ROWS),
    "Product": (_PRODUCT_COLS, _PRODUCT_ROWS),
}

DEMO_JOB_NUMBERS = [row[0] for row in _TICKET_ROWS]

_SELECT_RE = re.compile(r"SELECT\s+(.*?)\s+FROM\s+(\w+)", re.IGNORECASE | re.DOTALL)
_WHERE_RE = re.compile(r"WHERE\s+(\w+)\s*=\s*'([^']*)'", re.IGNORECASE)


class _DemoCursor:
    def __init__(self, cols, rows):
        self.description = [(c,) for c in cols]
        self._rows = rows

    def fetchall(self):
        return self._rows


class DemoConnection:
    """Drop-in stand-in for ReadOnlyConnection when Settings.demo_mode is True.
    Never opens a socket or ODBC handle - every query is answered from
    DEMO_TABLES above."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql: str, params=None):
        select_match = _SELECT_RE.search(sql)
        if not select_match:
            raise ValueError(f"DemoConnection can't parse this query: {sql!r}")
        select_clause, table = select_match.group(1).strip(), select_match.group(2)
        if table not in DEMO_TABLES:
            raise ValueError(f"DemoConnection has no demo data for table {table!r}: {sql!r}")
        all_cols, rows = DEMO_TABLES[table]

        where_match = _WHERE_RE.search(sql)
        if where_match:
            column, value = where_match.group(1), where_match.group(2)
            col_index = all_cols.index(column)
            rows = [r for r in rows if r[col_index] == value]

        if select_clause == "*":
            return _DemoCursor(all_cols, rows)

        wanted_cols = [c.strip() for c in select_clause.split(",")]
        indices = [all_cols.index(c) for c in wanted_cols]
        narrowed_rows = [tuple(r[i] for i in indices) for r in rows]
        return _DemoCursor(wanted_cols, narrowed_rows)
