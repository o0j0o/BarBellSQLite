"""
Operational, per-plant BarBell settings - editable via setup_gui.py.

Deliberately separate from .env: .env holds only the Label Traxx connection
credentials (LT_DSN/LT_HOST/LT_PORT/LT_USER/LT_PASSWORD), which aren't meant
to be hand-edited through a GUI. Everything here is plant-specific config
that was previously static in code - the GS1 Company Prefix and SSCC
extension digit can differ at other CLC plants, and the CSV output location
is a per-machine choice.
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_SETTINGS_FILE = Path(__file__).resolve().parent.parent / "settings.json"


@dataclass
class Settings:
    output_dir: str = "output"
    gs1_company_prefix: str = ""
    sscc_extension_digit: str = "0"
    sscc_state_file: str = "sscc_state.json"
    # Soft deterrent so Setup isn't one accidental click away from the main
    # app's About dialog - not real access control (anyone who can edit this
    # file can read or change it), just a "are you sure you meant to" gate.
    setup_password: str = "change4GOOD"
    # Beta-only measure: CLC is still registering GTINs into Label Traxx, so
    # Product.BC_Start can't yet be treated as the sole authoritative source -
    # manual entry stays available for every run, not just when BC_Start is
    # empty. Flip to False once BC_Start is trustworthy enough to be
    # authoritative (see QUESTIONS.md - revisit before 1.0.0); the textbox
    # then reverts to enabled only when BC_Start is empty, no code change.
    allow_manual_gtin_override: bool = True
    # Append-only audit trail (JSON Lines) of every GTIN sourcing decision -
    # see src/audit.py.
    audit_log_file: str = "gtin_audit_log.jsonl"
    # Local SQLite database (Jobs + Labels tables) - BarBell's own record of
    # every job and label it has generated, separate from Label Traxx. See
    # src/db/local_store.py.
    local_db_file: str = "barbell.db"


def load_settings(path: Path | str = DEFAULT_SETTINGS_FILE) -> Settings:
    """Missing file (first run) -> defaults. Unknown keys in the file are ignored."""
    path = Path(path)
    if not path.exists():
        return Settings()
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    known_fields = {f for f in Settings.__dataclass_fields__}
    return Settings(**{k: v for k, v in data.items() if k in known_fields})


def save_settings(settings: Settings, path: Path | str = DEFAULT_SETTINGS_FILE) -> None:
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(settings), f, indent=2)
