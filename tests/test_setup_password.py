"""
1.1.17: the standard Setup password can be changed from Setup (stored hashed in
SQLite, at least 6 characters, confirmed twice, viewable with the eye icon) and
reset to the default - the reset only after the Admin (Greg) password. The Admin
password never changes.

Setup is its own Tk window, so the GUI scenarios run in a subprocess against a
TEMP settings file and a TEMP database (same approach as test_setup_gui_backup.py).
"""

import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from src.db.local_store import (
    clear_setup_password_hash,
    get_setup_password_hash,
    set_setup_password_hash,
)
from src.setup_access import (
    ADMIN_SETUP_PASSWORD,
    MIN_SETUP_PASSWORD_LENGTH,
    SetupAccessLevel,
    hash_setup_password,
    is_admin_password,
    resolve_setup_access,
    validate_new_setup_password,
    verify_setup_password_hash,
)

ROOT = Path(__file__).resolve().parent.parent


def test_hash_verifies_and_is_salted():
    first, second = hash_setup_password("secret1"), hash_setup_password("secret1")
    assert first != second  # random salt
    assert verify_setup_password_hash("secret1", first)
    assert verify_setup_password_hash("secret1", second)
    assert not verify_setup_password_hash("Secret1", first)
    assert "secret1" not in first


@pytest.mark.parametrize("bad", ["", "nonsense", "a$b$c$d", "pbkdf2_sha256$x$zz$zz", "md5$1$00$00"])
def test_a_malformed_stored_hash_never_matches_and_never_raises(bad):
    assert verify_setup_password_hash("anything", bad) is False


def test_new_password_rules():
    validate_new_setup_password("abcdef", "abcdef")  # exactly the minimum is fine
    with pytest.raises(ValueError, match="at least 6"):
        validate_new_setup_password("abcde", "abcde")
    with pytest.raises(ValueError, match="do not match"):
        validate_new_setup_password("abcdef", "abcdeg")
    assert MIN_SETUP_PASSWORD_LENGTH == 6


def test_a_changed_password_replaces_the_default_and_admin_is_unaffected():
    stored = hash_setup_password("newpass1")
    assert resolve_setup_access("newpass1", "change4GOOD", stored) is SetupAccessLevel.Standard
    assert resolve_setup_access("change4GOOD", "change4GOOD", stored) is None  # old one is gone
    assert resolve_setup_access(ADMIN_SETUP_PASSWORD, "change4GOOD", stored) is SetupAccessLevel.Admin
    assert is_admin_password(ADMIN_SETUP_PASSWORD)
    assert not is_admin_password("change4GOOD")


def test_no_stored_hash_behaves_exactly_as_before():
    assert resolve_setup_access("change4GOOD", "change4GOOD", None) is SetupAccessLevel.Standard
    assert resolve_setup_access("change4GOOD", "change4GOOD", "") is SetupAccessLevel.Standard


def test_hash_persists_in_sqlite_never_as_plain_text(tmp_path):
    db = tmp_path / "barbell.db"
    assert get_setup_password_hash(db) is None
    set_setup_password_hash(hash_setup_password("PlainTextCheck9"), db)
    stored = get_setup_password_hash(db)  # a fresh connection: it survived a "restart"
    assert verify_setup_password_hash("PlainTextCheck9", stored)

    set_setup_password_hash(hash_setup_password("second-one"), db)  # changing again replaces it
    assert verify_setup_password_hash("second-one", get_setup_password_hash(db))
    assert not verify_setup_password_hash("PlainTextCheck9", get_setup_password_hash(db))

    raw = db.read_bytes()
    assert b"PlainTextCheck9" not in raw and b"second-one" not in raw
    with sqlite3.connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM setup_credentials").fetchone()[0] == 1

    clear_setup_password_hash(db)
    assert get_setup_password_hash(db) is None


