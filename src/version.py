"""
Single source of truth for BarBell's version - import from here everywhere
it's displayed (About dialog, CHANGELOG.md, etc.). Never hardcode the version
string, build date, or beta flag anywhere else.

Versioning rules (MAJOR.MINOR.PATCH):
  - Starting value: 0.1.0 Beta.
  - BUILD_DATE updates to the date of every change, of any kind.
  - While BETA is True: PATCH increments by one for every change, of any kind.
  - Greg decides when to drop BETA and move to 1.0.0 - never do this on your
    own initiative.
  - Once BETA is False: PATCH increments for cosmetic/non-functional changes
    (styling, wording, layout). MINOR increments (PATCH resets to 0) for
    functional changes (a new button, a new input field, a new calculation,
    a change in behaviour). MAJOR only changes on Greg's instruction.
  - A commit with both a cosmetic and a functional change bumps MINOR (the
    functional change wins).

See CHANGELOG.md for the history behind each bump.
"""

MAJOR = 0
MINOR = 1
PATCH = 0
BETA = True

BUILD_DATE = "2026-09-10"  # date of the most recent change


def version_string() -> str:
    base = f"{MAJOR}.{MINOR}.{PATCH}"
    return f"{base} Beta" if BETA else base
