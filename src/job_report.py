"""
Job Report: every pallet and carton BarBell has logged for ONE job, as a US Letter
(8.5" x 11") landscape PDF - the same page size, 300 DPI 1-bit drawing and look as
the Pallet Report (src/pallet_report.py, whose helpers this reuses).

It is a hierarchy:

  - each PALLET: its SSCC as a barcode and as a number, then the text of its
    GS1-128 contents - GTIN, product description, production date, quantity on
    the pallet, batch, and how many cartons it carries - followed by a list of
    every carton SSCC on that pallet (description, production date, quantity per
    carton, batch).
  - at the end, under "No Associated Pallet SSCC", the cartons that are not on
    any pallet.

Data comes from src.db.local_store.fetch_job_report() - BarBell's own SQLite
database only, never Label Traxx or ODBC. This module only lays it out, and the
same pages feed both the on-screen view and the PDF.
"""

import datetime
from pathlib import Path

from PIL import Image, ImageDraw

from src.db.local_store import JobReport, JobReportCarton, JobReportPallet
from src.gs1 import build_contents_element_string, build_sscc_barcode_data, build_sscc_element_string
from src.pallet_report import (
    DPI,
    MARGIN_MM,
    PAGE_H_MM,
    PAGE_W_MM,
    _barcode_1bit,
    _fit_font,
    _font,
    _is_real_sscc,
    _px,
    _text_width,
)
from src.version import version_string

NO_PALLET_HEADING = "No Associated Pallet SSCC"


def _fit_bold(draw, text: str, max_px: int, start_pt: float, min_pt: float):
    """The largest bold font up to start_pt in which text fits max_px."""
    pt = start_pt
    while pt > min_pt and _text_width(draw, text, _font(pt, bold=True)) > max_px:
        pt -= 0.5
    return _font(pt, bold=True)

_PALLET_MODULE_MM = 3 * 25.4 / DPI
FIRST_PAGE_TOP_MM = 56.0
LATER_PAGE_TOP_MM = 35.0
FOOTER_H_MM = 7.0
PALLET_BLOCK_H_MM = 27.0
TABLE_HEAD_H_MM = 6.5
ROW_H_MM = 5.8
SECTION_GAP_MM = 5.0
HEADING_H_MM = 9.0

# Carton table columns: # | Carton SSCC | Description | GTIN | Production Date | Qty per Carton | Batch.
# GTIN is a column (not just in the page header) because one job can hold several products.
COL_NUM = 13.0
COL_SSCC = 22.0
COL_DESC = 58.0
COL_GTIN = 140.0
COL_DATE_CENTER = 181.0  # the production date is centred on this line
COL_QTY_RIGHT = 222.0  # quantity is right-aligned to this edge
COL_BATCH = 227.0
BATCH_HEADING = "Batch (Job No. - P/N)"  # the batch is the job number followed by the product's P/N
COL_END = PAGE_W_MM - MARGIN_MM

_BOTTOM_MM = PAGE_H_MM - MARGIN_MM - FOOTER_H_MM


