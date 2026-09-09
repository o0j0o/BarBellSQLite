import pytest

from src.labels import (
    PackingSlipLineItem,
    assemble_label_rows,
    compute_package_quantities,
    get_product_info,
    get_ticket_info,
    list_packing_slip_line_items,
)
from src.sscc import SSCCGenerator

CLC_PREFIX = "08600157112"


# --- compute_package_quantities: pure logic, no DB involved ---------------

def test_compute_package_quantities_matches_real_job_122984_shipment():
    """
    Job 122984 / packing slip 100495 really did ship as 20 boxes of 27000
    plus one box of 7000 (per the packing slip's own Notes field), totaling
    547000 - and Label Traxx's own PackingSlip.NoPackage for that slip is 21.
    This is a real ground-truth example, not a made-up one.
    """
    quantities = compute_package_quantities(547000, 27000)
    assert len(quantities) == 21
    assert quantities[:20] == [27000] * 20
    assert quantities[20] == 7000
    assert sum(quantities) == 547000


def test_compute_package_quantities_exact_division_has_no_partial_package():
    quantities = compute_package_quantities(90000, 9000)
    assert quantities == [9000] * 10


def test_compute_package_quantities_rejects_non_positive_inputs():
    with pytest.raises(ValueError):
        compute_package_quantities(0, 100)
    with pytest.raises(ValueError):
        compute_package_quantities(100, 0)
    with pytest.raises(ValueError):
        compute_package_quantities(-5, 100)


# --- DB-facing helpers, using a fake connection (same shape as ReadOnlyConnection) ---

class FakeCursor:
    def __init__(self, cols, rows):
        self.description = [(c,) for c in cols]
        self._rows = rows

    def fetchall(self):
        return self._rows


class FakeConn:
    """Returns canned rows keyed by which table the SQL mentions - good enough
    for these simple single-table SELECTs, no real SQL parsing needed."""

    def __init__(self, tables: dict):
        self.tables = tables  # {table_name: (cols, rows)}
        self.queries = []

    def execute(self, sql):
        self.queries.append(sql)
        for table, (cols, rows) in self.tables.items():
            if table in sql:
                return FakeCursor(cols, rows)
        raise AssertionError(f"No fake data registered for query: {sql}")


def make_fake_conn(pack_slip_items=None):
    return FakeConn(
        {
            "Ticket": (
                ["Number", "CustomerNum", "CustomerName"],
                [("122984", "J00005", "J. Wray & Nephew Ltd.")],
            ),
            "PackSlipItem": (
                ["PackSlipNumber", "ProductNumber", "ProdDescr", "TicketItemID", "ShipQuantity"],
                pack_slip_items
                or [("100495", "47388", "233458 - JWN White O/P Rum B 750Ml USA - PS", "213223", 547000)],
            ),
            "Product": (
                ["ProdNum", "Name4", "Description"],
                [("47388", "233458", "233458 - JWN White O/P Rum B 750Ml USA - PS")],
            ),
        }
    )


def make_line_item(**overrides):
    defaults = dict(
        packing_slip_number="100495",
        product_number="47388",
        description="233458 - JWN White O/P Rum B 750Ml USA - PS",
        ship_quantity=547000,
        ticket_item_id="213223",
    )
    return PackingSlipLineItem(**{**defaults, **overrides})


def test_get_ticket_info_reads_the_right_columns():
    ticket = get_ticket_info(make_fake_conn(), "122984")
    assert ticket.job_number == "122984"
    assert ticket.customer_number == "J00005"
    assert ticket.customer_name == "J. Wray & Nephew Ltd."


def test_list_packing_slip_line_items_returns_one_item_for_a_single_product_slip():
    items = list_packing_slip_line_items(make_fake_conn(), "100495")
    assert len(items) == 1
    assert items[0].product_number == "47388"
    assert items[0].description == "233458 - JWN White O/P Rum B 750Ml USA - PS"
    assert items[0].ship_quantity == 547000


def test_list_packing_slip_line_items_returns_all_products_on_a_multi_product_slip():
    """A packing slip can carry multiple products - all lines must come back,
    not just the first, so the caller can offer a selection list."""
    conn = make_fake_conn(
        pack_slip_items=[
            ("100495", "47388", "233458 - Product A", "213223", 300000),
            ("100495", "99999", "999999 - Product B", "213224", 247000),
        ]
    )
    items = list_packing_slip_line_items(conn, "100495")
    assert len(items) == 2
    assert {i.product_number for i in items} == {"47388", "99999"}
    assert {i.description for i in items} == {"233458 - Product A", "999999 - Product B"}


