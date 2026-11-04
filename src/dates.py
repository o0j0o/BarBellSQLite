"""
The production date: entered, stored, shown, and printed as YYMMDD (e.g. 4 Nov
2026 -> "261104") - the same form GS1 AI (11) already requires, so the string
on screen, in the database and CSV, and in the barcode is one and the same.

Two-digit years are always read as 20YY (BarBell has no use for dates outside
2000-2099), which also means plain string comparison/min() of two stored
production dates orders them correctly.

normalize_production_date() additionally accepts the old YYYY-MM-DD form -
databases written before YYMMDD became the format still hold it until the
migration in src/db/local_store.py rewrites them - so nothing that reads an
old value breaks.
"""

import datetime
import re

PRODUCTION_DATE_FORMAT = "YYMMDD"
PRODUCTION_DATE_EXAMPLE = "261104"  # 4 Nov 2026
_YYMMDD_RE = re.compile(r"\d{6}")
_LEGACY_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_production_date(text: str) -> datetime.date:
    """Strict YYMMDD -> date. Raises ValueError if it isn't exactly six
    digits forming a real calendar date."""
    if not _YYMMDD_RE.fullmatch(text):
        raise ValueError(f"{text!r} isn't a {PRODUCTION_DATE_FORMAT} date")
    return datetime.date(2000 + int(text[:2]), int(text[2:4]), int(text[4:]))


def format_production_date(d: datetime.date) -> str:
    if not 2000 <= d.year <= 2099:
        raise ValueError(f"{d} is outside the supported years 2000-2099")
    return f"{d.year % 100:02d}{d.month:02d}{d.day:02d}"


def normalize_production_date(value: str) -> str:
    """YYMMDD (or a legacy YYYY-MM-DD) -> YYMMDD. Raises ValueError for
    anything else."""
    if _LEGACY_ISO_RE.fullmatch(value):
        return format_production_date(datetime.date.fromisoformat(value))
    return format_production_date(parse_production_date(value))