DRIVER = r'''
import json, sys
from pathlib import Path

root, tmp = sys.argv[1], Path(sys.argv[2])
sys.path.insert(0, root)

import tkinter.messagebox as mb
import tkinter.simpledialog as sd

log = {"info": [], "error": [], "ask": []}
answers = {"yesno": True, "string": None}
mb.showinfo = lambda t, m, **k: log["info"].append(m)
mb.showerror = lambda t, m, **k: log["error"].append(m)
mb.askyesno = lambda t, m, **k: (log["ask"].append(t), answers["yesno"])[1]
sd.askstring = lambda *a, **k: answers["string"]

import setup_gui
from src import settings as sm
from src.db.local_store import get_setup_password_hash
from src.setup_access import ADMIN_SETUP_PASSWORD, SetupAccessLevel, resolve_setup_access

settings_path = tmp / "settings.json"
db = str(tmp / "barbell.db")
sm.save_settings(sm.Settings(local_db_file=db, output_dir=str(tmp / "out")), settings_path)
setup_gui.load_settings = lambda path=settings_path: sm.load_settings(settings_path)
setup_gui.save_settings = lambda s, path=settings_path: sm.save_settings(s, settings_path)

def access(entered):
    return resolve_setup_access(entered, sm.load_settings(settings_path).setup_password, get_setup_password_hash(db))

def fresh(level):
    log["info"].clear(); log["error"].clear()
    return setup_gui.SetupGUI(level)

out = {}
gui = fresh(SetupAccessLevel.Standard)
gui.update()

# eye icon: the box starts hidden, one click shows it, another hides it again
entry = gui.new_password_entry
out["starts_hidden"] = entry.cget("show") == "*"
entry.eye_button.invoke()
out["shown_after_click"] = entry.cget("show") == ""
entry.eye_button.invoke()
out["hidden_again"] = entry.cget("show") == "*"
out["both_boxes_have_an_eye"] = bool(gui.confirm_password_entry.eye_button)

# too short, then mismatch: nothing is saved
gui.new_password_var.set("abc"); gui.confirm_password_var.set("abc")
gui._change_setup_password()
out["short_error"] = list(log["error"]); log["error"].clear()
gui.new_password_var.set("abcdef"); gui.confirm_password_var.set("abcdeg")
gui._change_setup_password()
out["mismatch_error"] = list(log["error"]); log["error"].clear()
out["nothing_saved_yet"] = get_setup_password_hash(db) is None

# a good change
gui.new_password_var.set("Fresh-pass1"); gui.confirm_password_var.set("Fresh-pass1")
gui._change_setup_password()
out["changed_message"] = list(log["info"])
out["boxes_cleared"] = gui.new_password_var.get() == "" and gui.confirm_password_var.get() == ""
out["new_works"] = access("Fresh-pass1") is not None and access("Fresh-pass1").value == "standard"
out["old_default_rejected"] = access("change4GOOD") is None
out["greg_unchanged"] = access(ADMIN_SETUP_PASSWORD) is SetupAccessLevel.Admin
out["json_has_no_new_password"] = "Fresh-pass1" not in settings_path.read_text()

# reset as a Standard user: needs the Admin password
log["info"].clear(); log["error"].clear()
answers["string"] = "not-the-admin-password"
gui._reset_setup_password()
out["wrong_admin_error"] = list(log["error"])
out["still_changed_after_wrong"] = access("Fresh-pass1") is not None

answers["string"] = None  # cancelled
gui._reset_setup_password()
out["still_changed_after_cancel"] = access("Fresh-pass1") is not None

answers["string"] = ADMIN_SETUP_PASSWORD
gui._reset_setup_password()
out["reset_message"] = list(log["info"])
out["default_back"] = access("change4GOOD") is not None and access("change4GOOD").value == "standard"
out["changed_one_gone"] = access("Fresh-pass1") is None
out["greg_unchanged_after_reset"] = access(ADMIN_SETUP_PASSWORD) is SetupAccessLevel.Admin
gui.destroy()

# reset when Setup was already opened with the Admin password: no password prompt, just a confirm
gui = fresh(SetupAccessLevel.Admin)
gui.update()
gui.new_password_var.set("Another-1"); gui.confirm_password_var.set("Another-1")
gui._change_setup_password()
out["admin_can_change_too"] = access("Another-1") is not None
answers["string"] = "would-fail-if-asked"
answers["yesno"] = False
gui._reset_setup_password()
out["admin_declined_confirm_keeps_password"] = access("Another-1") is not None
answers["yesno"] = True
gui._reset_setup_password()
out["admin_reset_without_prompt"] = access("change4GOOD") is not None
gui.destroy()
print("RESULT" + json.dumps(out))
'''


@pytest.fixture(scope="module")
def result(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("setup_pw")
    proc = subprocess.run(
        [sys.executable, "-c", DRIVER, str(ROOT), str(tmp)],
        capture_output=True, text=True, timeout=120, cwd=str(tmp),
    )
    assert proc.returncode == 0, proc.stderr
    line = [l for l in proc.stdout.splitlines() if l.startswith("RESULT")][-1]
    return json.loads(line[len("RESULT"):])


def test_eye_icon_shows_and_hides_both_boxes(result):
    assert result["starts_hidden"] and result["shown_after_click"] and result["hidden_again"]
    assert result["both_boxes_have_an_eye"]


def test_too_short_and_mismatched_passwords_are_refused(result):
    assert "at least 6" in result["short_error"][0]
    assert "do not match" in result["mismatch_error"][0]
    assert result["nothing_saved_yet"]


def test_changing_the_password_works_and_leaves_greg_alone(result):
    assert result["changed_message"] == ["The Setup password has been changed."]
    assert result["boxes_cleared"] and result["new_works"] and result["old_default_rejected"]
    assert result["greg_unchanged"] and result["json_has_no_new_password"]


def test_reset_needs_the_admin_password_then_restores_the_default(result):
    assert result["wrong_admin_error"] == ["That password is incorrect."]
    assert result["still_changed_after_wrong"] and result["still_changed_after_cancel"]
    assert result["reset_message"] == ["The Setup password has been reset to the default."]
    assert result["default_back"] and result["changed_one_gone"] and result["greg_unchanged_after_reset"]


def test_when_setup_was_opened_as_admin_reset_only_asks_for_confirmation(result):
    assert result["admin_can_change_too"]
    assert result["admin_declined_confirm_keeps_password"]
    assert result["admin_reset_without_prompt"]
