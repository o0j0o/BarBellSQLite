"""
Reading the units in a full box from a packing slip's free-text Notes. The sample notes below are real
wordings from Label Traxx (invoice numbers and all), with the real box counts and quantities of those slips.
A suggestion is made only when the notes add up to the packing slip.
"""

import pytest

from src.packing_notes import parse_box_groups, read_units_per_full_box

# (notes, packing slip quantity, NoPackage, expected units per full box)
REAL_NOTES = {
    "20 full boxes then a part box": (
        "Inv # 76140 dd 03/25/2026\r12 1/2 X 12 3/8 X 10 3/8    BOX# 25 - 44       3 ROLLS X 9000    "
        "12 X 12 X 5    BOX# 45      1 ROLL X 7000",
        547000, 21, 27000,
    ),
    "two boxes, the second a mix of two roll sizes": (
        "Inv # 76157 dd 03/27/2026\r14 1/2 X 14 3/8 X 6 3/8    BOX# 286    2 ROLLS X 7500     "
        "BOX# 287     1 ROLL X 7500 + 1 ROLL X 5000",
        27500, 2, 15000,
    ),
    "one roll per box": (
        "Inv # 75830 dd 01/27/2026 | 16 1/2 X 16 3/8 X 6 3/8    BOX# 28 - 50      1 ROLL X 9000    "
        "14 1/2 X 14 3/8 X 6 3/8   BOX# 51     1 ROLL X 7000",
        23 * 9000 + 7000, 24, 9000,
    ),
    "CRTN label and thousands commas": (
        "Inv # 75700 dd 12/31/2025 | 14 1/2 X 14 3/8 X 6 3/8     CRTN # 1 - 2      2 ROLLS X 12,000     "
        "10 X 10 X 5       CRTN # 3     1 ROLL X 5,000  PN 47387",
        2 * 24000 + 5000, 3, 24000,
    ),
    "a mixed last box that is the only partial one": (
        "Inv # 75708 dd 12/31/2025 | 12 1/2 X 12 3/8 X 10 3/8    BOX# 119  - 129      3 ROLLS X 7000    "
        "BOX# 130    2 ROLLS X 7000 + 1 ROLL X 5000",
        11 * 21000 + 19000, 12, 21000,
    ),
    "lower case and 'carton'": (
        "Inv # 75641 dd 12/19/2025   predone.................Inv # 75642 freight |  carton 7- 9  2 rolls x 5000 pn 47268 | ",
        3 * 10000, 3, 10000,
    ),
    "BOXX typo": (
        "Inv # 75708 dd 12/31/2025   predone please return | 14 1/2 X 14 3/8 X 6 3/8     BOX# 193 - 196    "
        "2 ROLLS X 5000     BOXX# 197     1 ROLL X 5000",
        4 * 10000 + 5000, 5, 10000,
    ),
    "rolls taken from stock are not a box line": (
        "Inv # 75708 dd 12/31/2025   predone please return | FROM STOCK 3 ROLLS X 9,000 JOB#121690.....ROLLS#55,56,61 .   "
        "14 1/2 X 14 3/8 X 6 3/8   CRTN#143-170   2 ROLLS X 9,000 PN 41",
        28 * 18000, 28, 18000,
    ),
}


@pytest.mark.parametrize("name", list(REAL_NOTES))
def test_real_notes_give_the_units_in_a_full_box(name):
    notes, quantity, boxes, expected = REAL_NOTES[name]
    reading = read_units_per_full_box(notes, quantity, boxes)
    assert reading.units_per_full_box == expected, reading.reason
    assert reading.reason == ""
    assert reading.full_box_text  # what it was read from, to show the operator


def test_the_box_lines_are_read_in_order_with_their_box_counts():
    groups = parse_box_groups(REAL_NOTES["20 full boxes then a part box"][0])
    assert [(g.first_box, g.last_box, g.boxes, g.units_per_box) for g in groups] == [(25, 44, 20, 27000), (45, 45, 1, 7000)]


def test_the_suggestion_is_the_fullest_box():
    # equal-sized boxes first and a smaller last one (the usual case), and the reverse order too
    notes = "BOX# 1 - 3  2 ROLLS X 5000   BOX# 4  1 ROLL X 5000"
    assert read_units_per_full_box(notes, 35000, 4).units_per_full_box == 10000
    notes = "BOX# 1  1 ROLL X 5000   BOX# 2 - 4  2 ROLLS X 5000"
    assert read_units_per_full_box(notes, 35000, 4).units_per_full_box == 10000


def test_nothing_is_suggested_when_the_notes_do_not_add_up_to_the_quantity():
    notes, quantity, boxes, _ = REAL_NOTES["20 full boxes then a part box"]
    reading = read_units_per_full_box(notes, quantity + 3000, boxes)
    assert reading.units_per_full_box is None
    assert "547,000" in reading.reason and "550,000" in reading.reason


def test_nothing_is_suggested_when_the_box_count_does_not_match_the_packing_slip():
    notes, quantity, boxes, _ = REAL_NOTES["20 full boxes then a part box"]
    reading = read_units_per_full_box(notes, quantity, boxes + 1)
    assert reading.units_per_full_box is None
    assert "21" in reading.reason and "22" in reading.reason


def test_nothing_is_suggested_for_a_slip_with_more_than_one_product():
    notes, quantity, boxes, _ = REAL_NOTES["20 full boxes then a part box"]
    reading = read_units_per_full_box(notes, quantity, boxes, product_count=2)
    assert reading.units_per_full_box is None
    assert "more than one product" in reading.reason


@pytest.mark.parametrize("notes", [None, "", "Inv # 24416  dd 10/28/05", "cancelled", "Inv. #17262  dd 30/09/03   INSIDE SAME BOX AS 30329"])
def test_notes_with_no_box_lines_suggest_nothing(notes):
    reading = read_units_per_full_box(notes, 1000, 1)
    assert reading.units_per_full_box is None and reading.groups == []


def test_a_box_range_written_backwards_is_not_trusted():
    assert read_units_per_full_box("BOX# 9 - 5  1 ROLL X 1000", 5000, 5).units_per_full_box is None


def test_the_carton_size_lines_are_not_mistaken_for_box_lines():
    assert parse_box_groups("14 1/2 X 14 3/8 X 6 3/8     12 X 12 X 5") == []
