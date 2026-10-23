"""
Pallet Report: a one-pallet, A4-landscape PDF listing every carton on the
pallet - carton SSCC, description, quantity, batch, and a small GS1-128
contents barcode built exactly like the one on the carton's own label
(src.gs1.build_contents_barcode_data) - with the pallet's own SSCC barcode at
the top of the first page (and a smaller copy on each later page, so a page
separated from the rest still identifies its pallet).

Pages are drawn with Pillow at 300 DPI in 1-bit mode and saved as a PDF
(Pillow encodes 1-bit pages losslessly, CCITT G4) - no PDF library needed,
and 1-bit means the barcode bars stay hard-edged with no JPEG/anti-alias
fringing. Text is therefore part of the page image, not selectable.

Data comes from src.db.local_store.fetch_pallet_report(); this module only
lays it out.
"""

import datetime
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from src.barcode_render import render_barcode_image
from src.db.local_store import PalletReport, PalletReportCarton
from src.gs1 import (
    build_contents_barcode_data,
    build_contents_element_string,
    build_sscc_barcode_data,
    build_sscc_element_string,
)
from src.version import version_string

DPI = 300
PAGE_W_MM, PAGE_H_MM = 297.0, 210.0  # A4 landscape
MARGIN_MM = 12.0

# Barcode bars are drawn at exactly 2px per module (0.169mm) so every bar is
# a whole number of pixels - a fractional module width would alias unevenly.
_MODULE_MM = 2 * 25.4 / DPI
_PALLET_MODULE_MM = 4 * 25.4 / DPI  # the pallet's own barcode is the prominent one

ROW_H_MM = 15.0
HEADER_ROW_H_MM = 7.0
TOTALS_H_MM = 9.0
FOOTER_H_MM = 7.0
FIRST_PAGE_TABLE_Y_MM = 60.0
LATER_PAGE_TABLE_Y_MM = 28.0

# Table column left edges / right edge, in mm.
COL_NUM = 12.0
COL_SSCC = 24.0
COL_DESC = 72.0
COL_QTY_RIGHT = 176.0  # quantity is right-aligned to this edge
COL_BATCH = 182.0
COL_BARCODE = 212.0
COL_END = PAGE_W_MM - MARGIN_MM

_FONT_CANDIDATES = {
    False: ("arial.ttf", "DejaVuSans.ttf"),
    True: ("arialbd.ttf", "DejaVuSans-Bold.ttf"),
}
_MONO_CANDIDATES = ("cour.ttf", "DejaVuSansMono.ttf")


def _px(mm: float) -> int:
    return round(mm * DPI / 25.4)


@lru_cache(maxsize=None)
def _font(size_pt: float, bold: bool = False, mono: bool = False) -> ImageFont.ImageFont:
    size_px = max(1, round(size_pt * DPI / 72))
    for name in (_MONO_CANDIDATES if mono else _FONT_CANDIDATES[bold]):
        try:
            return ImageFont.truetype(name, size_px)
        except OSError:
            continue
    return ImageFont.load_default(size=size_px)


