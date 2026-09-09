import pytest

from generate_labels import resolve_gtin
from src.labels import ProductInfo


def make_product(gtin=None):
    return ProductInfo(
        prod_num="47388",
        item_number="233458",
        description="233458 - JWN White O/P Rum B 750Ml USA - PS",
        gtin=gtin,
    )


def test_resolve_gtin_prompts_and_returns_normalized_value_on_choice_1(monkeypatch):
    inputs = iter(["1", "6291041500213"])  # choice 1 (enter now), then a valid GTIN
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(make_product())
    assert result == "06291041500213"


def test_resolve_gtin_reprompts_on_invalid_gtin_before_accepting(monkeypatch):
    inputs = iter(["1", "not-digits", "6291041500213"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    result = resolve_gtin(make_product())
    assert result == "06291041500213"


def test_resolve_gtin_exits_cleanly_on_choice_2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "2")

    with pytest.raises(SystemExit) as exc_info:
        resolve_gtin(make_product())
    assert exc_info.value.code == 0


def test_resolve_gtin_rejects_bad_choice_then_accepts_2(monkeypatch):
    inputs = iter(["9", "2"])
    monkeypatch.setattr("builtins.input", lambda *_: next(inputs))

    with pytest.raises(SystemExit):
        resolve_gtin(make_product())


def test_resolve_gtin_skips_prompt_entirely_when_gtin_already_on_file(monkeypatch):
    def _fail_if_called(*_):
        raise AssertionError("input() should not be called when a GTIN is already on file")

    monkeypatch.setattr("builtins.input", _fail_if_called)

    result = resolve_gtin(make_product(gtin="00000012345670"))
    assert result is None
