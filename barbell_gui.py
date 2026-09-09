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
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk

from dotenv import load_dotenv

from src.barcode_render import render_barcode_image
from src.batch import build_batch_number
from src.db.readonly_connection import ReadOnlyConnection
from src.gs1 import (
    build_contents_barcode_data,
    build_contents_element_string,
    build_sscc_barcode_data,
    build_sscc_element_string,
)
from src.gtin import InvalidGTINError, normalize_gtin
from src.labels import (
    assemble_label_rows,
    get_product_info,
    list_packing_slip_line_items,
    list_packing_slips_for_job,
)
from src.settings import load_settings
from src.sscc import SSCCGenerator, build_sscc, build_test_sscc, get_counter_status

APP_ROOT = Path(__file__).resolve().parent
ICON_PATH = APP_ROOT / "assets" / "barbell_icon.png"  # square icon-only mark, used for the taskbar icon
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
        self.title("BarBell")
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
        self._gtin_override = None

        self._load_logos()
        self._build_widgets()

    # --- setup ---------------------------------------------------------

    def _load_logos(self):
        # Taskbar icon stays the square icon-only mark, not the wordmark.
        self._taskbar_icon = load_scaled_or_none(ICON_PATH, 32)
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
        header = ttk.Frame(self, padding=10)
        header.grid(row=0, column=0, sticky="ew")
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
        job_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        ttk.Label(job_frame, text="Job number:").grid(row=0, column=0, sticky="w")
        self.job_number_var = tk.StringVar()
        ttk.Entry(job_frame, textvariable=self.job_number_var, width=20).grid(
            row=0, column=1, sticky="w", padx=5
        )
        ttk.Button(job_frame, text="Find Packing Slips", command=self._load_packing_slips).grid(
            row=0, column=2
        )

        slip_frame = ttk.LabelFrame(self, text="2. Packing Slip", padding=10)
        slip_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.slip_listbox = tk.Listbox(slip_frame, width=90, height=6, exportselection=False)
        self.slip_listbox.grid(row=0, column=0, sticky="ew")
        self.slip_listbox.bind("<<ListboxSelect>>", self._on_slip_selected)

        product_frame = ttk.LabelFrame(self, text="3. Product (a packing slip can carry more than one)", padding=10)
        product_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.product_listbox = tk.Listbox(product_frame, width=90, height=4, exportselection=False)
        self.product_listbox.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.product_listbox.bind("<<ListboxSelect>>", self._on_product_selected)

        self.gtin_status_label = ttk.Label(product_frame, text="")
        self.gtin_status_label.grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.enter_gtin_button = ttk.Button(
            product_frame, text="Enter GTIN...", command=self._enter_gtin, state="disabled"
        )
        self.enter_gtin_button.grid(row=1, column=1, sticky="e", pady=(8, 0))

        pkg_frame = ttk.LabelFrame(self, text="4. Package Details", padding=10)
        pkg_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=5)

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
        ttk.Checkbutton(
            pkg_frame,
            text="Test mode (fake SSCCs - doesn't touch the real counter)",
            variable=self.test_mode_var,
        ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))

        action_frame = ttk.Frame(self, padding=10)
        action_frame.grid(row=5, column=0, sticky="ew")
        ttk.Button(action_frame, text="Preview Barcode", command=self._preview_barcode).pack(side="left")
        ttk.Button(action_frame, text="Generate Labels", command=self._generate).pack(side="left", padx=(8, 0))
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
            with ReadOnlyConnection() as conn:
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

    def _reset_product_selection(self):
        self.product_listbox.delete(0, tk.END)
        self._line_items = []
        self._selected_line_item = None
        self._product = None
        self._gtin_override = None
        self.gtin_status_label.config(text="")
        self.enter_gtin_button.config(state="disabled")

    def _on_slip_selected(self, _event):
        selection = self.slip_listbox.curselection()
        if not selection:
            return
        self._selected_slip = self._slips[selection[0]]
        self._reset_product_selection()

        try:
            with ReadOnlyConnection() as conn:
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
        self._gtin_override = None

        try:
            with ReadOnlyConnection() as conn:
                product = get_product_info(conn, self._selected_line_item.product_number)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Lookup failed", str(exc))
            self._product = None
            return

        self._product = product
        if product.gtin:
            self.gtin_status_label.config(text=f"GTIN on file: {product.gtin}")
            self.enter_gtin_button.config(state="disabled")
        else:
            self.gtin_status_label.config(
                text=f"No GTIN on file for item {product.item_number} - "
                "enter one below, or add it in Label Traxx first."
            )
            self.enter_gtin_button.config(state="normal")

    def _enter_gtin(self):
        if self._product is None:
            return
        raw = simpledialog.askstring(
            "Enter GTIN", f"GTIN for item {self._product.item_number}:", parent=self
        )
        if raw is None:  # cancelled
            return
        try:
            gtin = normalize_gtin(raw)
        except InvalidGTINError as exc:
            messagebox.showerror("Invalid GTIN", str(exc))
            return

        self._gtin_override = gtin
        self.gtin_status_label.config(text=f"GTIN entered for this run: {gtin} (not saved to Label Traxx)")

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
        if not self._product.gtin and not self._gtin_override:
            messagebox.showerror(
                "GTIN required",
                "Enter a GTIN for this run, or add it in Label Traxx first, before generating labels.",
            )
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

        gtin = self._gtin_override or self._product.gtin
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
            with ReadOnlyConnection() as conn:
                rows = assemble_label_rows(
                    conn=conn,
                    sscc_generator=gen,
                    job_number=job_number,
                    line_item=line_item,
                    units_per_package=units_per_package,
                    labels_per_package=labels_per_package,
                    production_date=production_date,
                    gtin_override=self._gtin_override,
                    test_mode=test_mode,
                )
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Generation failed", str(exc))
            return

        out_path = self._write_csv(rows, job_number, packing_slip_number, test_mode=test_mode)
        packages_used = len({r.sscc for r in rows})
        messagebox.showinfo(
            "Labels generated",
            f"Wrote {len(rows)} label row(s) covering {packages_used} package(s) to:\n{out_path}",
        )

    def _write_csv(self, rows, job_number, packing_slip_number, test_mode=False) -> Path:
        import csv

        output_dir = Path(self.settings.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        suffix = "_TEST" if test_mode else ""
        out_path = output_dir / f"labels_{job_number}_{packing_slip_number}{suffix}.csv"
        fieldnames = [
            "JobNumber", "PackingSlipNumber", "CustomerNumber", "CustomerName", "ProductNo",
            "ItemNumber", "ItemDescription", "Quantity", "Batch", "ProductionDate",
            "SSCC", "GTIN", "PackageIndex", "LabelCopyIndex",
        ]
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            for r in rows:
                writer.writerow(
                    [
                        r.job_number, r.packing_slip_number, r.customer_number, r.customer_name,
                        r.product_no, r.item_number, r.item_description, r.quantity, r.batch,
                        r.production_date, r.sscc, r.gtin or "", r.package_index, r.label_copy_index,
                    ]
                )
        return out_path

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
        ttk.Label(frame, text="Designed by: Greg Coles").pack(pady=(0, 15))

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
