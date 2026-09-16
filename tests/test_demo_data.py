import pytest

from src.demo_data import DEMO_JOB_NUMBERS, DemoConnection
from src.gtin import InvalidGTINError
from src.labels import (
    assemble_label_rows,
    get_product_info,
    get_ticket_info,
    list_packing_slip_line_items,
    list_packing_slips_for_job,
)


def test_demo_job_numbers_are_obviously_fake():
    assert len(DEMO_JOB_NUMBERS) >= 3
    assert all(job.startswith("DEMO-") for job in DEMO_JOB_NUMBERS)


def test_get_ticket_info_works_against_demo_connection():
    ticket = get_ticket_info(DemoConnection(), "DEMO-1001")
    assert ticket.job_number == "DEMO-1001"
    assert "DEMO" in ticket.customer_name


def test_get_ticket_info_raises_for_unknown_job():
    with pytest.raises(ValueError, match="NOPE"):
        get_ticket_info(DemoConnection(), "NOPE")


def test_list_packing_slips_for_job_computes_ship_quantity_correctly():
    """Regression guard: list_packing_slips_for_job() issues a
    'SELECT ShipQuantity FROM PackSlipItem WHERE ...' (a single narrowed
    column, not '*') and sums column 0 of what comes back - DemoConnection
    must actually narrow to just that column, not hand back full rows."""
    slips = list_packing_slips_for_job(DemoConnection(), "DEMO-1002")
    assert len(slips) == 1
    assert slips[0].ship_quantity == 36000 + 24000  # DEMO-PS-5002's two line items


def test_list_packing_slip_line_items_shows_multi_product_slip():
    """DEMO-PS-5002 deliberately carries two products - demo mode must show
    the same multi-product picker flow real packing slips can require."""
    items = list_packing_slip_line_items(DemoConnection(), "DEMO-PS-5002")
    assert len(items) == 2
    assert {i.product_number for i in items} == {"DEMO-P200", "DEMO-P201"}


def test_get_product_info_returns_valid_gtin_for_normal_demo_product():
    product = get_product_info(DemoConnection(), "DEMO-P100")
    assert product.gtin is not None
    assert product.gtin_error is None


def test_get_product_info_flags_missing_gtin_for_demo_product_without_one():
    """DEMO-P300 deliberately has no BC_Start, so demo mode can also show the
    'No GTIN on file' / manual-entry flow, not just the happy path."""
    product = get_product_info(DemoConnection(), "DEMO-P300")
    assert product.gtin is None
    assert "empty" in product.gtin_error.lower()


def test_demo_connection_raises_for_unknown_table():
    with pytest.raises(ValueError, match="no demo data"):
        DemoConnection().execute("SELECT * FROM NotARealTable WHERE X = 'Y'")


def test_assemble_label_rows_end_to_end_against_demo_connection():
    """The full real pipeline (src/labels.py, completely unmodified for Demo
    Mode) must work against DemoConnection exactly as it does against a real
    ReadOnlyConnection - this is the whole point of Demo Mode."""
    conn = DemoConnection()
    line_item = list_packing_slip_line_items(conn, "DEMO-PS-5001")[0]

    rows = assemble_label_rows(
        conn=conn,
        sscc_generator=None,
        job_number="DEMO-1001",
        line_item=line_item,
        units_per_package=27000,
        labels_per_package=1,
        production_date="2026-09-16",
        test_mode=True,
    )

    assert len(rows) == 2  # 54000 / 27000 = 2 packages, 1 copy each
    assert all(r.sscc.startswith("TEST-SSCC-") for r in rows)  # demo never issues a real SSCC
    assert rows[0].gtin is not None
    assert rows[0].job_number == "DEMO-1001"


def test_assemble_label_rows_blocks_on_demo_products_missing_gtin():
    """Demo Mode should demonstrate real validation behaviour too, not just
    the happy path - DEMO-P300 (no BC_Start) must still block."""
    conn = DemoConnection()
    line_item = list_packing_slip_line_items(conn, "DEMO-PS-5003")[0]

    with pytest.raises(InvalidGTINError):
        assemble_label_rows(
            conn=conn,
            sscc_generator=None,
            job_number="DEMO-1003",
            line_item=line_item,
            units_per_package=9000,
            labels_per_package=1,
            production_date="2026-09-16",
            test_mode=True,
        )