class _Layout:
    """Flows content down pages, starting a new page whenever the next piece
    would run past the footer. Pages are drawn as they are needed; the
    'Page n of N' numbers are added at the end, once N is known."""

    def __init__(self, report: JobReport, company_name: str | None):
        self.report = report
        self.company_name = company_name
        self.pages: list[Image.Image] = []
        self.draw: ImageDraw.ImageDraw | None = None
        self.y = 0.0
        self.left = _px(MARGIN_MM)
        self.right = _px(COL_END)
        self.desc_font = _font(9.5)

    # --- pages ------------------------------------------------------------

    def new_page(self):
        page = Image.new("1", (_px(PAGE_W_MM), _px(PAGE_H_MM)), 1)
        self.pages.append(page)
        self.draw = ImageDraw.Draw(page)
        draw, report = self.draw, self.report
        first = len(self.pages) == 1

        if self.company_name:
            draw.text((self.left, _px(MARGIN_MM - 2)), self.company_name, font=_font(12, bold=True), fill=0)
        draw.text((self.left, _px(MARGIN_MM + 4)), "JOB REPORT", font=_font(20, bold=True), fill=0)
        if report.test_mode:
            draw.text((self.left + _px(62), _px(MARGIN_MM + 7)), "TEST LABELS", font=_font(11, bold=True), fill=0)

        if first:
            label_font, value_font = _font(10), _font(10, bold=True)
            details = [
                ("Job No:", report.job_number),
                ("Packing Slip:", report.packing_slip_number or "-"),
                ("Customer:", report.customer_name or "-"),
            ]
            for i, (label, value) in enumerate(details):
                col, row = divmod(i, 3)
                x = _px(MARGIN_MM + col * 120)
                y = _px(28 + row * 7)
                draw.text((x, y), label, font=label_font, fill=0)
                room = _px(92 if col == 0 else 108)
                draw.text((x + _px(28), y), value, font=_fit_font(draw, value, room, 10.0, 6.5), fill=0)
            total = (
                f"{len(report.pallets):,} pallet(s)   {report.carton_total:,} carton(s) in total"
            )
            draw.text((self.left, _px(49.5)), total, font=_font(11, bold=True), fill=0)
            draw.line([(self.left, _px(54.0)), (self.right, _px(54.0))], fill=0, width=3)
            self.y = FIRST_PAGE_TOP_MM
        else:
            draw.text(
                (self.left, _px(MARGIN_MM + 12.5)), f"Job {report.job_number}",
                font=_font(11, bold=True), fill=0,
            )
            self.y = LATER_PAGE_TOP_MM

    def ensure(self, height_mm: float):
        if self.draw is None or self.y + height_mm > _BOTTOM_MM:
            self.new_page()

    # --- pieces -----------------------------------------------------------

    def table_header(self):
        self.ensure(TABLE_HEAD_H_MM + ROW_H_MM)
        draw, head_font = self.draw, _font(9, bold=True)
        ty = _px(self.y + 1.0)
        draw.text((_px(COL_NUM), ty), "#", font=head_font, fill=0)
        draw.text((_px(COL_SSCC), ty), "Carton SSCC", font=head_font, fill=0)
        draw.text((_px(COL_DESC), ty), "Description", font=head_font, fill=0)
        draw.text((_px(COL_GTIN), ty), "GTIN", font=head_font, fill=0)
        date = "Production Date"
        draw.text((_px(COL_DATE_CENTER) - _text_width(draw, date, head_font) // 2, ty), date, font=head_font, fill=0)
        qty = "Qty per Carton"
        draw.text((_px(COL_QTY_RIGHT) - _text_width(draw, qty, head_font), ty), qty, font=head_font, fill=0)
        batch_font = _fit_bold(draw, BATCH_HEADING, _px(COL_END - COL_BATCH), 9.0, 6.5)
        draw.text((_px(COL_BATCH), ty), BATCH_HEADING, font=batch_font, fill=0)
        rule_y = _px(self.y + TABLE_HEAD_H_MM) - 2
        draw.line([(self.left, rule_y), (self.right, rule_y)], fill=0, width=3)
        self.y += TABLE_HEAD_H_MM

    def carton_row(self, index: int, carton: JobReportCarton):
        draw = self.draw
        top = _px(self.y + 0.9)
        body = _font(9.5)
        draw.text((_px(COL_NUM), top), str(index), font=_font(8.5), fill=0)
        draw.text((_px(COL_SSCC), top), carton.sscc, font=_fit_bold(draw, carton.sscc, _px(COL_DESC - COL_SSCC - 2), 9.5, 6.5), fill=0)
        draw.text(
            (_px(COL_DESC), top), carton.description,
            font=self.desc_font, fill=0,
        )
        gtin = carton.gtin or "-"
        draw.text((_px(COL_GTIN), top), gtin, font=body, fill=0)
        date_font = body
        draw.text(
            (_px(COL_DATE_CENTER) - _text_width(draw, carton.production_date, date_font) // 2, top),
            carton.production_date, font=date_font, fill=0,
        )
        qty = f"{carton.quantity:,}"
        draw.text((_px(COL_QTY_RIGHT) - _text_width(draw, qty, body), top), qty, font=body, fill=0)
        draw.text(
            (_px(COL_BATCH), top), carton.batch,
            font=_fit_font(draw, carton.batch, _px(COL_END - COL_BATCH), 9.5, 6.0), fill=0,
        )
        self.y += ROW_H_MM
        draw.line([(self.left, _px(self.y) - 1), (self.right, _px(self.y) - 1)], fill=0, width=1)

    def cartons(self, cartons: list[JobReportCarton], continued_label: str | None):
        """The carton table, repeating its column header (and what it belongs
        to) when it runs onto a new page."""
        self.table_header()
        # one description size for the whole table (the smallest any row needs), so rows look alike
        room = _px(COL_GTIN - COL_DESC - 2)
        self.desc_font = min(
            (_fit_font(self.draw, c.description, room, 9.5, 6.0) for c in cartons),
            key=lambda f: f.size, default=_font(9.5),
        )
        for index, carton in enumerate(cartons, start=1):
            if self.y + ROW_H_MM > _BOTTOM_MM:
                self.new_page()
                if continued_label:
                    self.draw.text(
                        (self.left, _px(self.y)), continued_label + "  (continued)",
                        font=_font(10, bold=True), fill=0,
                    )
                    self.y += 6.5
                self.table_header()
            self.carton_row(index, carton)

    def pallet_block(self, pallet: JobReportPallet):
        self.ensure(PALLET_BLOCK_H_MM + TABLE_HEAD_H_MM + 2 * ROW_H_MM)
        draw = self.draw
        top = self.y
        draw.line([(self.left, _px(top)), (self.right, _px(top))], fill=0, width=5)

        # The pallet's SSCC: barcode, then the number.
        bx, by = self.left, _px(top + 2.5)
        if _is_real_sscc(pallet.sscc):
            barcode = _barcode_1bit(build_sscc_barcode_data(pallet.sscc), 13.0, _PALLET_MODULE_MM)
            draw_w = min(barcode.width, _px(92))
            if barcode.width > draw_w:
                barcode = barcode.convert("L").resize(
                    (draw_w, barcode.height), Image.LANCZOS
                ).point(lambda v: 255 if v > 128 else 0).convert("1")
            self.pages[-1].paste(barcode, (bx, by))
        else:  # a TEST-SSCC placeholder can't be encoded as a barcode
            draw.rectangle((bx, by, bx + _px(70), by + _px(13)), outline=0, width=3)
            draw.text((bx + _px(3), by + _px(2.5)), "TEST PALLET\nno barcode - fake SSCC", font=_font(8, bold=True), fill=0)
        draw.text(
            (bx, _px(top + 17.0)), build_sscc_element_string(pallet.sscc),
            font=_font(13, bold=True, mono=True), fill=0,
        )

        # The text of the pallet label's GS1-128 contents.
        label_font, value_font = _font(9.5), _font(9.5, bold=True)
        x1, x2 = _px(104), _px(200)
        rows = [
            (x1, 0, "GTIN:", pallet.gtin or "-", _px(60)),
            (x1, 1, "Production Date:", pallet.production_date, _px(60)),
            (x1, 2, "Cartons on Pallet:", f"{pallet.carton_count:,}", _px(60)),
            (x2, 0, "Pallet Qty:", f"{pallet.quantity:,}", self.right - x2 - _px(33)),
            (x2, 1, "Batch:", pallet.batch, self.right - x2 - _px(33)),
        ]
        for x, row, label, value, room in rows:
            y = _px(top + 2.0 + row * 4.9)
            draw.text((x, y), label, font=label_font, fill=0)
            vx = x + _px(33)
            draw.text((vx, y), value, font=_fit_font(draw, value, room, 9.5, 6.5), fill=0)
        y = _px(top + 2.0 + 3 * 4.9)
        draw.text((x1, y), "Description:", font=label_font, fill=0)
        draw.text(
            (x1 + _px(33), y), pallet.description,
            font=_fit_font(draw, pallet.description, self.right - x1 - _px(33), 9.5, 6.5), fill=0,
        )
        if pallet.gtin:
            contents = build_contents_element_string(
                pallet.gtin, pallet.production_date, pallet.quantity, pallet.batch
            )
            draw.text(
                (x1, _px(top + 2.0 + 4 * 4.9)), contents,
                font=_fit_font(draw, contents, self.right - x1, 9.0, 5.5), fill=0,
            )
        self.y = top + PALLET_BLOCK_H_MM
        label = f"Pallet {build_sscc_element_string(pallet.sscc)}"
        if pallet.cartons:
            self.cartons(pallet.cartons, label)
        else:
            self.ensure(ROW_H_MM + 2)
            draw = self.draw
            draw.text(
                (_px(COL_SSCC), _px(self.y + 0.5)), "No cartons are linked to this pallet.",
                font=_font(9.5), fill=0,
            )
            self.y += ROW_H_MM
        self.y += SECTION_GAP_MM

    def no_pallet_section(self):
        self.ensure(HEADING_H_MM + TABLE_HEAD_H_MM + 2 * ROW_H_MM)
        draw = self.draw
        draw.line([(self.left, _px(self.y)), (self.right, _px(self.y))], fill=0, width=5)
        draw.text((self.left, _px(self.y + 2.0)), NO_PALLET_HEADING, font=_font(13, bold=True), fill=0)
        self.y += HEADING_H_MM
        cartons = self.report.unassociated_cartons
        if cartons:
            self.cartons(cartons, NO_PALLET_HEADING)
        else:
            draw.text((_px(COL_SSCC), _px(self.y + 0.5)), "None - every carton is on a pallet.", font=_font(9.5), fill=0)
            self.y += ROW_H_MM
        self.y += SECTION_GAP_MM


def render_job_report_pages(
    report: JobReport,
    printed_at: datetime.datetime | None = None,
    company_name: str | None = None,
) -> list[Image.Image]:
    """One 1-bit PIL image per page, US Letter landscape at 300 DPI."""
    printed_at = printed_at or datetime.datetime.now()
    layout = _Layout(report, company_name)
    layout.new_page()

    if not report.pallets and not report.unassociated_cartons:
        layout.draw.text(
            (layout.left, _px(layout.y + 4)),
            "No pallets or cartons have been logged for this job.", font=_font(12), fill=0,
        )
    for pallet in report.pallets:
        layout.pallet_block(pallet)
    layout.no_pallet_section()

    total_pages = len(layout.pages)
    footer_font = _font(8)
    for number, page in enumerate(layout.pages, start=1):
        draw = ImageDraw.Draw(page)
        page_text = f"Page {number} of {total_pages}"
        draw.text(
            (layout.right - _text_width(draw, page_text, _font(10)), _px(MARGIN_MM + 6)),
            page_text, font=_font(10), fill=0,
        )
        draw.text(
            (layout.left, _px(PAGE_H_MM - MARGIN_MM - 3)),
            f"BarBell {version_string()}  -  printed {printed_at:%Y-%m-%d %H:%M}",
            font=footer_font, fill=0,
        )
        job_text = f"Job {report.job_number}"
        draw.text(
            (layout.right - _text_width(draw, job_text, footer_font), _px(PAGE_H_MM - MARGIN_MM - 3)),
            job_text, font=footer_font, fill=0,
        )
    return layout.pages


def build_job_report_pdf(
    report: JobReport,
    out_path: Path | str,
    printed_at: datetime.datetime | None = None,
    company_name: str | None = None,
) -> Path:
    """Writes the report as a PDF at out_path (parent dirs created) and returns the path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pages = render_job_report_pages(report, printed_at, company_name)
    pages[0].save(out_path, "PDF", resolution=float(DPI), save_all=True, append_images=pages[1:])
    return out_path
