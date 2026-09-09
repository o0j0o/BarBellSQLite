import json

from src.settings import Settings, load_settings, save_settings


def test_load_settings_returns_defaults_when_file_missing(tmp_path):
    settings = load_settings(tmp_path / "does_not_exist.json")
    assert settings == Settings()
    assert settings.output_dir == "output"
    assert settings.sscc_extension_digit == "0"


def test_save_then_load_roundtrips(tmp_path):
    path = tmp_path / "settings.json"
    original = Settings(
        output_dir="C:/CLC/bartender_csv",
        gs1_company_prefix="08600157112",
        sscc_extension_digit="1",
        sscc_state_file="C:/CLC/sscc_state.json",
    )
    save_settings(original, path)

    loaded = load_settings(path)
    assert loaded == original


def test_load_settings_fills_in_missing_fields_with_defaults(tmp_path):
    """An older or hand-edited settings.json missing a field shouldn't crash - it
    should fall back to that field's default rather than raising."""
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"gs1_company_prefix": "08600157112"}), encoding="utf-8")

    settings = load_settings(path)
    assert settings.gs1_company_prefix == "08600157112"
    assert settings.output_dir == "output"  # default, not present in the file


def test_load_settings_ignores_unknown_keys(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"output_dir": "x", "some_future_field": "y"}), encoding="utf-8")

    settings = load_settings(path)  # should not raise on the unknown key
    assert settings.output_dir == "x"
