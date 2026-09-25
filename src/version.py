"""
Single source of truth for BarBell's version - import from here everywhere
it's displayed (About dialog, CHANGELOG.md, etc.). Never hardcode the version
string, build date, or beta flag anywhere else.

Versioning rules (MAJOR.MINOR.PATCH):
  - 2026-09-14 (Greg's instruction): version reset to 1.0.0 Beta to mark the
    start of the SQLite-backed rewrite. The pre-reset history (0.1.0-0.1.4
    Beta) is preserved as-is in git and tagged `BarBellSQLite`.
  - 2026-09-25 (Greg's instruction): MINOR bumped to 1.1.0 Beta (not the next
    1.0.x) for the Pallet Labels feature - explicitly called out as a major
    addition, not a routine PATCH-level change, even though BETA is still
    True. Built on branch `pallet-labels`, not merged to `main`.
  - While BETA is True: PATCH increments by one for every change, of any
    kind - e.g. 1.1.1 Beta, 1.1.2 Beta, etc. A MINOR bump like the one above
    is Greg's call, same as MAJOR - not something to do on your own
    initiative just because a change is large.
  - Greg decides when to drop BETA (to a plain MAJOR.MINOR.PATCH release,
    starting from whatever MAJOR.MINOR it's at when he does) - never do this
    on your own initiative.
  - Once BETA is False: PATCH increments for cosmetic/non-functional changes
    (styling, wording, layout). MINOR increments (PATCH resets to 0) for
    functional changes (a new button, a new input field, a new calculation,
    a change in behaviour). MAJOR only changes on Greg's instruction.
  - A commit with both a cosmetic and a functional change bumps MINOR (the
    functional change wins).

See CHANGELOG.md for the history behind each bump.
"""

MAJOR = 1
MINOR = 1
PATCH = 1
BETA = True

BUILD_DATE = "2026-09-25"  # date of the most recent change


def version_string() -> str:
    base = f"{MAJOR}.{MINOR}.{PATCH}"
    return f"{base} Beta" if BETA else base
