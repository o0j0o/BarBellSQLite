import pytest

from generate_labels import require_valid_gtin
from src.labels import ProductInfo


def make_product(gtin=None, gtin_raw=None, gtin_error=None):
    return ProductInfo(
        prod_num="47388",
        item_number="233458",
        description="233458 - JWN White O/P Rum B 750Ml USA - PS",
        gtin=gtin,
        gtin_raw=gtin_raw,
        gtin_error=gtin_error,
    )


def test_require_valid_gtin_does_nothing_when_gtin_is_valid():
    """No manual override anymore (item 3) - a valid GTIN from Product.BC_Start
    just passes through silently."""
    require_valid_gtin(make_product(gtin="00000012345670"))  # must not raise/exit


def test_require_valid_gtin_blocks_and_exits_when_gtin_missing(capsys):
    product = make_product(
        gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)"
    )
    with pytest.raises(SystemExit) as exc_info:
        require_valid_gtin(product)
    assert exc_info.value.code == 1

    output = capsys.readouterr().out
    assert "233458" in output  # names the item
    assert "47388" in output  # names the P/N
    assert "GTIN is empty (no value)" in output  # what's wrong
    assert "''" in output  # the raw value as found


def test_require_valid_gtin_blocks_and_exits_when_gtin_invalid(capsys):
    product = make_product(
        gtin=None,
        gtin_raw="ABC123",
        gtin_error="GTIN must be all digits (after removing whitespace), got 'ABC123'",
    )
    with pytest.raises(SystemExit) as exc_info:
        require_valid_gtin(product)
    assert exc_info.value.code == 1

    output = capsys.readouterr().out
    assert "233458" in output
    assert "ABC123" in output