def _text_width(draw: ImageDraw.ImageDraw, text: str, font) -> int:
    return round(draw.textlength(text, font=font))


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, max_px: int, max_lines: int) -> list[str]:
    """Greedy word wrap to at most max_lines; an overlong remainder is cut
    with an ellipsis rather than silently dropped."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if _text_width(draw, trial, font) <= max_px or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and _text_width(draw, last + "...", font) > max_px:
            last = last[:-1]
        lines[-1] = last.rstrip() + "..."
    return lines


def _barcode_1bit(barcode_data: str, module_height_mm: float, module_mm: float) -> Image.Image:
    """The barcode as a 1-bit image with no quiet zone baked in (the page
    layout supplies the surrounding white space)."""
    img = render_barcode_image(
        barcode_data, module_height=module_height_mm, module_width=module_mm, quiet_zone=0
    )
    return img.convert("L").point(lambda v: 255 if v > 128 else 0).convert("1")


def _paste_barcode(page: Image.Image, barcode: Image.Image, x_px: int, y_px: int, max_w_px: int):
    if barcode.width > max_w_px:  # unusually long batch/qty - shrink rather than overflow
        scale = max_w_px / barcode.width
        barcode = barcode.convert("L").resize(
            (max_w_px, max(1, round(barcode.height * scale))), Image.LANCZOS
        ).point(lambda v: 255 if v > 128 else 0).convert("1")
    page.paste(barcode, (x_px, y_px))


def _fit_mono(draw, text: str, max_px: int, start_pt: float, min_pt: float = 5.0):
    pt = start_pt
    while pt > min_pt and _text_width(draw, text, _font(pt, mono=True)) > max_px:
        pt -= 0.5
    return _font(pt, mono=True)


def _carton_contents_barcode(carton: PalletReportCarton) -> tuple[str, str] | None:
    """(raw barcode data, human-readable AI string) for the carton's
    contents barcode, or None if the carton has no GTIN to build one from."""
    if not carton.gtin or not carton.production_date:
        return None
    return (
        build_contents_barcode_data(carton.gtin, carton.production_date, carton.quantity, carton.batch),
        build_contents_element_string(carton.gtin, carton.production_date, carton.quantity, carton.batch),
    )


def _is_real_sscc(sscc: str) -> bool:
    """False for build_test_sscc()'s TEST-SSCC-##### placeholders, which
    aren't digits and so can't be encoded as a (00) GS1-128 barcode."""
    return sscc.isdigit()


def _paginate(carton_count: int) -> list[tuple[int, int]]:
    """[(start, end)) carton index ranges, one per page. The last page also
    needs room for the totals row; if it wouldn't fit under the final
    carton, the totals row gets a page of its own (an empty range)."""
    def rows_that_fit(table_y_mm: float, extra_mm: float = 0.0) -> int:
        body_bottom = PAGE_H_MM - MARGIN_MM - FOOTER_H_MM - extra_mm
        return int((body_bottom - table_y_mm - HEADER_ROW_H_MM) // ROW_H_MM)

    pages: list[tuple[int, int]] = []
    start = 0
    table_y = FIRST_PAGE_TABLE_Y_MM
    while True:
        remaining = carton_count - start
        if remaining <= rows_that_fit(table_y, TOTALS_H_MM):
            pages.append((start, carton_count))
            return pages
        end = min(carton_count, start + rows_that_fit(table_y))
        pages.append((start, end))
        start = end
        table_y = LATER_PAGE_TABLE_Y_MM
        if start >= carton_count:  # totals row alone on a new page
            pages.append((start, start))
            return pages


def _format_created(created_at: str) -> str:
    try:
        return datetime.datetime.fromisoformat(created_at).astimezone().strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return created_at


def render_pallet_report_pages(
    report: PalletReport, printed_at: datetime.datetime | None = None
) -> list[Image.Image]:
    """One 1-bit PIL image per page, A4 landscape at 300 DPI."""
    printed_at = printed_at or datetime.datetime.now()
    pages_ranges = _paginate(len(report.cartons))
    total_pages = len(pages_ranges)
    sscc_is_real = _is_real_sscc(report.pallet_sscc)
    pallet_barcode_data = build_sscc_barcode_data(report.pallet_sscc) if sscc_is_real else None
    pallet_ai_text = build_sscc_element_string(report.pallet_sscc)

    pages = []
    for page_index, (start, end) in enumerate(pages_ranges):
        page = Image.new("1", (_px(PAGE_W_MM), _px(PAGE_H_MM)), 1)
        draw = ImageDraw.Draw(page)
        first = page_index == 0
        left, right = _px(MARGIN_MM), _px(COL_END)

        # --- header ----------------------------------------------------
        draw.text((left, _px(MARGIN_MM)), "PALLET CONTENTS REPORT", font=_font(20, bold=True), fill=0)
        page_text = f"Page {page_index + 1} of {total_pages}"
        page_font = _font(10)
        draw.text(
            (right - _text_width(draw, page_text, page_font), _px(MARGIN_MM + 2)),
            page_text, font=page_font, fill=0,
        )

        if first:
            barcode_y = _px(26.0)
            if pallet_barcode_data:
                barcode = _barcode_1bit(pallet_barcode_data, 18.0, _PALLET_MODULE_MM)
                page.paste(barcode, (left, barcode_y))
            else:
                box = (left, barcode_y, left + _px(60), barcode_y + _px(18))
                draw.rectangle(box, outline=0, width=3)
                draw.text(
                    (left + _px(4), barcode_y + _px(4)),
                    "TEST PALLET\nno barcode - fake SSCC", font=_font(10, bold=True), fill=0,
                )
            draw.text((left, _px(46.5)), pallet_ai_text, font=_font(14, bold=True, mono=True), fill=0)

            details = [
                ("Job No:", report.job_number),
                ("Packing Slip:", report.packing_slip_number or "-"),
                ("Production Date:", report.production_date or "-"),
                ("Pallet Created:", _format_created(report.created_at)),
                ("Cartons:", f"{len(report.cartons):,}"),
                ("Total Qty:", f"{report.total_quantity:,}"),
            ]
            label_font, value_font = _font(10), _font(10, bold=True)
            for i, (label, value) in enumerate(details):
                col, row = divmod(i, 3)
                x = _px(120 + col * 80)
                y = _px(28 + row * 7)
                draw.text((x, y), label, font=label_font, fill=0)
                draw.text((x + _px(30), y), value, font=value_font, fill=0)
            table_y_mm = FIRST_PAGE_TABLE_Y_MM
        else:
            if pallet_barcode_data:
                small = _barcode_1bit(pallet_barcode_data, 8.0, _MODULE_MM)
                page.paste(small, (right - small.width - _px(40), _px(MARGIN_MM - 2)))
            draw.text(
                (left, _px(MARGIN_MM + 9)), f"Pallet {pallet_ai_text}   Job {report.job_number}",
                font=_font(11, bold=True), fill=0,
            )
            table_y_mm = LATER_PAGE_TABLE_Y_MM

        # --- table header ----------------------------------------------
        head_y = _px(table_y_mm)
        head_font = _font(9, bold=True)
        text_y = head_y + _px(1.5)
        draw.text((_px(COL_NUM), text_y), "#", font=head_font, fill=0)
        draw.text((_px(COL_SSCC), text_y), "Carton SSCC", font=head_font, fill=0)
        draw.text((_px(COL_DESC), text_y), "Description", font=head_font, fill=0)
        qty_head = "Qty"
        draw.text(
            (_px(COL_QTY_RIGHT) - _text_width(draw, qty_head, head_font), text_y),
            qty_head, font=head_font, fill=0,
        )
        draw.text((_px(COL_BATCH), text_y), "Batch", font=head_font, fill=0)
        draw.text((_px(COL_BARCODE), text_y), "Contents barcode (GS1-128)", font=head_font, fill=0)
        rule_y = head_y + _px(HEADER_ROW_H_MM) - 2
        draw.line([(left, rule_y), (right, rule_y)], fill=0, width=3)

        # --- carton rows -----------------------------------------------
        body_font, small_font, num_font = _font(10.5), _font(9), _font(9)
        sscc_font = _font(11, bold=True)
        row_y = head_y + _px(HEADER_ROW_H_MM)
        for offset, carton in enumerate(report.cartons[start:end]):
            index = start + offset + 1
            top = row_y + _px(1.8)
            draw.text((_px(COL_NUM), top), str(index), font=num_font, fill=0)
            draw.text((_px(COL_SSCC), top), carton.sscc, font=sscc_font, fill=0)

            desc_lines = _wrap(draw, carton.description, small_font, _px(COL_QTY_RIGHT - 24 - COL_DESC), 3)
            for line_no, line in enumerate(desc_lines):
                draw.text((_px(COL_DESC), top + line_no * _px(3.9)), line, font=small_font, fill=0)

            qty_text = f"{carton.quantity:,}"
            draw.text(
                (_px(COL_QTY_RIGHT) - _text_width(draw, qty_text, body_font), top),
                qty_text, font=body_font, fill=0,
            )
            draw.text((_px(COL_BATCH), top), carton.batch, font=body_font, fill=0)

            contents = _carton_contents_barcode(carton)
            col_w = _px(COL_END - COL_BARCODE)
            if contents:
                data, ai_text = contents
                barcode = _barcode_1bit(data, 7.0, _MODULE_MM)
                _paste_barcode(page, barcode, _px(COL_BARCODE), top - _px(0.6), col_w)
                draw.text(
                    (_px(COL_BARCODE), top + _px(7.8)), ai_text,
                    font=_fit_mono(draw, ai_text, col_w, 7.0), fill=0,
                )
            else:
                draw.text(
                    (_px(COL_BARCODE), top), "no barcode - carton has no GTIN on record",
                    font=small_font, fill=0,
                )

            row_y += _px(ROW_H_MM)
            draw.line([(left, row_y - 2), (right, row_y - 2)], fill=0, width=1)

        # --- totals (last page only) -------------------------------------
        if page_index == total_pages - 1:
            draw.line([(left, row_y + 2), (right, row_y + 2)], fill=0, width=3)
            total_font = _font(11, bold=True)
            ty = row_y + _px(2.5)
            draw.text(
                (_px(COL_SSCC), ty),
                f"TOTAL - {len(report.cartons):,} carton(s)", font=total_font, fill=0,
            )
            total_text = f"{report.total_quantity:,}"
            draw.text(
                (_px(COL_QTY_RIGHT) - _text_width(draw, total_text, total_font), ty),
                total_text, font=total_font, fill=0,
            )

        # --- footer ------------------------------------------------------
        footer_y = _px(PAGE_H_MM - MARGIN_MM - 3)
        footer_font = _font(8)
        draw.text(
            (left, footer_y),
            f"BarBell {version_string()}  -  printed {printed_at:%Y-%m-%d %H:%M}",
            font=footer_font, fill=0,
        )
        draw.text(
            (right - _text_width(draw, pallet_ai_text, footer_font), footer_y),
            pallet_ai_text, font=footer_font, fill=0,
        )
        pages.append(page)
    return pages


def build_pallet_report_pdf(
    report: PalletReport, out_path: Path | str, printed_at: datetime.datetime | None = None
) -> Path:
    """Writes the report as a PDF at out_path (parent dirs created) and
    returns the path."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pages = render_pallet_report_pages(report, printed_at)
    pages[0].save(
        out_path, "PDF", resolution=float(DPI), save_all=True, append_images=pages[1:]
    )
    return out_path
