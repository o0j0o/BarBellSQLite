import pytest

from generate_labels import require_valid_gtin, resolve_gtin
from src.labels import ProductInfo
from src.settings import Settings

VALID_BC_START = "0 51096 18492 1"
VALID_GTIN = "00051096184921"


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
    """require_valid_gtin() is the pure-blocking fallback used only when
    Settings.allow_manual_gtin_override is False (see resolve_gtin below for
    the Beta-default behaviour) - a valid GTIN just passes through silently."""
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


# --- resolve_gtin: the Beta-default (allow_manual_gtin_override=True) path -

def settings_with_override(allow=True):
    return Settings(allow_manual_gtin_override=allow)


def test_resolve_gtin_falls_back_to_require_valid_gtin_when_flag_off(monkeypatch):
    def _fail_if_called(*_):
        raise AssertionError("input() should not be called when the flag is off")

    monkeypatch.setattr("builtins.input", _fail_if_called)

    result = resolve_gtin(make_product(gtin=VALID_GTIN), settings_with_override(allow=False))
    assert result == VALID_GTIN


def test_resolve_gtin_falls_back_and_blocks_when_flag_off_and_gtin_invalid():
    with pytest.raises(SystemExit):
        resolve_gtin(
            make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)"),
            settings_with_override(allow=False),
        )


def test_resolve_gtin_pressing_enter_accepts_the_bc_start_default(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "")  # just press Enter

    result = resolve_gtin(
        make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START), settings_with_override()
    )
    assert result == VALID_GTIN


def test_resolve_gtin_retyping_the_same_value_needs_no_confirmation(monkeypatch):
    inputs = iter([VALID_BC_START])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(
        make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START), settings_with_override()
    )
    assert result == VALID_GTIN
    with pytest.raises(StopIteration):
        next(inputs)  # only one input() call happened - no confirmation prompt


def test_resolve_gtin_different_value_requires_confirmation_and_proceeds_on_yes(monkeypatch, capsys):
    inputs = iter(["12345670", "y"])  # different GTIN, then confirm
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(
        make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START), settings_with_override()
    )
    assert result == "00000012345670"
    output = capsys.readouterr().out
    assert VALID_GTIN in output  # shows the Label Traxx value
    assert "00000012345670" in output  # shows the value being used instead


def test_resolve_gtin_different_value_cancels_on_decline(monkeypatch):
    inputs = iter(["12345670", "n"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    with pytest.raises(SystemExit) as exc_info:
        resolve_gtin(
            make_product(gtin=VALID_GTIN, gtin_raw=VALID_BC_START), settings_with_override()
        )
    assert exc_info.value.code == 0


def test_resolve_gtin_prompts_directly_when_bc_start_empty(monkeypatch):
    inputs = iter([VALID_BC_START])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(
        make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)"),
        settings_with_override(),
    )
    assert result == VALID_GTIN


def test_resolve_gtin_reprompts_on_invalid_input_before_accepting(monkeypatch):
    inputs = iter(["not-digits", VALID_BC_START])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(
        make_product(gtin=None, gtin_raw="", gtin_error="GTIN is empty (no value)"),
        settings_with_override(),
    )
    assert result == VALID_GTIN
