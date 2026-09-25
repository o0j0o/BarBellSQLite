"""
BarBell main application GUI: job -> packing slip -> GTIN check -> package
details -> CSV. Same flow and underlying logic as generate_labels.py (the
CLI), just as a Tkinter window - both call the same functions in src/labels.py,
src/gtin.py, src/sscc.py, src/settings.py, so there's one source of truth for
the business logic.

Setup (settings.json - GS1 Company Prefix, SSCC counter, CSV output
directory) is intentionally a SEPARATE program (setup_gui.py), reached only
from the About dialog behind a password prompt - not a button on the main
screen, so it isn't one accidental click away.

Run with:
    python barbell_gui.py
"""

import datetime
import subprocess
import sys
import tkinter as tk
import winsound
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk

from dotenv import load_dotenv

from src.barcode_render import render_barcode_image
from src.batch import build_batch_number
from src.db.local_store import (
    count_pallets,
    create_pallet,
    create_reprint_rows,
    fetch_label_history,
    find_carton_by_sscc,
    record_generation_run,
    void_pallet,
    write_flat_csv,
)
from src.db.readonly_connection import ReadOnlyConnection
from src.demo_data import DEMO_JOB_NUMBERS, DemoConnection
from src.gs1 import (
    build_contents_barcode_data,
    build_contents_element_string,
    build_sscc_barcode_data,
    build_sscc_element_string,
)
from src.gtin import GTIN_SOURCE_MANUAL_OVERRIDE, InvalidGTINError, classify_gtin_source, normalize_gtin
from src.labels import (
    assemble_label_rows,
    get_product_info,
    list_packing_slip_line_items,
    list_packing_slips_for_job,
)
from src.pallet_scan import ScanError, check_carton_for_pallet, clean_scanned_sscc
from src.settings import load_settings
from src.sscc import SSCCGenerator, build_sscc, build_test_sscc, get_counter_status
from src.version import BUILD_DATE, version_string

APP_ROOT = Path(__file__).resolve().parent
ICON_PATH = APP_ROOT / "assets" / "barbell_icon.png"  # plain icon-only mark, used as header/About fallback
APP_ICON_PATH = APP_ROOT / "assets" / "barbell_app_icon.png"  # rounded-square app-icon tile, taskbar icon
BARBELL_LOGO_PATH = APP_ROOT / "assets" / "barbell_logo.png"  # full wordmark (icon + "BarBell" text)
CLC_LOGO_PATH = APP_ROOT / "assets" / "clc_logo.png"  # Caribbean Label Crafts Ltd company logo

HEADER_CLC_HEIGHT_PX = 22  # reduced to 50% of its original 44px per user request
HEADER_BARBELL_HEIGHT_PX = 88  # main-screen BarBell logo at 200% (of the original 44px baseline)
ABOUT_BARBELL_TARGET_PX = 200
ABOUT_CLC_TARGET_PX = ABOUT_BARBELL_TARGET_PX // 2  # CLC shown at ~50% of the BarBell logo's size

APP_DESCRIPTION = (
    "BarBell pulls job, packing slip, and item data from Label Traxx and combines it\n"
    "with the SSCC and GTIN needed for GS1-128 logistics labels, producing a CSV ready\n"
    "for BarTender to print on the Zebra printers."
)


def check_setup_password(entered: str, settings) -> bool:
    return entered == settings.setup_password


def scaled_photo_image(path: Path, target_px: int) -> tk.PhotoImage:
    """
    Downscale a source image to roughly `target_px` on its longest side,
    preserving aspect ratio and original colors exactly (no interpolation).
    Uses stdlib PhotoImage.subsample() (integer factors only, so the result
    is approximate) rather than adding a Pillow dependency just for this.
    """
    full = tk.PhotoImage(file=str(path))
    factor = max(1, round(max(full.width(), full.height()) / target_px))
    return full.subsample(factor, factor)


def scaled_photo_image_by_height(path: Path, target_height_px: int) -> tk.PhotoImage:
    """Same as scaled_photo_image(), but targets height specifically - for
    lining up two logos of different aspect ratios side by side in a header."""
    full = tk.PhotoImage(file=str(path))
    factor = max(1, round(full.height() / target_height_px))
    return full.subsample(factor, factor)


def load_scaled_or_none(path: Path, target_px: int, by_height: bool = False) -> tk.PhotoImage | None:
    """Best-effort load - returns None (not an error) if the asset isn't there yet."""
    if not path.exists():
        return None
    try:
        if by_height:
            return scaled_photo_image_by_height(path, target_px)
        return scaled_photo_image(path, target_px)
    except tk.TclError:
        return None


class BarBellApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"BarBell {version_string()}")
        self.resizable(False, False)

        self.settings = load_settings()
        self._taskbar_icon = None
        self._header_barbell_logo = None
        self._header_clc_logo = None
        self._about_barbell_logo = None
        self._about_clc_logo = None
        self._slips = []
        self._selected_slip = None
        self._line_items = []
        self._selected_line_item = None
        self._product = None

        self._load_logos()
        self._build_widgets()
        self._apply_demo_mode_ui()

    # --- setup ---------------------------------------------------------

    def _connect(self):
        """The one place that decides real Label Traxx vs. Demo Mode - every
        DB lookup in this app goes through this instead of instantiating
        ReadOnlyConnection/DemoConnection directly."""
        if self.settings.demo_mode:
            return DemoConnection()
        return ReadOnlyConnection(dsn=self.settings.label_traxx_dsn or None)

    def _apply_demo_mode_ui(self):
        """Demo Mode is read once at startup (self.settings, like every other
        setting) - toggling it in Setup takes effect the next time BarBell is
        started, not live. When on: an unmistakable banner + title-bar tag,
        a hint listing the available demo job numbers, and Test mode is
        forced on and locked - Demo Mode must never issue a real SSCC."""
        if self.settings.demo_mode:
            self.title(f"BarBell {version_string()} - DEMO MODE")
            self.demo_banner.grid()
            self.demo_hint_label.config(
                text=f"Demo Mode - try job numbers: {', '.join(DEMO_JOB_NUMBERS)}"
            )
            self.test_mode_var.set(True)
            self.test_mode_checkbox.config(state="disabled")
        else:
            self.title(f"BarBell {version_string()}")
            self.demo_banner.grid_remove()
            self.demo_hint_label.config(text="")
            self.test_mode_checkbox.config(state="normal")

    def _load_logos(self):
        # Taskbar icon stays the square icon-only mark, not the wordmark.
        self._taskbar_icon = load_scaled_or_none(APP_ICON_PATH, 32) or load_scaled_or_none(ICON_PATH, 32)
        if self._taskbar_icon is not None:
            self.iconphoto(True, self._taskbar_icon)

        # Header: BarBell wordmark (falls back to the icon-only mark if the
        # wordmark file isn't present yet), centered, at 200% of the CLC
        # logo's height. The wordmark already has "BarBell" text baked in -
        # only the icon-only fallback needs a separate text label next to it.
        self._header_barbell_logo = load_scaled_or_none(
            BARBELL_LOGO_PATH, HEADER_BARBELL_HEIGHT_PX, by_height=True
        )
        self._using_wordmark = self._header_barbell_logo is not None
        if self._header_barbell_logo is None:
            self._header_barbell_logo = load_scaled_or_none(
                ICON_PATH, HEADER_BARBELL_HEIGHT_PX, by_height=True
            )
        # CLC logo is pinned to the header's right edge, independent of the
        # centered BarBell logo - see _build_widgets().
        self._header_clc_logo = load_scaled_or_none(
            CLC_LOGO_PATH, HEADER_CLC_HEIGHT_PX, by_height=True
        )

        # About dialog: BarBell logo large, CLC logo at ~50% of that size.
        self._about_barbell_logo = load_scaled_or_none(BARBELL_LOGO_PATH, ABOUT_BARBELL_TARGET_PX)
        self._using_wordmark_about = self._about_barbell_logo is not None
        if self._about_barbell_logo is None:
            self._about_barbell_logo = load_scaled_or_none(ICON_PATH, ABOUT_BARBELL_TARGET_PX)
        self._about_clc_logo = load_scaled_or_none(CLC_LOGO_PATH, ABOUT_CLC_TARGET_PX)

    def _build_widgets(self):
        # Demo Mode banner - always created, shown/hidden by _apply_demo_mode_ui()
        # so tests and later toggles have a stable widget to check, rather than
        # conditionally building it only when demo_mode happens to be on.
        self.demo_banner = tk.Label(
            self,
            text="DEMO MODE - sample data only, not connected to Label Traxx",
            bg="#c0392b",
            fg="white",
            font=("", 11, "bold"),
            pady=6,
        )
        self.demo_banner.grid(row=0, column=0, sticky="ew")
        self.demo_banner.grid_remove()  # hidden unless/until _apply_demo_mode_ui() shows it

        header = ttk.Frame(self, padding=10)
        header.grid(row=1, column=0, sticky="ew")
        # Two equal-weight spacer columns either side of column 1 keep the
        # BarBell logo centered regardless of the header's actual width.
        header.columnconfigure(0, weight=1)
        header.columnconfigure(2, weight=1)

        center = ttk.Frame(header)
        center.grid(row=0, column=1)
        if self._header_barbell_logo is not None:
            ttk.Label(center, image=self._header_barbell_logo).pack(side="left")
        if not self._using_wordmark:
            ttk.Label(center, text="BarBell", font=("", 16, "bold")).pack(side="left", padx=10)

        if self._header_clc_logo is not None:
            # place(), not grid - pinned to the header's right edge, independent
            # of the centered BarBell logo above.
            ttk.Label(header, image=self._header_clc_logo).place(relx=1.0, rely=0.5, anchor="e")

        job_frame = ttk.LabelFrame(self, text="1. Job", padding=10)
        job_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        ttk.Label(job_frame, text="Job number:").grid(row=0, column=0, sticky="w")
        self.job_number_var = tk.StringVar()
        ttk.Entry(job_frame, textvariable=self.job_number_var, width=20).grid(
            row=0, column=1, sticky="w", padx=5
        )
        ttk.Button(job_frame, text="Find Packing Slips", command=self._load_packing_slips).grid(
            row=0, column=2
        )
        self.demo_hint_label = ttk.Label(job_frame, text="", foreground="#c0392b", font=("", 8))
        self.demo_hint_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(4, 0))

        slip_frame = ttk.LabelFrame(self, text="2. Packing Slip", padding=10)
        slip_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.slip_listbox = tk.Listbox(slip_frame, width=90, height=6, exportselection=False)
        self.slip_listbox.grid(row=0, column=0, sticky="ew")
        self.slip_listbox.bind("<<ListboxSelect>>", self._on_slip_selected)

        product_frame = ttk.LabelFrame(self, text="3. Product (a packing slip can carry more than one)", padding=10)
        product_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        self.product_listbox = tk.Listbox(product_frame, width=90, height=4, exportselection=False)
        self.product_listbox.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.product_listbox.bind("<<ListboxSelect>>", self._on_product_selected)

        self.gtin_status_label = ttk.Label(product_frame, text="", wraplength=600, justify="left")
        self.gtin_status_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(8, 0))

        ttk.Label(product_frame, text="GTIN:").grid(row=2, column=0, sticky="w", pady=(4, 0))
        self.gtin_entry_var = tk.StringVar()
        self.gtin_entry = ttk.Entry(product_frame, textvariable=self.gtin_entry_var, width=30)
        self.gtin_entry.grid(row=2, column=1, sticky="w", pady=(4, 0))
        ttk.Label(
            product_frame,
            text="Manually entered values are never saved back to Label Traxx.",
            font=("", 8),
        ).grid(row=3, column=0, columnspan=2, sticky="w")

        pkg_frame = ttk.LabelFrame(self, text="4. Package Details", padding=10)
        pkg_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        ttk.Label(pkg_frame, text="Units per package:").grid(row=0, column=0, sticky="w")
        self.units_per_package_var = tk.StringVar()
        ttk.Entry(pkg_frame, textvariable=self.units_per_package_var, width=15).grid(
            row=0, column=1, sticky="w", padx=5
        )

        ttk.Label(pkg_frame, text="Logistics labels per package:").grid(row=1, column=0, sticky="w")
        self.labels_per_package_var = tk.StringVar()
        ttk.Entry(pkg_frame, textvariable=self.labels_per_package_var, width=15).grid(
            row=1, column=1, sticky="w", padx=5
        )

        ttk.Label(pkg_frame, text="Production date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.production_date_var = tk.StringVar()
        ttk.Entry(pkg_frame, textvariable=self.production_date_var, width=15).grid(
            row=2, column=1, sticky="w", padx=5
        )

        self.test_mode_var = tk.BooleanVar(value=False)
        self.test_mode_checkbox = ttk.Checkbutton(
            pkg_frame,
            text="Test mode (fake SSCCs - doesn't touch the real counter)",
            variable=self.test_mode_var,
        )
        self.test_mode_checkbox.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

        action_frame = ttk.Frame(self, padding=10)
        action_frame.grid(row=6, column=0, sticky="ew")
        ttk.Button(action_frame, text="Preview Barcode", command=self._preview_barcode).pack(side="left")
        ttk.Button(action_frame, text="Generate Labels", command=self._generate).pack(side="left", padx=(8, 0))
        ttk.Button(action_frame, text="Pallet Labels...", command=self._show_pallet_screen).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(action_frame, text="Job/Label History...", command=self._show_history).pack(
            side="right", padx=(0, 8)
        )
        ttk.Button(action_frame, text="About", command=self._show_about).pack(side="right")

    # --- job / packing slip / GTIN -------------------------------------

    def _load_packing_slips(self):
        job_number = self.job_number_var.get().strip()
        if not job_number:
            messagebox.showerror("Missing job number", "Enter a job number first.")
            return

        self.slip_listbox.delete(0, tk.END)
        self._reset_product_selection()
        self._slips = []
        self._selected_slip = None

        try:
            with self._connect() as conn:
                slips = list_packing_slips_for_job(conn, job_number)
        except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
            messagebox.showerror("Lookup failed", str(exc))
            return

        if not slips:
            messagebox.showwarning("No packing slips", f"No packing slips found for job {job_number!r}.")
            return

        self._slips = slips
        for slip in slips:
            self.slip_listbox.insert(
                tk.END,
                f"{slip.number} (suffix {slip.suffix}) - {slip.customer_name} - "
                f"ship date {slip.ship_date} - qty {slip.ship_quantity} - "
                f"{slip.no_package} package(s) per Label Traxx",
            )

    def _set_gtin_status_text(self, text: str, error: bool = False):
        """error=True renders in red - used for a blocking, invalid-GTIN warning
        (see _on_product_selected) so it stays visibly distinct even after the
        matching messagebox is dismissed."""
        self.gtin_status_label.config(text=text, foreground="red" if error else "")

    def _reset_product_selection(self):
        self.product_listbox.delete(0, tk.END)
        self._line_items = []
        self._selected_line_item = None
        self._product = None
        self._set_gtin_status_text("")
        self.gtin_entry_var.set("")
        self.gtin_entry.config(state="normal")

    def _on_slip_selected(self, _event):
        selection = self.slip_listbox.curselection()
        if not selection:
            return
        self._selected_slip = self._slips[selection[0]]
        self._reset_product_selection()

        try:
            with self._connect() as conn:
                items = list_packing_slip_line_items(conn, self._selected_slip.number)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Lookup failed", str(exc))
            return

        self._line_items = items
        for item in items:
            self.product_listbox.insert(
                tk.END, f"P/N {item.product_number} - {item.description} - qty {item.ship_quantity}"
            )
        if len(items) == 1:
            self.product_listbox.select_set(0)
            self._on_product_selected(None)

    def _on_product_selected(self, _event):
        selection = self.product_listbox.curselection()
        if not selection:
            return
        self._selected_line_item = self._line_items[selection[0]]

        try:
            with self._connect() as conn:
                product = get_product_info(conn, self._selected_line_item.product_number)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Lookup failed", str(exc))
            self._product = None
            return

        self._product = product
        self._apply_gtin_entry_state_for_product(product)

    def _apply_gtin_entry_state_for_product(self, product):
        """
        Sets the status label, textbox content, and textbox enabled state for
        a newly-selected product. Split out from _on_product_selected() (which
        needs a live DB lookup) so this part - the actual prefill/warning
        logic - is directly testable.
        """
        override_allowed = self.settings.allow_manual_gtin_override

        if product.gtin:
            self._set_gtin_status_text(f"GTIN on file: {product.gtin}")
            self.gtin_entry_var.set(product.gtin_raw or "")
            # Beta default: always editable. Once allow_manual_gtin_override
            # is turned off, a valid BC_Start becomes authoritative again and
            # the field is locked to it - no code change needed to tighten.
            self.gtin_entry.config(state="normal" if override_allowed else "disabled")
            return

        # No usable value on file - the textbox is always enabled here
        # (there's nothing to fall back on), and it's required: normalize_gtin
        # rejects blank input, so _resolve_gtin() blocks Preview/Generate
        # until something valid is typed in. Not dismissible: closing this
        # popup doesn't lift that block.
        self.gtin_entry_var.set("")
        self.gtin_entry.config(state="normal")
        messagebox.showwarning(
            "No GTIN on file",
            f"No GTIN on file in Label Traxx for P/N {product.prod_num} "
            f"({product.description}).\n\nEnter one below to continue.",
        )
        self._set_gtin_status_text(
            f"No GTIN on file for P/N {product.prod_num} ({product.description}) - "
            "enter one below.",
            error=True,
        )

    def _resolve_gtin(self):
        """
        Reads the GTIN textbox and validates it through the same code path
        as Product.BC_Start. If it differs from a valid BC_Start value, this
        is a deliberate override, and requires explicit confirmation before
        proceeding - showing both values - since that's the one case where
        the operator is knowingly overriding known Label Traxx data. Returns
        the normalized GTIN to use, or None if blocked/declined (having
        already shown the relevant error/prompt).
        """
        raw = self.gtin_entry_var.get()
        try:
            normalized = normalize_gtin(raw)
        except InvalidGTINError as exc:
            messagebox.showerror("Invalid GTIN", str(exc))
            return None

        if classify_gtin_source(self._product.gtin, normalized) == GTIN_SOURCE_MANUAL_OVERRIDE:
            confirmed = messagebox.askyesno(
                "Confirm GTIN override",
                f"Label Traxx has GTIN {self._product.gtin} on file for this item.\n"
                f"You are about to use {normalized} instead.\n\n"
                "This will NOT be saved back to Label Traxx. Continue?",
            )
            if not confirmed:
                return None

        return normalized

    # --- generate --------------------------------------------------------

    def _gather_preview_inputs(self):
        """
        Validates the form and computes everything needed for a preview
        (barcode or text) or an actual generate - shared by both so they can
        never disagree with each other. Returns None (having already shown
        the relevant error) if anything's missing/invalid.
        """
        job_number = self.job_number_var.get().strip()
        if not job_number or self._selected_line_item is None:
            messagebox.showerror("Incomplete", "Pick a job, packing slip, and product first.")
            return None
        if self._product is None:
            messagebox.showerror("Incomplete", "Couldn't load product info for this line item.")
            return None

        gtin = self._resolve_gtin()
        if gtin is None:
            return None

        try:
            units_per_package = int(self.units_per_package_var.get())
            labels_per_package = int(self.labels_per_package_var.get())
            if units_per_package <= 0 or labels_per_package <= 0:
                raise ValueError("Units per package and labels per package must be positive.")
        except ValueError as exc:
            messagebox.showerror("Invalid input", f"Units/labels per package: {exc}")
            return None

        production_date = self.production_date_var.get().strip()
        try:
            datetime.date.fromisoformat(production_date)
        except ValueError:
            messagebox.showerror("Invalid date", f"{production_date!r} isn't a valid YYYY-MM-DD date.")
            return None

        line_item = self._selected_line_item
        total_qty = line_item.ship_quantity
        test_mode = self.test_mode_var.get()

        batch = build_batch_number(job_number, self._product.prod_num)
        first_package_qty = min(units_per_package, total_qty)
        preview_sscc = (
            build_test_sscc(1)
            if test_mode
            else build_sscc(
                self.settings.gs1_company_prefix,
                self.settings.sscc_extension_digit,
                get_counter_status(self.settings.sscc_state_file).next_serial or 0,
            )
        )

        return {
            "job_number": job_number,
            "line_item": line_item,
            "units_per_package": units_per_package,
            "labels_per_package": labels_per_package,
            "production_date": production_date,
            "total_qty": total_qty,
            "num_packages": -(-total_qty // units_per_package),  # ceil division
            "test_mode": test_mode,
            "gtin": gtin,
            "batch": batch,
            "first_package_qty": first_package_qty,
            "preview_sscc": preview_sscc,
        }

    def _preview_barcode(self):
        info = self._gather_preview_inputs()
        if info is None:
            return

        contents_data = build_contents_barcode_data(
            info["gtin"], info["production_date"], info["first_package_qty"], info["batch"]
        )
        sscc_data = build_sscc_barcode_data(info["preview_sscc"])

        win = tk.Toplevel(self)
        win.title("Barcode Preview - package 1")
        win.resizable(False, False)
        frame = ttk.Frame(win, padding=15)
        frame.pack()

        for label, ai_text, data in (
            ("Contents", build_contents_element_string(
                info["gtin"], info["production_date"], info["first_package_qty"], info["batch"]
            ), contents_data),
            ("SSCC", build_sscc_element_string(info["preview_sscc"]), sscc_data),
        ):
            ttk.Label(frame, text=label, font=("", 11, "bold")).pack(anchor="w", pady=(10, 0))
            photo = self._render_barcode_photo(data)
            ttk.Label(frame, image=photo).pack()
            ttk.Label(frame, text=ai_text, font=("Courier New", 10)).pack()
            # keep a reference so the image isn't garbage-collected while shown
            win.__dict__.setdefault("_photos", []).append(photo)

        if info["test_mode"]:
            note = "Test mode - this SSCC is a fake placeholder, not a real one."
        else:
            note = "This is the NEXT real SSCC that would be issued - previewing does not consume it."
        ttk.Label(frame, text=note, wraplength=350, justify="center").pack(pady=(10, 0))
        ttk.Button(frame, text="Close", command=win.destroy).pack(pady=(10, 0))

    def _render_barcode_photo(self, barcode_data: str) -> tk.PhotoImage:
        import base64
        import io

        image = render_barcode_image(barcode_data)
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return tk.PhotoImage(data=base64.b64encode(buf.getvalue()).decode("ascii"))

    def _generate(self):
        info = self._gather_preview_inputs()
        if info is None:
            return

        job_number = info["job_number"]
        line_item = info["line_item"]
        packing_slip_number = line_item.packing_slip_number
        total_qty = info["total_qty"]
        num_packages = info["num_packages"]
        test_mode = info["test_mode"]
        units_per_package = info["units_per_package"]
        labels_per_package = info["labels_per_package"]
        production_date = info["production_date"]

        preview_text = (
            f"GS1-128 element strings for package 1:\n"
            f"  Contents: {build_contents_element_string(info['gtin'], production_date, info['first_package_qty'], info['batch'])}\n"
            f"  SSCC:     {build_sscc_element_string(info['preview_sscc'])}\n\n"
        )

        gen = None
        if test_mode:
            confirmed = messagebox.askyesno(
                "Confirm test run",
                preview_text
                + f"Test mode: will generate {num_packages} fake TEST-SSCC-##### row(s) for job "
                f"{job_number}, packing slip {packing_slip_number}. The real SSCC counter will "
                f"NOT be touched. Continue?",
            )
        else:
            confirmed = messagebox.askyesno(
                "Confirm SSCC issuance",
                preview_text
                + f"About to issue {num_packages} real SSCC number(s) for job {job_number}, "
                f"packing slip {packing_slip_number} ({total_qty} units at "
                f"{units_per_package}/package).\n\nSSCCs can never be reused once issued. Continue?",
            )
            if confirmed:
                gen = SSCCGenerator(
                    self.settings.gs1_company_prefix,
                    self.settings.sscc_extension_digit,
                    self.settings.sscc_state_file,
                )
        if not confirmed:
            return

        try:
            with self._connect() as conn:
                rows = assemble_label_rows(
                    conn=conn,
                    sscc_generator=gen,
                    job_number=job_number,
                    line_item=line_item,
                    units_per_package=units_per_package,
                    labels_per_package=labels_per_package,
                    production_date=production_date,
                    gtin_override=info["gtin"],
                    audit_log_file=(
                        self.settings.demo_audit_log_file
                        if self.settings.demo_mode
                        else self.settings.audit_log_file
                    ),
                    test_mode=test_mode,
                )
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Generation failed", str(exc))
            return

        try:
            flat_rows = record_generation_run(
                rows,
                units_per_package=units_per_package,
                labels_per_package=labels_per_package,
                test_mode=test_mode,
                db_path=(
                    self.settings.demo_db_file if self.settings.demo_mode else self.settings.local_db_file
                ),
            )
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror(
                "Database error",
                f"Labels were generated but could not be logged to the local database:\n{exc}",
            )
            return

        out_path = self._write_csv(
            flat_rows, job_number, packing_slip_number, test_mode=test_mode, demo_mode=self.settings.demo_mode
        )
        packages_used = len({r.sscc for r in rows})
        messagebox.showinfo(
            "Labels generated",
            f"Wrote {len(rows)} label row(s) covering {packages_used} package(s) to:\n{out_path}",
        )

    def _write_csv(self, rows, job_number, packing_slip_number, test_mode=False, demo_mode=False) -> Path:
        output_dir = Path(self.settings.output_dir)
        prefix = "DEMO_" if demo_mode else ""
        suffix = "_TEST" if test_mode else ""
        out_path = output_dir / f"{prefix}labels_{job_number}_{packing_slip_number}{suffix}.csv"
        return write_flat_csv(rows, out_path)

    # --- job/label history -----------------------------------------------

    def _show_history(self):
        """
        Browses BarBell's own local log of everything it has generated
        (src/db/local_store.py), joined from the Jobs and Labels tables -
        not Label Traxx. Filter by an exact Job No and/or production date
        (YYYY-MM-DD); leave either blank to not filter on it.
        """
        win = tk.Toplevel(self)
        win.title("Job/Label History")
        win.geometry("1000x520")
        win.minsize(600, 300)

        CHECKED, UNCHECKED = "☑", "☐"  # ☑ / ☐
        checked_ids: set[str] = set()  # tree iids (== str(label id)) currently checked

        filter_frame = ttk.Frame(win, padding=10)
        filter_frame.pack(fill="x")

        ttk.Label(filter_frame, text="Job No:").pack(side="left")
        job_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=job_filter_var, width=12).pack(side="left", padx=(4, 12))

        ttk.Label(filter_frame, text="Date (YYYY-MM-DD):").pack(side="left")
        date_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=date_filter_var, width=11).pack(side="left", padx=(4, 12))

        # Live substring search against the full SSCC - any fragment (GS1
        # prefix, sequence number, or a piece spanning both) matches, so the
        # full number including the company prefix is never required. Filters
        # as you type; see the trace_add() below.
        ttk.Label(filter_frame, text="SSCC contains:").pack(side="left")
        sscc_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=sscc_filter_var, width=22).pack(side="left", padx=(4, 12))

        columns = (
            "sel", "job_number", "packing_slip", "product_no", "item_number", "batch",
            "sscc", "carton_seq", "copy", "quantity", "status", "label_type", "pallet_sscc",
            "created_at",
        )
        headings = {
            "job_number": "Job No", "packing_slip": "Packing Slip", "product_no": "P/N",
            "item_number": "Item No", "batch": "Batch", "sscc": "SSCC",
            "carton_seq": "Carton Seq", "copy": "Copy", "quantity": "Qty",
            "status": "Status", "label_type": "Label Type", "pallet_sscc": "Pallet SSCC",
            "created_at": "Logged At",
        }

        # Packed before the grid frame so the row-count line always keeps its
        # space at the bottom, however the grid resizes.
        status_label = ttk.Label(win, text="", padding=(10, 0, 10, 10))
        status_label.pack(side="bottom", fill="x")

        # grid(), not pack(): with pack the scrollbar was placed after a tree
        # wider than the window and got pushed off-screen. Here the tree takes
        # all the flexible space and the scrollbars sit in their own row/column.
        tree_frame = ttk.Frame(win, padding=(10, 0, 10, 0))
        tree_frame.pack(side="top", fill="both", expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        tree.heading("sel", text=UNCHECKED, command=lambda: toggle_select_all())
        tree.column("sel", width=30, anchor="center", stretch=False)
        # stretch=False everywhere: columns keep their set widths instead of
        # shrinking to fit, so a window narrower than the table gets a working
        # horizontal scrollbar rather than squashed/clipped columns.
        column_widths = {
            "job_number": 80, "packing_slip": 95, "product_no": 80, "item_number": 80,
            "batch": 120, "sscc": 170, "carton_seq": 85, "copy": 50, "quantity": 65,
            "status": 75, "label_type": 85, "pallet_sscc": 170, "created_at": 210,
        }
        for col in columns:
            if col == "sel":
                continue
            tree.heading(col, text=headings[col])
            tree.column(col, width=column_widths[col], anchor="w", stretch=False)

        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        def row_checkbox_symbol(iid: str) -> str:
            return CHECKED if iid in checked_ids else UNCHECKED

        def redraw_row_checkbox(iid: str):
            values = list(tree.item(iid, "values"))
            values[0] = row_checkbox_symbol(iid)
            tree.item(iid, values=values)

        def sync_select_all_heading():
            visible = tree.get_children()
            all_checked = bool(visible) and all(iid in checked_ids for iid in visible)
            tree.heading("sel", text=CHECKED if all_checked else UNCHECKED)

        def toggle_select_all():
            visible = tree.get_children()
            all_checked = bool(visible) and all(iid in checked_ids for iid in visible)
            new_state = not all_checked  # selecting from none/some -> all; from all -> none
            for iid in visible:
                if new_state:
                    checked_ids.add(iid)
                else:
                    checked_ids.discard(iid)
                redraw_row_checkbox(iid)
            sync_select_all_heading()

        def on_tree_click(event):
            if tree.identify_region(event.x, event.y) != "cell":
                return
            if tree.identify_column(event.x) != "#1":  # the "sel" column
                return
            iid = tree.identify_row(event.y)
            if not iid:
                return
            if iid in checked_ids:
                checked_ids.discard(iid)
            else:
                checked_ids.add(iid)
            redraw_row_checkbox(iid)
            sync_select_all_heading()

        tree.bind("<Button-1>", on_tree_click)

        def refresh():
            checked_ids.clear()  # a new search/filter clears stale selections
            tree.heading("sel", text=UNCHECKED)
            tree.delete(*tree.get_children())
            try:
                rows = fetch_label_history(
                    self.settings.demo_db_file if self.settings.demo_mode else self.settings.local_db_file,
                    job_number=job_filter_var.get().strip() or None,
                    date=date_filter_var.get().strip() or None,
                    sscc_contains=sscc_filter_var.get().strip() or None,
                )
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Lookup failed", str(exc), parent=win)
                return
            for r in rows:
                tree.insert(
                    "",
                    tk.END,
                    iid=str(r.id),
                    values=(
                        UNCHECKED, r.job_number, r.packing_slip_number, r.product_no, r.item_number,
                        r.batch, r.sscc, r.package_index, r.label_copy_index, r.quantity,
                        r.status, r.label_type, r.pallet_sscc or "", r.created_at,
                    ),
                )
            status_label.config(text=f"{len(rows)} label row(s)")

        def export_selected():
            selected_ids = [int(iid) for iid in tree.get_children() if iid in checked_ids]
            if not selected_ids:
                messagebox.showinfo(
                    "Nothing selected", "Check one or more rows first.", parent=win
                )
                return

            confirmed = messagebox.askyesno(
                "Confirm reprint export",
                f"Export {len(selected_ids)} selected label(s) to CSV?\n\n"
                "Each one will be logged as a new 'reprint' row in the database, "
                "linked back to the original - the original rows are kept, not changed.",
                parent=win,
            )
            if not confirmed:
                return

            demo = self.settings.demo_mode
            db_path = self.settings.demo_db_file if demo else self.settings.local_db_file
            try:
                reprint_rows = create_reprint_rows(selected_ids, db_path=db_path)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                prefix = "DEMO_" if demo else ""
                out_path = write_flat_csv(
                    reprint_rows, Path(self.settings.output_dir) / f"{prefix}reprint_{timestamp}.csv"
                )
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Reprint failed", str(exc), parent=win)
                return

            messagebox.showinfo(
                "Reprint exported",
                f"Wrote {len(reprint_rows)} label row(s) to:\n{out_path}",
                parent=win,
            )
            refresh()  # show the newly created reprint rows if they match the current filter

        def void_selected_pallet():
            selected_ids = [iid for iid in tree.get_children() if iid in checked_ids]
            if not selected_ids:
                messagebox.showinfo("Nothing selected", "Check a pallet's rows first.", parent=win)
                return

            pallet_ssccs = set()
            saw_non_pallet = False
            for iid in selected_ids:
                values = tree.item(iid, "values")
                if values[11] == "PALLET":  # label_type column
                    pallet_ssccs.add(values[6])  # sscc column
                else:
                    saw_non_pallet = True
            if saw_non_pallet or not pallet_ssccs:
                messagebox.showerror(
                    "Invalid selection", "Check only a pallet's own row(s) to void it.", parent=win
                )
                return
            if len(pallet_ssccs) > 1:
                messagebox.showerror(
                    "Invalid selection", "Check rows for only one pallet at a time.", parent=win
                )
                return
            pallet_sscc = next(iter(pallet_ssccs))

            confirmed = messagebox.askyesno(
                "Confirm void pallet",
                f"Void pallet {pallet_sscc}?\n\n"
                "This cannot be undone - the SSCC is never reused, and every carton "
                "currently on this pallet will be freed to be scanned onto a new one.",
                parent=win,
            )
            if not confirmed:
                return

            db_path = self.settings.demo_db_file if self.settings.demo_mode else self.settings.local_db_file
            try:
                freed = void_pallet(pallet_sscc, db_path)
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror("Void failed", str(exc), parent=win)
                return

            messagebox.showinfo(
                "Pallet voided",
                f"Pallet {pallet_sscc} voided. {freed} carton(s) freed to be scanned onto a new pallet.",
                parent=win,
            )
            refresh()

        button_frame = ttk.Frame(filter_frame)
        button_frame.pack(side="left")
        ttk.Button(button_frame, text="Search / Refresh", command=refresh).pack(side="left")
        ttk.Button(
            button_frame,
            text="Clear filters",
            command=lambda: (
                job_filter_var.set(""), date_filter_var.set(""), sscc_filter_var.set(""), refresh()
            ),
        ).pack(side="left", padx=(6, 0))
        ttk.Button(
            button_frame, text="Reprint Selected (Export to CSV)", command=export_selected
        ).pack(side="left", padx=(12, 0))
        ttk.Button(
            button_frame, text="Void Pallet", command=void_selected_pallet
        ).pack(side="left", padx=(8, 0))

        refresh()
        # Registered after the initial refresh() so setting up the window
        # doesn't fire it. Every keystroke in the SSCC box re-filters (which,
        # like any new search, clears checkboxes - see refresh()).
        sscc_filter_var.trace_add("write", lambda *_: refresh())

    # --- pallet labels -----------------------------------------------------

    def _show_pallet_screen(self):
        """
        Scan-to-build a pallet label: scan each carton's SSCC (a Bluetooth
        scanner acting as a keyboard wedge - types the decoded barcode, then
        Enter), BarBell links them to a new pallet SSCC and sums their
        quantity for AI (37). See src/pallet_scan.py for the scan
        cleanup/validation this screen is built around, and QUESTIONS.md #18.
        """
        win = tk.Toplevel(self)
        win.title("Pallet Labels")
        win.geometry("1000x620")
        win.minsize(700, 400)

        db_path = self.settings.demo_db_file if self.settings.demo_mode else self.settings.local_db_file
        scanned_cartons: list = []  # CartonInfo, in scan order - scanned_cartons[0] is the reference

        # --- step 1: expected carton count -----------------------------

        top_frame = ttk.Frame(win, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="1. Expected carton count:").pack(side="left")
        expected_count_var = tk.StringVar()
        expected_count_entry = ttk.Entry(top_frame, textvariable=expected_count_var, width=8)
        expected_count_entry.pack(side="left", padx=(4, 20))

        pallet_test_mode_var = tk.BooleanVar(value=self.settings.demo_mode)
        pallet_test_mode_checkbox = ttk.Checkbutton(
            top_frame, text="Test mode (fake SSCCs)", variable=pallet_test_mode_var
        )
        pallet_test_mode_checkbox.pack(side="left")
        if self.settings.demo_mode:
            pallet_test_mode_checkbox.config(state="disabled")  # Demo Mode must never issue a real SSCC

        # --- step 2: scan -------------------------------------------------

        scan_frame = ttk.Frame(win, padding=(10, 0, 10, 10))
        scan_frame.pack(fill="x")

        ttk.Label(scan_frame, text="2. Scan SSCC:").pack(side="left")
        scan_var = tk.StringVar()
        scan_entry = ttk.Entry(scan_frame, textvariable=scan_var, width=30, state="disabled")
        scan_entry.pack(side="left", padx=(4, 12))

        scan_feedback_label = ttk.Label(scan_frame, text="", font=("", 10, "bold"))
        scan_feedback_label.pack(side="left")

        def expected_count() -> int | None:
            """The typed expected count, or None if it isn't currently a
            whole number >= 1 - the one thing that gates scanning at all."""
            raw = expected_count_var.get().strip()
            try:
                value = int(raw)
            except ValueError:
                return None
            return value if value >= 1 else None

        def sync_scan_entry_enabled(*_):
            scan_entry.config(state="normal" if expected_count() is not None else "disabled")

        expected_count_var.trace_add("write", sync_scan_entry_enabled)

        # --- grid: one row per scanned carton ------------------------------

        columns = (
            "sscc", "qty", "job_number", "packing_slip", "product_no", "batch", "gtin",
            "production_date", "printed_at",
        )
        headings = {
            "sscc": "SSCC No.", "qty": "Qty", "job_number": "Job No.",
            "packing_slip": "Packing Slip", "product_no": "P/N", "batch": "Batch",
            "gtin": "GTIN", "production_date": "Production Date", "printed_at": "Printed Date/Time",
        }
        column_widths = {
            "sscc": 170, "qty": 80, "job_number": 80, "packing_slip": 95, "product_no": 80,
            "batch": 120, "gtin": 130, "production_date": 110, "printed_at": 170,
        }

        totals_label = ttk.Label(win, text="", padding=(10, 0, 10, 10))
        totals_label.pack(side="bottom", fill="x")

        tree_frame = ttk.Frame(win, padding=(10, 0, 10, 0))
        tree_frame.pack(side="top", fill="both", expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=column_widths[col], anchor="w", stretch=False)
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        def refresh_grid_and_totals():
            tree.delete(*tree.get_children())
            for carton in scanned_cartons:
                tree.insert(
                    "", tk.END, iid=carton.sscc,
                    values=(
                        carton.sscc, carton.quantity, carton.job_number, carton.packing_slip_number,
                        carton.product_no, carton.batch, carton.gtin, carton.production_date,
                        carton.created_at,
                    ),
                )
            expected = expected_count()
            expected_text = str(expected) if expected is not None else "?"
            total_qty = sum(c.quantity for c in scanned_cartons)
            totals_label.config(
                text=(
                    f"Scanned {len(scanned_cartons)} of {expected_text} cartons   |   "
                    f"Pallet total qty: {total_qty:,}"
                )
            )

        refresh_grid_and_totals()

        # --- scanning ------------------------------------------------------

        def show_feedback(message: str, ok: bool):
            scan_feedback_label.config(text=message, foreground="#1e8449" if ok else "#c0392b")
            try:
                winsound.MessageBeep(winsound.MB_OK if ok else winsound.MB_ICONHAND)
            except RuntimeError:
                pass  # no sound device - not fatal, the on-screen message still shows

        def on_scan_submit(_event=None):
            raw = scan_var.get()
            scan_var.set("")
            scan_entry.focus_set()
            if not raw.strip():
                return

            try:
                sscc = clean_scanned_sscc(raw, test_mode=pallet_test_mode_var.get())
            except ScanError as exc:
                show_feedback(str(exc), ok=False)
                return

            carton = find_carton_by_sscc(sscc, db_path)
            check = check_carton_for_pallet(
                carton, scanned_cartons, expected_count() or 0, pallet_test_mode_var.get()
            )
            if check.blocked_reason:
                show_feedback(check.blocked_reason, ok=False)
                return

            for warning in check.warnings:
                if not messagebox.askyesno(
                    "Confirm carton", f"{warning}\n\nAdd this carton to the pallet anyway?", parent=win
                ):
                    show_feedback("Scan discarded.", ok=False)
                    return

            scanned_cartons.append(check.carton)
            refresh_grid_and_totals()
            show_feedback(f"{sscc} added.", ok=True)

        scan_entry.bind("<Return>", on_scan_submit)

        # --- remove / clear --------------------------------------------------

        def remove_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showinfo("Nothing selected", "Select a row to remove first.", parent=win)
                return
            if not messagebox.askyesno(
                "Confirm remove", f"Remove {len(selection)} scanned carton(s) from this pallet?",
                parent=win,
            ):
                return
            selected_ssccs = set(selection)
            scanned_cartons[:] = [c for c in scanned_cartons if c.sscc not in selected_ssccs]
            refresh_grid_and_totals()

        def clear_pallet():
            if not scanned_cartons:
                return
            if not messagebox.askyesno(
                "Confirm clear", "Clear every scanned carton from this pallet?", parent=win
            ):
                return
            scanned_cartons.clear()
            refresh_grid_and_totals()

        # --- preview / generate ---------------------------------------------

        def pallet_reference_fields():
            """(gtin, batch, earliest production_date, packing_slip_number,
            job_number, total_qty) from the current scan - None if nothing's
            been scanned yet."""
            if not scanned_cartons:
                return None
            first = scanned_cartons[0]
            earliest_date = min(c.production_date for c in scanned_cartons)
            total_qty = sum(c.quantity for c in scanned_cartons)
            return {
                "gtin": first.gtin, "batch": first.batch, "production_date": earliest_date,
                "packing_slip_number": first.packing_slip_number, "job_number": first.job_number,
                "quantity": total_qty,
            }

        def preview_barcode():
            fields = pallet_reference_fields()
            if fields is None:
                messagebox.showerror("Nothing scanned", "Scan at least one carton first.", parent=win)
                return

            contents_data = build_contents_barcode_data(
                fields["gtin"], fields["production_date"], fields["quantity"], fields["batch"]
            )

            preview_win = tk.Toplevel(win)
            preview_win.title("Pallet Barcode Preview")
            preview_win.resizable(False, False)
            frame = ttk.Frame(preview_win, padding=15)
            frame.pack()

            ttk.Label(frame, text="Contents", font=("", 11, "bold")).pack(anchor="w", pady=(10, 0))
            photo = self._render_barcode_photo(contents_data)
            ttk.Label(frame, image=photo).pack()
            ttk.Label(
                frame,
                text=build_contents_element_string(
                    fields["gtin"], fields["production_date"], fields["quantity"], fields["batch"]
                ),
                font=("Courier New", 10),
            ).pack()
            preview_win.__dict__.setdefault("_photos", []).append(photo)

            ttk.Label(frame, text="SSCC", font=("", 11, "bold")).pack(anchor="w", pady=(14, 0))
            ttk.Label(
                frame,
                text="Assigned when Pallet Label is generated - not reserved by Preview.",
                wraplength=350, justify="center",
            ).pack()

            ttk.Button(frame, text="Close", command=preview_win.destroy).pack(pady=(14, 0))

        def generate_pallet_label():
            fields = pallet_reference_fields()
            if fields is None:
                messagebox.showerror("Nothing scanned", "Scan at least one carton first.", parent=win)
                return

            expected = expected_count() or len(scanned_cartons)
            if len(scanned_cartons) < expected:
                if not messagebox.askyesno(
                    "Fewer cartons than expected",
                    f"Only {len(scanned_cartons)} of {expected} cartons scanned. "
                    f"Generate pallet label for {len(scanned_cartons)} cartons?",
                    parent=win,
                ):
                    return

            test_mode = pallet_test_mode_var.get()
            confirmed = messagebox.askyesno(
                "Confirm pallet SSCC" if test_mode else "Confirm real SSCC issuance",
                (
                    f"Generate a pallet label for {len(scanned_cartons)} carton(s), "
                    f"total qty {fields['quantity']:,}?"
                    + ("\n\nTest mode - a fake SSCC will be used." if test_mode
                       else "\n\nA real SSCC will be issued and can never be reused. Continue?")
                ),
                parent=win,
            )
            if not confirmed:
                return

            if test_mode:
                pallet_sscc = build_test_sscc(count_pallets(db_path) + 1)
            else:
                pallet_sscc = SSCCGenerator(
                    self.settings.gs1_company_prefix,
                    self.settings.sscc_extension_digit,
                    self.settings.sscc_state_file,
                ).next_sscc()

            try:
                pallet_rows = create_pallet(
                    carton_ssccs=[c.sscc for c in scanned_cartons],
                    job_number=fields["job_number"],
                    quantity=fields["quantity"],
                    production_date=fields["production_date"],
                    packing_slip_number=fields["packing_slip_number"],
                    pallet_sscc=pallet_sscc,
                    carton_count=len(scanned_cartons),
                    db_path=db_path,
                )
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror(
                    "Pallet save failed",
                    f"The pallet could not be saved - no CSV was written, and the SSCC "
                    f"{pallet_sscc} was not used:\n{exc}",
                    parent=win,
                )
                return

            # The pallet row is safely committed at this point - if the CSV
            # write below fails, the SSCC is NOT lost: the pallet already
            # exists in history and can be exported again from there
            # (Job/Label History's Reprint Selected), same SSCC, no new one.
            demo = self.settings.demo_mode
            prefix = "DEMO_" if demo else ""
            suffix = "_TEST" if test_mode else ""
            out_path = Path(self.settings.output_dir) / f"{prefix}Pallet_labels_{fields['job_number']}_{pallet_sscc}{suffix}.csv"
            try:
                write_flat_csv(pallet_rows, out_path)
            except Exception as exc:  # noqa: BLE001
                messagebox.showerror(
                    "CSV write failed",
                    f"Pallet {pallet_sscc} was saved, but the CSV could not be written:\n{exc}\n\n"
                    "Use Reprint Selected in Job/Label History to export it again - "
                    "it will use this SAME SSCC, not a new one.",
                    parent=win,
                )
                return

            messagebox.showinfo(
                "Pallet label generated",
                f"Pallet SSCC: {pallet_sscc}\nWrote 2 label row(s) to:\n{out_path}",
                parent=win,
            )
            scanned_cartons.clear()
            expected_count_var.set("")
            refresh_grid_and_totals()

        # --- window-level buttons / close -------------------------------

        button_frame = ttk.Frame(win, padding=10)
        button_frame.pack(side="bottom", fill="x")
        ttk.Button(button_frame, text="Remove Selected", command=remove_selected).pack(side="left")
        ttk.Button(button_frame, text="Clear Pallet", command=clear_pallet).pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(button_frame, text="Preview Barcode", command=preview_barcode).pack(
            side="left", padx=(20, 0)
        )
        ttk.Button(button_frame, text="Generate Pallet Label", command=generate_pallet_label).pack(
            side="left", padx=(8, 0)
        )

        def return_to_main_screen():
            if scanned_cartons and not messagebox.askyesno(
                "Discard scanned cartons?",
                f"{len(scanned_cartons)} scanned carton(s) haven't been generated yet - "
                "leaving now discards them (nothing is saved to the database). Continue?",
                parent=win,
            ):
                return
            win.destroy()

        ttk.Button(button_frame, text="Return to Main Screen", command=return_to_main_screen).pack(
            side="right"
        )
        win.protocol("WM_DELETE_WINDOW", return_to_main_screen)

        scan_entry.focus_set()

    # --- about / setup ---------------------------------------------------

    def _show_about(self):
        win = tk.Toplevel(self)
        win.title("About BarBell")
        win.resizable(False, False)

        frame = ttk.Frame(win, padding=15)
        frame.pack()

        if self._about_barbell_logo is not None:
            ttk.Label(frame, image=self._about_barbell_logo).pack(pady=(0, 10))
        if not self._using_wordmark_about:
            ttk.Label(frame, text="BarBell", font=("", 14, "bold")).pack()

        if self._about_clc_logo is not None:
            ttk.Label(frame, image=self._about_clc_logo).pack(pady=(0, 10))

        ttk.Label(frame, text=APP_DESCRIPTION, justify="center").pack(pady=10)
        ttk.Label(frame, text="© 2026 Caribbean Label Crafts Ltd.").pack()
        ttk.Label(frame, text="Designed by: Greg Coles").pack()
        ttk.Label(frame, text=f"Version: {version_string()}").pack()
        ttk.Label(frame, text=f"Build date: {BUILD_DATE}").pack(pady=(0, 15))

        ttk.Button(frame, text="Setup...", command=self._prompt_setup_password).pack()

    def _prompt_setup_password(self):
        entered = simpledialog.askstring(
            "Setup", "Enter the setup password:", show="*", parent=self
        )
        if entered is None:  # cancelled
            return

        settings = load_settings()  # reload in case it changed since app start
        if not check_setup_password(entered, settings):
            messagebox.showerror("Incorrect password", "That password is incorrect.")
            return

        subprocess.Popen([sys.executable, str(APP_ROOT / "setup_gui.py")], cwd=str(APP_ROOT))


if __name__ == "__main__":
    load_dotenv()
    BarBellApp().mainloop()
