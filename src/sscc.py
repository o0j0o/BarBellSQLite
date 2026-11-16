"""
SSCC (Serial Shipping Container Code) generation for GS1-128 pallet/carton labels.

Structure (18 digits total): extension digit (1) + GS1 Company Prefix (N) +
serial reference (16-N) + check digit (1). CLC's GS1 Company Prefix is
'08600157112' (see the GS1 Company Prefix Certificate, Account 30391419).

An SSCC must NEVER be reused once issued - that's a hard GS1 requirement, not
a style preference (a duplicate gets a shipment rejected at JWN's warehouse).
SSCCGenerator enforces this by persisting the last-issued serial reference to
a state file and refusing to ever move it backwards.

Scope (2026-09): single plant, single process. This does not coordinate
across multiple CLC plants or multiple concurrent processes writing the same
state file - see QUESTIONS.md.
"""

import datetime
import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

SSCC_LENGTH = 18


# A TEST SSCC is a real-shaped 18-digit SSCC - so its barcode really encodes, the scanner accepts it and
# BarTender's GS1-128 object treats it like any other - but it starts with seven zeros. A real SSCC starts
# with the extension digit and the GS1 Company Prefix (CLC's is 008600157112...), so the two can never
# meet. Layout: 7 zeros + a 10-digit test serial + the GS1 check digit.
TEST_SSCC_LEAD = "0" * 7
TEST_SERIAL_WIDTH = 10
MAX_TEST_SERIAL = 10**TEST_SERIAL_WIDTH - 1


def build_test_sscc(serial: int) -> str:
    """
    The TEST SSCC for test serial number `serial` (1, 2, 3...): seven zeros, the serial padded to 10
    digits, and a correct GS1 check digit - e.g. serial 17 -> 000000000000000178. Test serials are one
    running count shared by test cartons and test pallets and are worked out from the database (see
    src.db.local_store.next_test_serial), so no two test labels ever share a number. It never touches the
    real SSCC counter/state file - there is nothing to "waste" or "recover" using this.
    """
    if not 1 <= serial <= MAX_TEST_SERIAL:
        raise ValueError(f"Test serial must be between 1 and {MAX_TEST_SERIAL}, got {serial!r}")
    body = f"{TEST_SSCC_LEAD}{serial:0{TEST_SERIAL_WIDTH}d}"
    return body + gs1_check_digit(body)


def is_test_sscc(sscc: str) -> bool:
    """True for an SSCC made by build_test_sscc(): 18 digits that start with the seven-zero test lead."""
    return len(sscc) == SSCC_LENGTH and sscc.isdigit() and sscc.startswith(TEST_SSCC_LEAD)


def _atomic_write_last_serial(state_file: Path, value: int) -> None:
    # Write to a temp file in the same directory, then atomically replace -
    # avoids a half-written state file if the process dies mid-write.
    fd, tmp_path = tempfile.mkstemp(dir=state_file.parent or ".", prefix=state_file.name + ".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"last_serial": value}, f)
        os.replace(tmp_path, state_file)
    except BaseException:
        os.unlink(tmp_path)
        raise


def gs1_check_digit(digits: str) -> str:
    """Standard GS1 mod-10 check digit: weight 3/1 alternating from the rightmost digit."""
    total = 0
    weight = 3
    for d in reversed(digits):
        total += int(d) * weight
        weight = 1 if weight == 3 else 3
    return str((10 - (total % 10)) % 10)


def serial_reference_width(company_prefix: str) -> int:
    """Digits available for the serial reference, given the company prefix length."""
    width = 16 - len(company_prefix)
    if width < 1:
        raise ValueError(f"Company prefix {company_prefix!r} leaves no room for a serial reference")
    return width


def build_sscc(company_prefix: str, extension_digit: str, serial_reference: int) -> str:
    if not company_prefix.isdigit():
        raise ValueError(f"Company prefix must be all digits, got {company_prefix!r}")
    if not (extension_digit.isdigit() and len(extension_digit) == 1):
        raise ValueError(f"Extension digit must be a single digit, got {extension_digit!r}")

    width = serial_reference_width(company_prefix)
    max_serial = 10**width - 1
    if not (0 <= serial_reference <= max_serial):
        raise ValueError(
            f"Serial reference {serial_reference} out of range for a {width}-digit field "
            f"(max {max_serial}) with company prefix {company_prefix!r}"
        )

    base17 = extension_digit + company_prefix + str(serial_reference).zfill(width)
    sscc = base17 + gs1_check_digit(base17)
    assert len(sscc) == SSCC_LENGTH
    return sscc


class SSCCGenerator:
    """
    Issues sequential SSCCs backed by a durable, never-reused serial reference
    counter in a local JSON state file.

    The state file must be initialized explicitly with `initialize()` before
    `next_sscc()` will work - there is no silent "start at zero" if the file
    is missing, since that could reissue an already-used number after the
    state file is lost or moved to a fresh machine.
    """

    def __init__(self, company_prefix: str, extension_digit: str, state_file: Path):
        self.company_prefix = company_prefix
        self.extension_digit = extension_digit
        self.state_file = Path(state_file)

    def _read_last_serial(self) -> int:
        if not self.state_file.exists():
            raise FileNotFoundError(
                f"{self.state_file} does not exist - call initialize() once, explicitly, "
                "before issuing SSCCs (never let this start at 0 implicitly)."
            )
        with open(self.state_file, encoding="utf-8") as f:
            return json.load(f)["last_serial"]

    def _write_last_serial(self, value: int) -> None:
        _atomic_write_last_serial(self.state_file, value)

    def initialize(self, start_at: int = 0) -> None:
        """Create the state file. Refuses if it already exists - use next_sscc() instead."""
        if self.state_file.exists():
            raise FileExistsError(
                f"{self.state_file} already exists - refusing to reinitialize an "
                "existing SSCC counter (that risks reissuing numbers)."
            )
        self._write_last_serial(start_at - 1)  # next_sscc() will advance to start_at

    def next_sscc(self) -> str:
        last_serial = self._read_last_serial()
        next_serial = last_serial + 1
        sscc = build_sscc(self.company_prefix, self.extension_digit, next_serial)
        self._write_last_serial(next_serial)
        return sscc


@dataclass
class CounterStatus:
    initialized: bool
    last_serial: int | None  # None if never initialized
    next_serial: int | None  # None if never initialized


def get_counter_status(state_file: Path | str) -> CounterStatus:
    """Read-only status for display in the setup GUI - never issues a number."""
    state_file = Path(state_file)
    if not state_file.exists():
        return CounterStatus(initialized=False, last_serial=None, next_serial=None)
    with open(state_file, encoding="utf-8") as f:
        last_serial = json.load(f)["last_serial"]
    return CounterStatus(initialized=True, last_serial=last_serial, next_serial=last_serial + 1)


def archive_and_reset_state_file(state_file: Path | str, start_at: int) -> Path:
    """
    DANGER: moves the existing counter state aside (timestamped, not deleted)
    and starts a fresh one at `start_at`. This does NOT protect against SSCC
    reuse on its own - only call it with explicit, deliberate user
    confirmation (see setup_gui.py), and only when you're certain nothing
    already issued under the current company prefix + extension digit
    overlaps the new range.
    """
    state_file = Path(state_file)
    if not state_file.exists():
        raise FileNotFoundError(f"{state_file} does not exist - use initialize() instead")

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = state_file.with_name(f"{state_file.stem}.archived-{timestamp}{state_file.suffix}")
    state_file.rename(archive_path)
    _atomic_write_last_serial(state_file, start_at - 1)
    return archive_path
