"""
BarBell setup GUI: edits settings.json (CSV output directory, GS1 Company
Prefix, SSCC extension digit, counter file location) and shows/manages the
SSCC counter status.

Settings here are separate from .env, which holds only the Label Traxx
connection credentials - not meant to be hand-edited through a GUI.

The SSCC starting serial number is the one field that's dangerous to change
casually: setting it is only offered while the counter has never been
initialized, and re-initializing an already-issued counter ("Reset") requires
typing a literal confirmation and archives (never deletes) the old counter
file - see src/sscc.py's initialize()/archive_and_reset_state_file().

Run with:
    python setup_gui.py
"""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.settings import Settings, load_settings, save_settings
from src.sscc import (
    SSCCGenerator,
    archive_and_reset_state_file,
    get_counter_status,
    serial_reference_width,
)

APP_ROOT = Path(__file__).resolve().parent


def validate_company_prefix(raw: str) -> str:
    prefix = raw.strip()
    if not prefix.isdigit():
        raise ValueError(f"GS1 Company Prefix must be all digits, got {raw!r}")
    serial_reference_width(prefix)  # raises ValueError if too long to leave any serial digits
    return prefix


def validate_extension_digit(raw: str) -> str:
    digit = raw.strip()
    if not (digit.isdigit() and len(digit) == 1):
        raise ValueError(f"SSCC extension digit must be a single digit (0-9), got {raw!r}")
    return digit


class SetupGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BarBell Setup")
        self.resizable(False, False)

        self.settings = load_settings()

        self._build_output_section()
        self._build_gs1_section()
        self._build_counter_section()
        self._build_buttons()

        self._refresh_counter_status()

    # --- widget layout -----------------------------------------------------

    def _build_output_section(self):
        frame = ttk.LabelFrame(self, text="Label Output", padding=10)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="CSV output directory:").grid(row=0, column=0, sticky="w")
        self.output_dir_var = tk.StringVar(value=self.settings.output_dir)
        ttk.Entry(frame, textvariable=self.output_dir_var, width=45).grid(
            row=0, column=1, sticky="ew", padx=5
        )
        ttk.Button(frame, text="Browse...", command=self._browse_output_dir).grid(row=0, column=2)

    def _build_gs1_section(self):
        frame = ttk.LabelFrame(self, text="GS1 / SSCC Configuration", padding=10)
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="GS1 Company Prefix:").grid(row=0, column=0, sticky="w")
        self.company_prefix_var = tk.StringVar(value=self.settings.gs1_company_prefix)
        ttk.Entry(frame, textvariable=self.company_prefix_var, width=20).grid(
            row=0, column=1, sticky="w", padx=5
        )
        ttk.Label(
            frame, text="(can differ per plant - see the GS1 Company Prefix Certificate)"
        ).grid(row=0, column=2, sticky="w")

        ttk.Label(frame, text="SSCC extension digit:").grid(row=1, column=0, sticky="w")
        self.extension_digit_var = tk.StringVar(value=self.settings.sscc_extension_digit)
        ttk.Entry(frame, textvariable=self.extension_digit_var, width=5).grid(
            row=1, column=1, sticky="w", padx=5
        )

        ttk.Label(frame, text="SSCC counter file:").grid(row=2, column=0, sticky="w")
        self.state_file_var = tk.StringVar(value=self.settings.sscc_state_file)
        ttk.Entry(frame, textvariable=self.state_file_var, width=45).grid(
            row=2, column=1, sticky="ew", padx=5
        )
        ttk.Button(frame, text="Browse...", command=self._browse_state_file).grid(row=2, column=2)

    def _build_counter_section(self):
        frame = ttk.LabelFrame(self, text="SSCC Counter Status", padding=10)
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        frame.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(frame, text="")
        self.status_label.grid(row=0, column=0, columnspan=3, sticky="w")

        ttk.Label(frame, text="Starting serial number:").grid(row=1, column=0, sticky="w")
        self.start_at_var = tk.StringVar(value="0")
        self.start_at_entry = ttk.Entry(frame, textvariable=self.start_at_var, width=10)
        self.start_at_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.init_button = ttk.Button(
            frame, text="Initialize Counter", command=self._initialize_counter
        )
        self.init_button.grid(row=1, column=2, sticky="w")

        self.reset_button = ttk.Button(
            frame, text="Reset Counter (danger)", command=self._reset_counter
        )
        self.reset_button.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8, 0))

    def _build_buttons(self):
        frame = ttk.Frame(self, padding=10)
        frame.grid(row=3, column=0, sticky="ew")
        ttk.Button(frame, text="Save Settings", command=self._save).pack(side="right")

    # --- actions -------------------------------------------------------

    def _browse_output_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.output_dir_var.get() or str(APP_ROOT))
        if chosen:
            self.output_dir_var.set(chosen)

    def _browse_state_file(self):
        chosen = filedialog.asksaveasfilename(
            initialdir=str(APP_ROOT),
            initialfile="sscc_state.json",
            defaultextension=".json",
        )
        if chosen:
            self.state_file_var.set(chosen)

    def _refresh_counter_status(self):
        status = get_counter_status(self.state_file_var.get())
        if status.initialized:
            self.status_label.config(
                text=f"Initialized - last issued serial {status.last_serial}, "
                f"next will be {status.next_serial}."
            )
            self.start_at_entry.config(state="disabled")
            self.init_button.config(state="disabled")
            self.reset_button.config(state="normal")
        else:
            self.status_label.config(text="Not yet initialized - no SSCCs have been issued.")
            self.start_at_entry.config(state="normal")
            self.init_button.config(state="normal")
            self.reset_button.config(state="disabled")

    def _initialize_counter(self):
        try:
            start_at = int(self.start_at_var.get())
            if start_at < 0:
                raise ValueError("Starting serial number can't be negative.")
        except ValueError as exc:
            messagebox.showerror("Invalid starting serial", str(exc))
            return

        state_file = Path(self.state_file_var.get())
        state_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            SSCCGenerator(
                self.company_prefix_var.get().strip(),
                self.extension_digit_var.get().strip(),
                state_file,
            ).initialize(start_at=start_at)
        except FileExistsError as exc:
            messagebox.showerror("Already initialized", str(exc))
            return

        messagebox.showinfo("Counter initialized", f"SSCC counter will start at serial {start_at}.")
        self._refresh_counter_status()

    def _reset_counter(self):
        confirm_win = tk.Toplevel(self)
        confirm_win.title("Confirm reset")
        confirm_win.resizable(False, False)

        ttk.Label(
            confirm_win,
            text=(
                "This starts a brand new SSCC counter. The old counter file is\n"
                "archived, not deleted, but any SSCCs already issued are NOT\n"
                "tracked against the new starting number - only do this if you're\n"
                "certain the new range can't collide with SSCCs already issued\n"
                "under the current GS1 Company Prefix + extension digit.\n\n"
                'Type RESET below to confirm, and enter the new starting serial:'
            ),
            justify="left",
            padding=10,
        ).grid(row=0, column=0, columnspan=2)

        ttk.Label(confirm_win, text="Confirmation:").grid(row=1, column=0, sticky="e")
        confirm_var = tk.StringVar()
        ttk.Entry(confirm_win, textvariable=confirm_var).grid(row=1, column=1, sticky="w")

        ttk.Label(confirm_win, text="New starting serial:").grid(row=2, column=0, sticky="e")
        new_start_var = tk.StringVar(value="0")
        ttk.Entry(confirm_win, textvariable=new_start_var).grid(row=2, column=1, sticky="w")

        def do_reset():
            if confirm_var.get().strip() != "RESET":
                messagebox.showerror("Not confirmed", 'Type RESET (exactly) to confirm.')
                return
            try:
                new_start = int(new_start_var.get())
                if new_start < 0:
                    raise ValueError("Starting serial number can't be negative.")
            except ValueError as exc:
                messagebox.showerror("Invalid starting serial", str(exc))
                return

            archive_path = archive_and_reset_state_file(self.state_file_var.get(), new_start)
            messagebox.showinfo(
                "Counter reset",
                f"Old counter archived to {archive_path.name}. New counter starts at {new_start}.",
            )
            confirm_win.destroy()
            self._refresh_counter_status()

        ttk.Button(confirm_win, text="Reset", command=do_reset).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def _save(self):
        try:
            prefix = validate_company_prefix(self.company_prefix_var.get())
            extension_digit = validate_extension_digit(self.extension_digit_var.get())
        except ValueError as exc:
            messagebox.showerror("Invalid setting", str(exc))
            return

        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showerror("Invalid setting", "CSV output directory is required.")
            return

        state_file = self.state_file_var.get().strip()
        if not state_file:
            messagebox.showerror("Invalid setting", "SSCC counter file location is required.")
            return

        settings = Settings(
            output_dir=output_dir,
            gs1_company_prefix=prefix,
            sscc_extension_digit=extension_digit,
            sscc_state_file=state_file,
        )
        save_settings(settings)
        messagebox.showinfo("Saved", "Settings saved.")


if __name__ == "__main__":
    SetupGUI().mainloop()
