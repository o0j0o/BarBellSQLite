"""
Reading "how many units go in a full box" from a Label Traxx packing slip's Notes.

The packers type the box contents into PackingSlip.Notes as free text, for example (job 122984):

    Inv # 76140 dd 03/25/2026
    12 1/2 X 12 3/8 X 10 3/8   BOX# 25 - 44   3 ROLLS X 9000    12 X 12 X 5   BOX# 45   1 ROLL X 7000

that is boxes 25 to 44 (20 boxes) each holding 3 rolls of 9000 = 27,000, then box 45 holding 7,000. The
wording varies (BOX#, BOXX#, CRTN#, "carton 7- 9"; "10,000"; "1 ROLL X 8000 + 1 ROLL X 6000" for a mixed
box), so only the box lines are read - a box label, a box number or range, then "<n> ROLL(S) X <qty>" -
and anything else (invoice numbers, carton sizes, "FROM STOCK ...", "predone") is ignored.

A reading is only trusted when it ADDS UP to the packing slip: the box lines must cover exactly the
packing slip's NoPackage boxes and exactly its total ShipQuantity, and the slip must carry a single
product (with several products the notes do not say which box is which in any way we can rely on). If it
does not add up, nothing is suggested and the operator types the number as before. The suggestion is the
fullest box listed, which is what BarBell's equal packages (plus a smaller last one) reproduce.
"""

import re
from dataclasses import dataclass

_ROLL = r"\d+\s*ROLLS?\s*X\s*\d[\d,]*"
_BOX_LINE_RE = re.compile(
    rf"(?<![A-Z])(?:BOXX?|CRTN|CARTON|CTN)\s*#?\s*(\d+)(?:\s*-\s*(\d+))?\s+((?:{_ROLL})(?:\s*\+\s*(?:{_ROLL}))*)"
)
_ROLL_RE = re.compile(r"(\d+)\s*ROLLS?\s*X\s*(\d[\d,]*)")


@dataclass
class BoxGroup:
    first_box: int
    last_box: int
    units_per_box: int
    text: str  # the notes text this was read from, tidied - shown to the operator

    @property
    def boxes(self) -> int:
        return self.last_box - self.first_box + 1


@dataclass
class NotesReading:
    units_per_full_box: int | None  # None = nothing trusted to suggest
    groups: list[BoxGroup]
    full_box_text: str = ""  # the notes line the suggestion came from
    reason: str = ""  # why there is no suggestion (empty when there is one)


def parse_box_groups(notes: str | None) -> list[BoxGroup]:
    """Every box line found in the notes, in the order written."""
    if not notes:
        return []
    text = " ".join(str(notes).upper().split())  # one line, single spaces, upper case
    groups = []
    for match in _BOX_LINE_RE.finditer(text):
        first = int(match.group(1))
        last = int(match.group(2)) if match.group(2) else first
        units = sum(int(n) * int(q.replace(",", "")) for n, q in _ROLL_RE.findall(match.group(3)))
        groups.append(BoxGroup(first, last, units, " ".join(match.group(0).split())))
    return groups


def read_units_per_full_box(
    notes: str | None, ship_quantity: int, no_package: int | None, product_count: int = 1
) -> NotesReading:
    """The units in a full box according to `notes`, or no suggestion (with the reason) unless the notes
    add up to the packing slip - see the module docstring. `ship_quantity` and `no_package` are the packing
    slip's totals; `product_count` is how many products the slip carries."""
    groups = parse_box_groups(notes)
    if not groups:
        return NotesReading(None, [], reason="No box lines found in the packing slip notes.")
    if product_count != 1:
        return NotesReading(None, groups, reason="The packing slip carries more than one product.")
    if any(g.last_box < g.first_box or g.units_per_box <= 0 for g in groups):
        return NotesReading(None, groups, reason="A box line in the notes could not be understood.")

    total_boxes = sum(g.boxes for g in groups)
    total_units = sum(g.boxes * g.units_per_box for g in groups)
    if no_package is not None and total_boxes != int(no_package):
        return NotesReading(
            None, groups, reason=f"The notes list {total_boxes} box(es) but the packing slip says {int(no_package)}."
        )
    if total_units != int(ship_quantity):
        return NotesReading(
            None, groups,
            reason=f"The notes add up to {total_units:,} units but the packing slip ships {int(ship_quantity):,}.",
        )

    fullest = max(groups, key=lambda g: g.units_per_box)
    return NotesReading(fullest.units_per_box, groups, full_box_text=fullest.text)
