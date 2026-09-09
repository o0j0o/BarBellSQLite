"""
Renders GS1-128 barcodes as actual scannable images, so the AI element
strings in src/gs1.py can be checked with a real scanner or phone camera
before anything gets printed.

Uses python-barcode's Gs1_128 class (a tested Code 128 implementation that
already handles the leading FNC1 GS1-128 requires) rather than hand-rolling
Code 128 encoding - getting that wrong produces something that looks like a
barcode but doesn't scan correctly, which is worse than not having one.
"""

from barcode.codex import Gs1_128
from barcode.writer import ImageWriter
from PIL import Image


def render_barcode_image(barcode_data: str, module_height: float = 15.0) -> Image.Image:
    """
    barcode_data: raw GS1-128 data from src/gs1.py's build_*_barcode_data()
    functions (FNC1 already embedded where required, no parentheses).
    Returns a PIL Image - the human-readable text is turned off since the
    AI-formatted string is already shown separately (and would otherwise
    render the FNC1 byte as a stray character - see Gs1_128.get_fullcode()).
    """
    bc = Gs1_128(barcode_data, writer=ImageWriter())
    return bc.render(writer_options={"write_text": False, "module_height": module_height})