def test_list_packing_slip_line_items_raises_if_none_found():
    conn = FakeConn({"PackSlipItem": (["PackSlipNumber", "ProductNumber", "ProdDescr", "TicketItemID", "ShipQuantity"], [])})
    with pytest.raises(ValueError, match="no line items"):
        list_packing_slip_line_items(conn, "100495")


def test_get_product_info_uses_name4_as_item_number_and_prodnum_as_product_no():
    product = get_product_info(make_fake_conn(), "47388")
    assert product.prod_num == "47388"  # ProductNo / "P/N" - feeds the batch
    assert product.item_number == "233458"  # distinct field, does NOT feed the batch
    assert product.description == "233458 - JWN White O/P Rum B 750Ml USA - PS"
    assert product.gtin is None  # not sourceable yet - see QUESTIONS.md #4


# --- assemble_label_rows: the full join + SSCC issuance ---------------------

def test_assemble_label_rows_end_to_end(tmp_path):
    state_file = tmp_path / "sscc_state.json"
    gen = SSCCGenerator(CLC_PREFIX, "0", state_file)
    gen.initialize(start_at=10)

    rows = assemble_label_rows(
        conn=make_fake_conn(),
        sscc_generator=gen,
        job_number="122984",
        line_item=make_line_item(),
        units_per_package=27000,
        labels_per_package=2,
        production_date="2026-03-23",
    )

    # 21 packages (20x27000 + 1x7000) x 2 label copies each = 42 rows
    assert len(rows) == 42

    first = rows[0]
    assert first.job_number == "122984"
    assert first.product_no == "47388"  # ProdNum, NOT the item number
    assert first.item_number == "233458"
    assert first.batch == "12298447388"  # job number + ProductNo (ProdNum), not item_number
    assert first.quantity == 27000
    assert first.package_index == 1
    assert first.label_copy_index == 1
    assert first.production_date == "2026-03-23"
    assert first.gtin is None

    # both copies of package 1 share the same SSCC ...
    second = rows[1]
    assert second.package_index == 1
    assert second.label_copy_index == 2
    assert second.sscc == first.sscc

    # ... but package 2's copies get a different SSCC than package 1's
    third = rows[2]
    assert third.package_index == 2
    assert third.sscc != first.sscc

    # the final (21st) package is the smaller remainder
    last_package_rows = [r for r in rows if r.package_index == 21]
    assert len(last_package_rows) == 2
    assert all(r.quantity == 7000 for r in last_package_rows)

    # SSCCs issued: 21 packages worth, all unique, starting at serial 10
    sccs_in_order = [r.sscc for r in rows if r.label_copy_index == 1]
    assert len(set(sccs_in_order)) == 21


def test_assemble_label_rows_test_mode_never_touches_the_real_counter(tmp_path):
    """
    Test mode must work with NO SSCCGenerator at all (sscc_generator=None) and
    must never create or write a state file - there's nothing to "waste" or
    later "recover" using this path.
    """
    state_file = tmp_path / "sscc_state.json"  # deliberately never initialized

    rows = assemble_label_rows(
        conn=make_fake_conn(),
        sscc_generator=None,
        job_number="122984",
        line_item=make_line_item(),
        units_per_package=27000,
        labels_per_package=2,
        production_date="2026-03-23",
        test_mode=True,
    )

    assert len(rows) == 42  # same 21 packages x 2 copies as the real-mode test
    assert not state_file.exists()  # never created, let alone written to

    test_sccs = {r.sscc for r in rows}
    assert len(test_sccs) == 21  # one per package, all unique
    assert all(s.startswith("TEST-SSCC-") for s in test_sccs)


def test_assemble_label_rows_requires_a_generator_unless_test_mode():
    with pytest.raises(ValueError, match="test_mode"):
        assemble_label_rows(
            conn=make_fake_conn(),
            sscc_generator=None,
            job_number="122984",
            line_item=make_line_item(),
            units_per_package=27000,
            labels_per_package=1,
            production_date="2026-03-23",
        )
