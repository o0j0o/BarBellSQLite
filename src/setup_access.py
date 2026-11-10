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

import hashlib
import hmac
import secrets
from enum import Enum


class SetupAccessLevel(Enum):
    Standard = "standard"
    Admin = "admin"


# === SETUP PASSWORDS - the only place they are defined =====================
STANDARD_SETUP_PASSWORD_DEFAULT = "change4GOOD"
ADMIN_SETUP_PASSWORD = "42Novell@1430$"
# ===========================================================================

ADMIN_WELCOME_MESSAGE = "Welcome Greg"


MIN_SETUP_PASSWORD_LENGTH = 6

# --- changing the standard setup password ----------------------------------
#
# From 1.1.17 the standard setup password can be changed from Setup. A changed
# password is never stored as typed: only a salted PBKDF2 hash goes into the
# SQLite database (src/db/local_store.py, table setup_credentials). Until it is
# changed - and again after a Reset - there is no hash and the plain default /
# Settings.setup_password applies exactly as before. The Admin password above is
# fixed and is never changed or reset by any of this.

_HASH_SCHEME = "pbkdf2_sha256"
_HASH_ITERATIONS = 200_000


def hash_setup_password(password: str) -> str:
    """A salted PBKDF2-SHA256 hash of `password`, as one storable string
    ("pbkdf2_sha256$iterations$salt$hash"). Different every call (random salt)."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _HASH_ITERATIONS)
    return f"{_HASH_SCHEME}${_HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_setup_password_hash(password: str, stored_hash: str) -> bool:
    """True if `password` matches a hash made by hash_setup_password(). A
    malformed stored value never matches (and never raises)."""
    try:
        scheme, iterations, salt_hex, digest_hex = stored_hash.split("$")
        if scheme != _HASH_SCHEME:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(digest, bytes.fromhex(digest_hex))
    except (ValueError, TypeError):
        return False


def validate_new_setup_password(new_password: str, confirmation: str) -> None:
    """Raises ValueError (with a message safe to show - it never contains the
    password) unless the new password is long enough and typed the same twice."""
    if len(new_password) < MIN_SETUP_PASSWORD_LENGTH:
        raise ValueError(
            f"The new password must be at least {MIN_SETUP_PASSWORD_LENGTH} characters long."
        )
    if new_password != confirmation:
        raise ValueError("The two passwords do not match.")


def is_admin_password(entered: str) -> bool:
    """True only for the Admin (Greg) password - what a Reset of the standard
    setup password has to be unlocked with."""
    return hmac.compare_digest(entered.encode("utf-8"), ADMIN_SETUP_PASSWORD.encode("utf-8"))


def resolve_setup_access(
    entered: str, standard_password: str, standard_password_hash: str | None = None
) -> SetupAccessLevel | None:
    """
    The access level `entered` grants, or None if it matches neither
    password. standard_password is the configured one (Settings.setup_password,
    defaulting to STANDARD_SETUP_PASSWORD_DEFAULT) - the standard check is the
    same plain comparison it has always been. If standard_password_hash is
    given (the password was changed in Setup), that hash is checked INSTEAD of
    standard_password, which is then ignored.
    """
    if standard_password_hash:
        standard_ok = verify_setup_password_hash(entered, standard_password_hash)
    else:
        standard_ok = entered == standard_password
    if standard_ok:
        return SetupAccessLevel.Standard
    if is_admin_password(entered):
        return SetupAccessLevel.Admin
    return None
