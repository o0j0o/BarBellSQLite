"""
Setup access levels and the two passwords that grant them.

This is the ONE place the setup passwords live - nothing else in the code
base spells either of them out. Neither is ever logged, printed, or put in
an error message (a wrong password gets the same generic message regardless
of what was typed).

  - Standard: the regular setup password. It's stored in settings.json
    (Settings.setup_password) like it always has been, so it can still be
    changed there; the value below is just the default a fresh install
    starts with.
  - Admin: a second, fixed password that gets the same Setup access plus a
    "Welcome Greg" greeting from the main window. Setup is told which level
    was used (SetupAccessLevel) so it can offer admin-only features later;
    for now both levels get identical Setup functionality.

This is a soft deterrent, not real security - see QUESTIONS.md item on the
setup password.
"""

import hmac
from enum import Enum


class SetupAccessLevel(Enum):
    Standard = "standard"
    Admin = "admin"


# === SETUP PASSWORDS - the only place they are defined =====================
STANDARD_SETUP_PASSWORD_DEFAULT = "change4GOOD"
ADMIN_SETUP_PASSWORD = "42Novell@1430$"
# ===========================================================================

ADMIN_WELCOME_MESSAGE = "Welcome Greg"


def resolve_setup_access(entered: str, standard_password: str) -> SetupAccessLevel | None:
    """
    The access level `entered` grants, or None if it matches neither
    password. standard_password is the configured one (Settings.setup_password,
    defaulting to STANDARD_SETUP_PASSWORD_DEFAULT) - the standard check is the
    same plain comparison it has always been.
    """
    if entered == standard_password:
        return SetupAccessLevel.Standard
    if hmac.compare_digest(entered.encode("utf-8"), ADMIN_SETUP_PASSWORD.encode("utf-8")):
        return SetupAccessLevel.Admin
    return None
