"""
Audit trail for GTIN sourcing decisions - one append-only JSON Lines record
per label-generation run, covering every case: sourced straight from Label
Traxx, entered manually because Product.BC_Start was empty, or an operator
deliberately overriding a Label Traxx value with something else.

See Settings.allow_manual_gtin_override and QUESTIONS.md - this exists
because CLC is still registering GTINs into Label Traxx, so manual entry is
allowed for every run while in Beta, and every use of it needs a record.
"""

import getpass
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class GtinAuditRecord:
    timestamp: str
    username: str
    job_number: str
    packing_slip_number: str
    product_no: str
    item_number: str
    bc_start_value: str | None
    gtin_used: str
    gtin_source: str
    test_mode: bool


def build_gtin_audit_record(
    *,
    job_number: str,
    packing_slip_number: str,
    product_no: str,
    item_number: str,
    bc_start_value: str | None,
    gtin_used: str,
    gtin_source: str,
    test_mode: bool,
) -> GtinAuditRecord:
    return GtinAuditRecord(
        timestamp=datetime.now(timezone.utc).isoformat(),
        username=getpass.getuser(),
        job_number=job_number,
        packing_slip_number=packing_slip_number,
        product_no=product_no,
        item_number=item_number,
        bc_start_value=bc_start_value,
        gtin_used=gtin_used,
        gtin_source=gtin_source,
        test_mode=test_mode,
    )


def record_gtin_audit(record: GtinAuditRecord, log_file: Path | str) -> None:
    """Appends one JSON line. Creates the file (and parent dirs) if needed."""
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record)) + "\n")
