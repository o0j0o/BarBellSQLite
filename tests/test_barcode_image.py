"""
Round-trips the rendered barcode images through zxing-cpp - a completely
independent decoder from the python-barcode encoder used to draw them - to
catch any FNC1/AI-structure mistake that would make a barcode look fine but
scan wrong (or not at all). zxing-cpp/numpy are test-only dependencies, not
needed by the app itself.
"""

import numpy as np
import zxingcpp

from src.barcode_render import render_barcode_image
from src.gs1 import build_contents_barcode_data, build_sscc_barcode_data


def decode(pil_image):
    results = zxingcpp.read_barcodes(np.array(pil_image.convert("L")))
    assert len(results) == 1, f"expected exactly one barcode, got {len(results)}"
    return results[0]


def test_contents_barcode_round_trips_to_users_real_example():
    """
    Directly verified against the real GS1-128 string the user pasted:
    (02)00721059000635(11)260515(37)5000(10)122984
    """
    data = build_contents_barcode_data(
        gtin="00721059000635", production_date_iso="2026-05-15", quantity=5000, batch="122984"
    )
    image = render_barcode_image(data)

    result = decode(image)
    assert result.format.name == "Code128"
    assert result.text == "(02)00721059000635(11)260515(37)5000(10)122984"


def test_contents_barcode_with_real_job_122984_batch():
    data = build_contents_barcode_data(
        gtin="00000012345670",
        production_date_iso="2026-03-23",
        quantity=27000,
        batch="12298447388",  # job number + ProductNo, per the corrected batch rule
    )
    image = render_barcode_image(data)

    result = decode(image)
    assert result.text == "(02)00000012345670(11)260323(37)27000(10)12298447388"


def test_sscc_barcode_round_trips():
    data = build_sscc_barcode_data("008600157112000104")
    image = render_barcode_image(data)

    result = decode(image)
    assert result.text == "(00)008600157112000104"


def test_decoded_bytes_show_fnc1_as_group_separator_before_batch():
    """
    The raw decoded bytes (not the AI-parsed text) should show the FNC1
    separator landing exactly between the quantity and the batch AI - not
    missing, and not misplaced.
    """
    data = build_contents_barcode_data(
        gtin="00721059000635", production_date_iso="2026-05-15", quantity=5000, batch="122984"
    )
    image = render_barcode_image(data)
    result = decode(image)

    assert result.bytes == b"020072105900063511260515375000\x1d10122984"
