import datetime

import numpy as np
import pytest
import zxingcpp

from src.db.local_store import (
    PalletReport,
    PalletReportCarton,
    create_pallet,
    fetch_pallet_report,
    record_generation_run,
    void_pallet,
)
from src.labels import LabelRow
from src.pallet_report import _paginate, build_pallet_report_pdf, render_pallet_report_pages

PALLET_SSCC = "008600157112099999"
GTIN = "00051096184921"


def carton_rows(ssccs, quantity=10000, copies=1):
    return [
        LabelRow(
            job_number="122984", packing_slip_number="100495", customer_number="J00005",
            customer_name="J. Wray & Nephew Ltd.", product_no="47388", item_number="233458",
            item_description="233458 - JWN White O/P Rum B 750Ml USA - PS", quantity=quantity,
            batch="12298447388", production_date="2026-03-23", sscc=sscc, gtin=GTIN,
            package_index=i, label_copy_index=copy,
        )
        for i, sscc in enumerate(ssccs, start=1)
        for copy in range(1, copies + 1)
    ]


def seed_pallet(db_path, ssccs=("008600157112000128", "008600157112000296"), copies=1):
    record_generation_run(
        carton_rows(ssccs, copies=copies),
        units_per_package=10000, labels_per_package=copies, test_mode=False, db_path=db_path,
    )
    create_pallet(
        carton_ssccs=list(ssccs), job_number="122984", quantity=10000 * len(ssccs),
        production_date="2026-03-23", packing_slip_number="100495",
        pallet_sscc=PALLET_SSCC, carton_count=len(ssccs), db_path=db_path,
    )
    return list(ssccs)


def make_report(carton_count, pallet_sscc=PALLET_SSCC, test_mode=False):
    cartons = [
        PalletReportCarton(
            sscc=f"00860015711200{i:04d}"[:18].ljust(18, "0"), item_number="233458",
            description="233458 - JWN White O/P Rum B 750Ml USA - PS", quantity=10000 + i,
            batch="12298447388", gtin=GTIN, production_date="2026-03-23",
        )
        for i in range(carton_count)
    ]
    return PalletReport(
        pallet_sscc=pallet_sscc, job_number="122984", packing_slip_number="100495",
        production_date="2026-03-23", test_mode=test_mode,
        created_at="2026-09-25T14:03:00+00:00", cartons=cartons,
    )


def decoded_texts(pages):
    texts = []
    for page in pages:
        for result in zxingcpp.read_barcodes(np.array(page.convert("L"))):
            texts.append(result.text)
    return texts


# --- fetch_pallet_report -----------------------------------------------------

def test_fetch_pallet_report_lists_each_carton_once_in_generation_order(tmp_path):
    db_path = tmp_path / "barbell.db"
    ssccs = seed_pallet(db_path, copies=2)  # two print copies per carton

    report = fetch_pallet_report(PALLET_SSCC, db_path)

    assert report.pallet_sscc == PALLET_SSCC
    assert report.job_number == "122984"
    assert report.packing_slip_number == "100495"
    assert report.production_date == "2026-03-23"
    assert report.test_mode is False
    assert [c.sscc for c in report.cartons] == ssccs
    assert report.total_quantity == 20000
    first = report.cartons[0]
    assert first.description == "233458 - JWN White O/P Rum B 750Ml USA - PS"
    assert (first.quantity, first.batch, first.gtin) == (10000, "12298447388", GTIN)


def test_fetch_pallet_report_rejects_unknown_sscc(tmp_path):
    db_path = tmp_path / "barbell.db"
    seed_pallet(db_path)
    with pytest.raises(ValueError, match="No pallet found"):
        fetch_pallet_report("008600157112000128", db_path)  # a carton, not a pallet


def test_fetch_pallet_report_rejects_voided_pallet(tmp_path):
    db_path = tmp_path / "barbell.db"
    seed_pallet(db_path)
    void_pallet(PALLET_SSCC, db_path)
    with pytest.raises(ValueError, match="voided"):
        fetch_pallet_report(PALLET_SSCC, db_path)


# --- layout ---------------------------------------------------------------

def test_paginate_single_page_when_everything_fits():
    assert _paginate(0) == [(0, 0)]
    assert _paginate(3) == [(0, 3)]


def test_paginate_covers_every_carton_exactly_once():
    for count in (1, 7, 8, 9, 19, 20, 21, 60, 100):
        pages = _paginate(count)
        covered = [i for start, end in pages for i in range(start, end)]
        assert covered == list(range(count)), count


