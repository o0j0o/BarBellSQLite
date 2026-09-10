"""
Assembles GS1-128 logistics label rows for one job + packing slip + product line.

Flow (see QUESTIONS.md and docs/gs1_label_requirements.md for the full picture):
  1. User picks a job number -> Ticket.Number
  2. User picks a packing slip for that job, from PackingSlip.TicketNum = job number
  3. A packing slip can carry multiple products - user picks ONE PackSlipItem line
     (ProductNo + description) to generate labels for
  4. User provides units-per-package and labels-per-package (manual - Label Traxx
     doesn't record how a shipment is broken into physical packages)
  5. User provides the production date to print on the label (manual - deliberately
     not sourced from Label Traxx; see QUESTIONS.md #3)
  6. This module joins Ticket + the selected PackSlipItem + Product, computes one
     package quantity per physical package, generates one SSCC per package, and
     returns one row per (package, label copy) ready to write to CSV.

Batch = job number + ProductNo (Product.ProdNum, the internal Label Traxx number the
user calls "P/N") - NOT the item number (Product.Name4). Both are carried on every
row; only ProductNo feeds the batch. See QUESTIONS.md #2/#9.

GTIN (AI 02) is sourced from Product.BC_Start ("Barcode Start"), validated by
src.gtin.normalize_gtin(). It's free text in Label Traxx, so a missing or invalid
value blocks label generation with a specific error rather than silently proceeding
or falling back to manual entry - see get_product_info() and QUESTIONS.md #4/#12.
"""

from dataclasses import dataclass

from src.batch import build_batch_number
from src.gtin import InvalidGTINError, normalize_gtin
from src.sscc import SSCCGenerator, build_test_sscc


@dataclass
class PackingSlipSummary:
    number: str
    suffix: int
    ship_date: object
    customer_name: str
    ship_quantity: int
    no_package: int


def list_packing_slips_for_job(conn, job_number: str) -> list[PackingSlipSummary]:
    """Packing slips for this job, each with its total ShipQuantity, for a selection list."""
    cur = conn.execute(f"SELECT * FROM PackingSlip WHERE TicketNum = '{job_number}' LIMIT 50")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    summaries = []
    for row in rows:
        slip = dict(zip(cols, row))
        summaries.append(
            PackingSlipSummary(
                number=slip["Number"],
                suffix=slip["Suffix"],
                ship_date=slip["ShipDate"],
                customer_name=slip["CustomerName"],
                ship_quantity=_total_ship_quantity(conn, slip["Number"]),
                no_package=slip["NoPackage"],
            )
        )
    return summaries


def _total_ship_quantity(conn, packing_slip_number: str) -> int:
    cur = conn.execute(
        f"SELECT ShipQuantity FROM PackSlipItem WHERE PackSlipNumber = '{packing_slip_number}' LIMIT 50"
    )
    rows = cur.fetchall()
    return sum(r[0] for r in rows)


@dataclass
class PackingSlipLineItem:
    packing_slip_number: str
    product_number: str  # Product.ProdNum (Label Traxx internal) - the "P/N"
    description: str  # PackSlipItem.ProdDescr - shown alongside ProductNo in the picker
    ship_quantity: int
    ticket_item_id: str


def list_packing_slip_line_items(conn, packing_slip_number: str) -> list[PackingSlipLineItem]:
    """
    All PackSlipItem lines for this packing slip - a packing slip can carry
    multiple products, so the caller must show these (ProductNo + description)
    and let the user pick ONE to generate labels for.
    """
    cur = conn.execute(
        f"SELECT * FROM PackSlipItem WHERE PackSlipNumber = '{packing_slip_number}' LIMIT 50"
    )
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    items = [dict(zip(cols, row)) for row in rows]

    if not items:
        raise ValueError(f"Packing slip {packing_slip_number!r} has no line items")

    return [
        PackingSlipLineItem(
            packing_slip_number=item["PackSlipNumber"],
            product_number=item["ProductNumber"],
            description=item["ProdDescr"],
            ship_quantity=item["ShipQuantity"],
            ticket_item_id=item["TicketItemID"],
        )
        for item in items
    ]


@dataclass
class ProductInfo:
    prod_num: str  # internal Label Traxx number - the "P/N" / ProductNo (feeds the batch)
    item_number: str  # Product.Name4 - what's on the label (see docs/field_mapping.md)
    description: str
    gtin: str | None = None  # validated, normalized 14-digit GTIN - None if missing/invalid
    gtin_raw: str | None = None  # exact Product.BC_Start value as found, for diagnostics
    gtin_error: str | None = None  # human-readable reason gtin is None, if BC_Start was populated but bad


