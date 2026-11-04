"""
Setup form layout: the whole form must be reachable by scrolling, Save
Settings must stay visible, and the explanatory notes must use the form's
full width. Setup is its own Tk window, so this runs in a subprocess against
a TEMP settings file (see test_setup_gui_backup.py for why).
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DRIVER = r'''
import json, sys
from pathlib import Path

root, tmp = sys.argv[1], Path(sys.argv[2])
sys.path.insert(0, root)

import setup_gui
from src import settings as sm
from src.setup_access import SetupAccessLevel

settings_path = tmp / "settings.json"
sm.save_settings(sm.Settings(gs1_company_prefix="08600157112", output_dir="output"), settings_path)
setup_gui.load_settings = lambda path=settings_path: sm.load_settings(settings_path)

gui = setup_gui.SetupGUI(SetupAccessLevel.Admin)
gui.update()
out = {}

# --- as opened: fits the screen, notes span the form --------------------------
out["screen_height"] = gui.winfo_screenheight()
out["window_height"] = gui.winfo_height()
out["body_width"] = gui.body.winfo_width()

notes = []
def walk(w):
    for c in w.winfo_children():
        if c.winfo_class() == "TLabel" and len(str(c.cget("text"))) > 150:
            notes.append({"wrap": int(str(c.cget("wraplength"))), "chars": len(str(c.cget("text"))),
                          "lines_estimate": c.winfo_height()})
        walk(c)
walk(gui.body)
out["notes"] = notes

# --- squeezed into a short window (a laptop screen): can we reach the bottom? ----
gui.geometry("1000x480+0+0")
gui.update()
out["scrollable_when_short"] = gui._canvas.yview() != (0.0, 1.0)
out["scrollbar_mapped"] = bool(gui._scrollbar.winfo_ismapped())
gui._canvas.yview_moveto(1.0)
gui.update()
out["yview_at_end"] = list(gui._canvas.yview())
canvas_bottom = gui._canvas.winfo_rooty() + gui._canvas.winfo_height()
restore_bottom = gui.restore_button.winfo_rooty() + gui.restore_button.winfo_height()
out["last_widget_visible_after_scroll"] = restore_bottom <= canvas_bottom + 1
window_bottom = gui.winfo_rooty() + gui.winfo_height()
save = [b for b in gui._button_bar.winfo_children() if b.cget("text") == "Save Settings"][0]
out["save_button_visible"] = bool(save.winfo_viewable()) and (
    save.winfo_rooty() + save.winfo_height() <= window_bottom + 1
)

# --- the mouse wheel scrolls too ---------------------------------------------------------
gui._canvas.yview_moveto(0.0)
gui.update()
class E: delta = -120
gui._on_mousewheel(E)
gui.update()
out["wheel_moved"] = gui._canvas.yview()[0] > 0.0

print("RESULT " + json.dumps(out))
'''


def run():
    with tempfile.TemporaryDirectory() as tmp:
        proc = subprocess.run(
            [sys.executable, "-c", DRIVER, str(ROOT), tmp], capture_output=True, text=True, timeout=120
        )
    lines = [l for l in proc.stdout.splitlines() if l.startswith("RESULT ")]
    assert lines, f"driver failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    return json.loads(lines[-1][len("RESULT "):])


def test_form_opens_within_the_screen_height():
    result = run()
    assert result["window_height"] <= result["screen_height"] - 60


def test_a_short_window_scrolls_all_the_way_to_the_last_section():
    result = run()
    assert result["scrollable_when_short"] is True
    assert result["scrollbar_mapped"] is True
    assert result["yview_at_end"][1] == 1.0
    assert result["last_widget_visible_after_scroll"] is True


def test_save_settings_stays_visible_however_far_the_form_is_scrolled():
    assert run()["save_button_visible"] is True


def test_the_mouse_wheel_scrolls_the_form():
    assert run()["wheel_moved"] is True


def test_notes_span_the_form_instead_of_a_narrow_column():
    result = run()
    assert len(result["notes"]) >= 4  # plant, demo, disable-test-mode, backup
    for note in result["notes"]:
        # wraps at (almost) the full section width, not the old hand-broken ~450px column
        assert note["wrap"] >= 0.8 * result["body_width"], note