def test_totals_row_always_fits_on_the_last_page():
    from src import pallet_report as pr

    body_bottom = pr.PAGE_H_MM - pr.MARGIN_MM - pr.FOOTER_H_MM
    for count in range(0, 200):
        pages = _paginate(count)
        start, end = pages[-1]
        table_y = pr.FIRST_PAGE_TABLE_Y_MM if len(pages) == 1 else pr.LATER_PAGE_TABLE_Y_MM
        used = table_y + pr.HEADER_ROW_H_MM + (end - start) * pr.ROW_H_MM + pr.TOTALS_H_MM
        assert used <= body_bottom, count


def test_report_pages_are_us_letter_landscape_1bit():
    pages = render_pallet_report_pages(make_report(3))
    assert len(pages) == 1
    assert pages[0].mode == "1"
    assert pages[0].size == (3300, 2550)  # 11in x 8.5in at 300 DPI


# --- barcodes decode to what the labels carry ------------------------------

def test_pallet_and_carton_barcodes_decode_to_label_values():
    report = make_report(3)
    texts = decoded_texts(render_pallet_report_pages(report))

    assert f"(00){PALLET_SSCC}" in texts
    for carton in report.cartons:
        assert f"(02){GTIN}(11)260323(37){carton.quantity}(10)12298447388" in texts


def test_multi_page_report_repeats_pallet_barcode_and_lists_every_carton():
    report = make_report(30)
    pages = render_pallet_report_pages(report, printed_at=datetime.datetime(2026, 10, 23, 9, 0))

    assert len(pages) > 1
    texts = decoded_texts(pages)
    assert texts.count(f"(00){PALLET_SSCC}") == len(pages)  # one per page
    contents = [t for t in texts if t.startswith("(02)")]
    assert sorted(contents) == sorted(
        f"(02){GTIN}(11)260323(37){c.quantity}(10)12298447388" for c in report.cartons
    )


def test_test_pallet_gets_a_placeholder_instead_of_a_pallet_barcode():
    texts = decoded_texts(render_pallet_report_pages(make_report(2, pallet_sscc="TEST-SSCC-00001", test_mode=True)))

    # no pallet barcode - only the two real-looking carton SSCC barcodes decode
    assert sorted(t for t in texts if t.startswith("(00)")) == sorted(
        f"(00){c.sscc}" for c in make_report(2).cartons
    )
    assert len([t for t in texts if t.startswith("(02)")]) == 2  # carton contents still render


def test_carton_without_gtin_prints_a_note_instead_of_crashing():
    report = make_report(2)
    report.cartons[0].gtin = None
    texts = decoded_texts(render_pallet_report_pages(report))

    assert len([t for t in texts if t.startswith("(02)")]) == 1


# --- PDF output ----------------------------------------------------------------

def test_build_pallet_report_pdf_writes_a_pdf_with_one_page_per_report_page(tmp_path):
    out = build_pallet_report_pdf(make_report(30), tmp_path / "sub" / "report.pdf")

    data = out.read_bytes()
    assert data.startswith(b"%PDF")
    assert data.count(b"/Type /Page\n") == len(_paginate(30))


def test_each_carton_has_its_own_sscc_barcode_below_the_number():
    report = make_report(3)
    texts = decoded_texts(render_pallet_report_pages(report))

    for carton in report.cartons:
        assert f"(00){carton.sscc}" in texts


def test_carton_with_placeholder_test_sscc_gets_no_sscc_barcode():
    report = make_report(2)
    report.cartons[0].sscc = "TEST-SSCC-00001"
    texts = decoded_texts(render_pallet_report_pages(report))

    assert "(00)TEST-SSCC-00001" not in texts
    assert f"(00){report.cartons[1].sscc}" in texts


def test_carton_sscc_barcode_is_the_configured_height():
    from src import pallet_report as pr

    # 7.5mm at 300 DPI is ~89px; rendered bars must match that, not the library default
    img = pr._barcode_1bit("00008600157112000128", pr.CARTON_SSCC_BARCODE_HEIGHT_MM, pr._CARTON_SSCC_MODULE_MM)
    assert abs(img.height - pr.CARTON_SSCC_BARCODE_HEIGHT_MM * 300 / 25.4) <= 2


def test_company_name_is_printed_when_given():
    report = make_report(2)
    when = datetime.datetime(2026, 10, 26, 9, 0)
    without = render_pallet_report_pages(report, printed_at=when)[0]
    with_name = render_pallet_report_pages(report, printed_at=when, company_name="Caribbean Label Crafts Ltd.")[0]

    assert without.tobytes() != with_name.tobytes()