def get_product_info(conn, prod_num: str) -> ProductInfo:
    """
    GTIN (AI 02) is sourced from Product.BC_Start ("Barcode Start" in Label
    Traxx's own UI) - free text, so it's validated here via
    src.gtin.normalize_gtin(). An empty or invalid value does NOT raise -
    gtin stays None and gtin_error explains why, so the caller can block
    label generation with a clear, specific message (see QUESTIONS.md #4
    and #12) rather than the lookup itself failing.
    """
    cur = conn.execute(f"SELECT * FROM Product WHERE ProdNum = '{prod_num}' LIMIT 1")
    rows = cur.fetchall()
    if not rows:
        raise ValueError(f"No Product found for ProdNum {prod_num!r}")
    cols = [d[0] for d in cur.description]
    product = dict(zip(cols, rows[0]))

    raw_gtin = product["BC_Start"]
    gtin = None
    gtin_error = None
    try:
        gtin = normalize_gtin(raw_gtin)
    except InvalidGTINError as exc:
        gtin_error = str(exc)

    return ProductInfo(
        prod_num=product["ProdNum"],
        item_number=product["Name4"],
        description=product["Description"],
        gtin=gtin,
        gtin_raw=raw_gtin,
        gtin_error=gtin_error,
    )


@dataclass
class TicketInfo:
    job_number: str
    customer_number: str
    customer_name: str


def get_ticket_info(conn, job_number: str) -> TicketInfo:
    cur = conn.execute(f"SELECT * FROM Ticket WHERE Number = '{job_number}' LIMIT 1")
    rows = cur.fetchall()
    if not rows:
        raise ValueError(f"No Ticket found for job number {job_number!r}")
    cols = [d[0] for d in cur.description]
    ticket = dict(zip(cols, rows[0]))
    return TicketInfo(
        job_number=ticket["Number"],
        customer_number=ticket["CustomerNum"],
        customer_name=ticket["CustomerName"],
    )


def compute_package_quantities(total_quantity: int, units_per_package: int) -> list[int]:
    """
    Split a total quantity into fixed-size packages, with a smaller final
    package for any remainder - e.g. 547000 units at 27000/package ->
    20 packages of 27000 plus a final package of 7000 (21 total). This
    matches Label Traxx's own PackingSlip.NoPackage for job 122984's real
    packing slip (100495), which really did ship as 20 boxes of 27000 plus
    one box of 7000.
    """
    if total_quantity <= 0:
        raise ValueError(f"total_quantity must be positive, got {total_quantity}")
    if units_per_package <= 0:
        raise ValueError(f"units_per_package must be positive, got {units_per_package}")

    full_packages, remainder = divmod(total_quantity, units_per_package)
    quantities = [units_per_package] * full_packages
    if remainder:
        quantities.append(remainder)
    return quantities


@dataclass
class LabelRow:
    job_number: str
    packing_slip_number: str
    customer_number: str
    customer_name: str
    product_no: str  # Product.ProdNum / "P/N" - feeds the batch, see build_batch_number below
    item_number: str
    item_description: str
    quantity: int
    batch: str
    production_date: str
    sscc: str
    gtin: str | None
    package_index: int  # 1-based, which physical package this label is for
    label_copy_index: int  # 1-based, which copy of this package's label this is


def assemble_label_rows(
    conn,
    sscc_generator: SSCCGenerator | None,
    job_number: str,
    line_item: PackingSlipLineItem,
    units_per_package: int,
    labels_per_package: int,
    production_date: str,
    test_mode: bool = False,
) -> list[LabelRow]:
    """
    line_item is the ONE PackSlipItem line the user picked from
    list_packing_slip_line_items() - a packing slip can carry multiple
    products, so the caller selects which one before calling this.

    test_mode=True skips the real SSCC counter entirely - every SSCC comes
    from build_test_sscc() instead, so sscc_generator can be None and
    sscc_state.json is never touched. Use this to try out the whole flow
    without consuming (or needing to "recover") any real SSCCs.

    Raises InvalidGTINError if the product's GTIN (Product.BC_Start) is
    missing or invalid - callers should check product.gtin_error themselves
    first (via get_product_info) to give a better-timed warning, but this is
    enforced here too so a bad GTIN can never slip through regardless of the
    caller - see QUESTIONS.md #12.
    """
    if not test_mode and sscc_generator is None:
        raise ValueError("sscc_generator is required unless test_mode=True")

    ticket = get_ticket_info(conn, job_number)
    product = get_product_info(conn, line_item.product_number)
    if product.gtin is None:
        raise InvalidGTINError(
            f"Item {product.item_number} (P/N {product.prod_num}): "
            f"{product.gtin_error or 'GTIN is missing'}. "
            "Fix Product.BC_Start (\"Barcode Start\") in Label Traxx before generating labels."
        )

    # Batch = job number + ProductNo (Product.ProdNum, the "P/N") - NOT item_number.
    batch = build_batch_number(ticket.job_number, product.prod_num)
    package_quantities = compute_package_quantities(line_item.ship_quantity, units_per_package)

    rows = []
    for package_index, package_qty in enumerate(package_quantities, start=1):
        sscc = build_test_sscc(package_index) if test_mode else sscc_generator.next_sscc()
        for copy_index in range(1, labels_per_package + 1):
            rows.append(
                LabelRow(
                    job_number=ticket.job_number,
                    packing_slip_number=line_item.packing_slip_number,
                    customer_number=ticket.customer_number,
                    customer_name=ticket.customer_name,
                    product_no=product.prod_num,
                    item_number=product.item_number,
                    item_description=product.description,
                    quantity=package_qty,
                    batch=batch,
                    production_date=production_date,
                    sscc=sscc,
                    gtin=product.gtin,
                    package_index=package_index,
                    label_copy_index=copy_index,
                )
            )
    return rows
