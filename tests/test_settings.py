import json

from src.settings import JAMAICA_LABEL_TRAXX_DSN, Settings, load_settings, save_settings


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


# --- per-plant SSCC config: active_* properties (QUESTIONS.md #19) ---------

def make_settings(**overrides):
    defaults = dict(
        gs1_company_prefix="08600157112",
        sscc_extension_digit="0",
        sscc_state_file="sscc_state.json",
        jamaica_gs1_company_prefix="",
        jamaica_sscc_extension_digit="1",
        jamaica_sscc_state_file="sscc_state_jamaica.json",
    )
    defaults.update(overrides)
    return Settings(**defaults)


def test_is_jamaica_plant_false_when_dsn_unset_or_barbados():
    assert make_settings(label_traxx_dsn="").is_jamaica_plant is False
    assert make_settings(label_traxx_dsn="LT64").is_jamaica_plant is False


def test_is_jamaica_plant_true_when_dsn_is_jamaicas():
    assert make_settings(label_traxx_dsn=JAMAICA_LABEL_TRAXX_DSN).is_jamaica_plant is True


def test_active_fields_resolve_to_barbados_by_default():
    settings = make_settings(label_traxx_dsn="LT64")
    assert settings.active_gs1_company_prefix == "08600157112"
    assert settings.active_sscc_extension_digit == "0"
    assert settings.active_sscc_state_file == "sscc_state.json"


def test_active_fields_resolve_to_jamaica_when_selected():
    settings = make_settings(
        label_traxx_dsn=JAMAICA_LABEL_TRAXX_DSN,
        jamaica_gs1_company_prefix="08600157112",
        jamaica_sscc_extension_digit="1",
        jamaica_sscc_state_file="sscc_state_jamaica.json",
    )
    assert settings.active_gs1_company_prefix == "08600157112"
    assert settings.active_sscc_extension_digit == "1"
    assert settings.active_sscc_state_file == "sscc_state_jamaica.json"


def test_active_prefix_falls_back_to_barbados_when_jamaica_prefix_unset():
    """Both plants share one prefix by default - Jamaica's own field starts
    blank and only needs setting if that ever changes."""
    settings = make_settings(
        label_traxx_dsn=JAMAICA_LABEL_TRAXX_DSN, jamaica_gs1_company_prefix=""
    )
    assert settings.active_gs1_company_prefix == "08600157112"


def test_editing_jamaica_extension_digit_never_affects_barbados():
    settings = make_settings(
        label_traxx_dsn=JAMAICA_LABEL_TRAXX_DSN, jamaica_sscc_extension_digit="3"
    )
    assert settings.active_sscc_extension_digit == "3"
    assert settings.sscc_extension_digit == "0"  # Barbados' own field, untouched

    settings.label_traxx_dsn = "LT64"  # switch plants
    assert settings.active_sscc_extension_digit == "0"  # back to Barbados, unaffected
    assert settings.jamaica_sscc_extension_digit == "3"  # Jamaica's edit preserved
