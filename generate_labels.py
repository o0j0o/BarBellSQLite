"""
Interactive CLI: walks through the BarBell label-generation flow and writes a
CSV of GS1-128 logistics label rows for BarTender.

Flow:
  1. Job number
  2. Pick a packing slip for that job (all packing slips tied to the job via
     PackingSlip.TicketNum)
  3. A packing slip can carry multiple products - pick ONE (ProductNo + description)
  4. GTIN comes from Product.BC_Start ("Barcode Start"), but while
     Settings.allow_manual_gtin_override is True (the Beta default - CLC is still
     registering GTINs into Label Traxx), manual entry is always available: a valid
     BC_Start is offered as the default (press Enter to accept, or type a different
     value - which asks for explicit confirmation before proceeding), and an empty
     BC_Start prompts for one directly. Validation is unchanged either way. Every run
     is recorded in the audit log (src/audit.py). See QUESTIONS.md #4/#12/#13.
  5. Units per package (manual - Label Traxx doesn't record physical packaging)
  6. Logistics labels per package (manual - e.g. 2 for a pallet needing labels
     on both sides, 1 for a carton)
  7. Production date to print on the label (manual - see QUESTIONS.md #3)
  8. Shows the actual GS1-128 element string(s) that will be encoded, before
     anything is generated

Each physical package gets ONE SSCC, issued for real and never reused -
issuing SSCCs is the one irreversible step here, so this confirms the summary
before calling assemble_label_rows().

Run with:
    python generate_labels.py
"""

import csv
import datetime
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.batch import build_batch_number
from src.db.local_store import record_generation_run
from src.db.readonly_connection import ReadOnlyConnection
from src.gs1 import build_contents_element_string, build_sscc_element_string
from src.gtin import GTIN_SOURCE_MANUAL_OVERRIDE, InvalidGTINError, classify_gtin_source, normalize_gtin
from src.labels import (
    assemble_label_rows,
    get_product_info,
    list_packing_slip_line_items,
    list_packing_slips_for_job,
)
from src.settings import load_settings
from src.sscc import SSCCGenerator, build_sscc, build_test_sscc, get_counter_status


def prompt(text: str) -> str:
    value = input(text).strip()
    if not value:
        print("This field is required.")
        return prompt(text)
    return value


def prompt_int(text: str) -> int:
    raw = prompt(text)
    try:
        value = int(raw)
    except ValueError:
        print(f"{raw!r} is not a whole number.")
        return prompt_int(text)
    if value <= 0:
        print("Must be a positive number.")
        return prompt_int(text)
    return value


def prompt_date(text: str) -> str:
    raw = prompt(f"{text} (YYYY-MM-DD): ")
    try:
        datetime.date.fromisoformat(raw)
    except ValueError:
        print(f"{raw!r} isn't a valid date in YYYY-MM-DD format.")
        return prompt_date(text)
    return raw


def choose_packing_slip(conn, job_number: str):
    slips = list_packing_slips_for_job(conn, job_number)
    if not slips:
        print(f"No packing slips found for job {job_number!r}.")
        sys.exit(1)

    print(f"\nPacking slips for job {job_number}:")
    for i, slip in enumerate(slips, start=1):
        print(
            f"  {i}. {slip.number} (suffix {slip.suffix}) - {slip.customer_name} - "
            f"ship date {slip.ship_date} - qty {slip.ship_quantity} - "
            f"{slip.no_package} package(s) per Label Traxx"
        )

    choice = prompt_int(f"\nSelect a packing slip (1-{len(slips)}): ")
    while not (1 <= choice <= len(slips)):
        print(f"Enter a number between 1 and {len(slips)}.")
        choice = prompt_int(f"Select a packing slip (1-{len(slips)}): ")
    return slips[choice - 1]


def choose_product(conn, packing_slip_number: str):
    """A packing slip can carry multiple products - pick ONE to generate labels for."""
    items = list_packing_slip_line_items(conn, packing_slip_number)
    if len(items) == 1:
        return items[0]

    print(f"\nProducts on packing slip {packing_slip_number}:")
    for i, item in enumerate(items, start=1):
        print(f"  {i}. P/N {item.product_number} - {item.description} - qty {item.ship_quantity}")

    choice = prompt_int(f"\nSelect a product (1-{len(items)}): ")
    while not (1 <= choice <= len(items)):
        print(f"Enter a number between 1 and {len(items)}.")
        choice = prompt_int(f"Select a product (1-{len(items)}): ")
    return items[choice - 1]


def require_valid_gtin(product):
    """
    GTIN comes only from Product.BC_Start - no manual override. A missing or
    invalid value is a blocking error: print exactly what's wrong (which
    item, what's wrong, the raw value as found) and exit, rather than
    letting a run proceed on a bad GTIN.
    """
    if product.gtin:
        return

    print(
        f"\nBLOCKED - invalid GTIN in Label Traxx for P/N {product.prod_num} "
        f"({product.description}): {product.gtin_error}"
    )
    print(f'Value found in Label Traxx (Barcode Start): {product.gtin_raw!r}')
    print("Fix this in Label Traxx, then re-run. No SSCCs were issued.")
    sys.exit(1)


def resolve_gtin(product, settings) -> str:
    """
    Beta default (settings.allow_manual_gtin_override=True): manual entry is
    always available, not just when BC_Start is empty - CLC is still
    registering GTINs into Label Traxx, so it can't yet be treated as the
    sole authoritative source. A valid BC_Start is offered as the default
    (Enter accepts it); typing something different requires explicit
    confirmation, since that's the one case where the operator is knowingly
    overriding known data. Never returns without a valid GTIN.

    Once the flag is off, this reverts to require_valid_gtin()'s pure
    blocking behaviour - BC_Start only, no override, no code change needed.
    """
    if not settings.allow_manual_gtin_override:
        require_valid_gtin(product)
        return product.gtin

    if product.gtin:
        raw = input(f"GTIN [{product.gtin_raw}] (Enter to accept): ").strip()
        if not raw:
            raw = product.gtin_raw
    else:
        print(
            f"\nNo GTIN on file in Label Traxx for P/N {product.prod_num} "
            f"({product.description})."
        )
        raw = prompt("GTIN: ")

    while True:
        try:
            normalized = normalize_gtin(raw)
            break
        except InvalidGTINError as exc:
            print(str(exc))
            raw = prompt("GTIN: ")

    if classify_gtin_source(product.gtin, normalized) == GTIN_SOURCE_MANUAL_OVERRIDE:
        print(
            f"\nLabel Traxx has GTIN {product.gtin} on file for this item.\n"
            f"You are about to use {normalized} instead - this will NOT be saved "
            "back to Label Traxx."
        )
        confirm = input("Continue with the different value? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled - no SSCCs were issued.")
            sys.exit(0)

    return normalized


def print_gs1_preview(gtin, production_date, first_package_qty, batch, sscc):
    print("\nGS1-128 element strings for package 1:")
    print(f"  Contents: {build_contents_element_string(gtin, production_date, first_package_qty, batch)}")
    print(f"  SSCC:     {build_sscc_element_string(sscc)}")


def write_csv(
    rows, output_dir: Path, job_number: str, packing_slip_number: str, test_mode: bool = False
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_TEST" if test_mode else ""
    out_path = output_dir / f"labels_{job_number}_{packing_slip_number}{suffix}.csv"
    fieldnames = [
        "JobNumber",
        "PackingSlipNumber",
        "CustomerNumber",
        "CustomerName",
        "ProductNo",
        "ItemNumber",
        "ItemDescription",
        "Quantity",
        "Batch",
        "ProductionDate",
        "SSCC",
        "GTIN",
        "PackageIndex",
        "LabelCopyIndex",
    ]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for r in rows:
            writer.writerow(
                [
                    r.job_number,
                    r.packing_slip_number,
                    r.customer_number,
                    r.customer_name,
                    r.product_no,
                    r.item_number,
                    r.item_description,
                    r.quantity,
                    r.batch,
                    r.production_date,
                    r.sscc,
                    r.gtin or "",
                    r.package_index,
                    r.label_copy_index,
                ]
            )
    return out_path


def main():
    load_dotenv()
    settings = load_settings()
    if not settings.gs1_company_prefix:
        print("GS1 Company Prefix isn't set yet - run setup_gui.py first.")
        sys.exit(1)

    test_mode = input("Test mode - no real SSCCs will be issued? [y/N]: ").strip().lower() == "y"

    job_number = prompt("Job number: ")

    with ReadOnlyConnection() as conn:
        slip = choose_packing_slip(conn, job_number)
        line_item = choose_product(conn, slip.number)
        product = get_product_info(conn, line_item.product_number)

        gtin = resolve_gtin(product, settings)

        units_per_package = prompt_int("Units per package: ")
        labels_per_package = prompt_int("Logistics labels per package: ")
        production_date = prompt_date("Production date")

        batch = build_batch_number(job_number, product.prod_num)
        first_package_qty = min(units_per_package, line_item.ship_quantity)

        if test_mode:
            preview_sscc = build_test_sscc(1)
        else:
            next_serial = get_counter_status(settings.sscc_state_file).next_serial or 0
            preview_sscc = build_sscc(
                settings.gs1_company_prefix, settings.sscc_extension_digit, next_serial
            )
        print_gs1_preview(gtin, production_date, first_package_qty, batch, preview_sscc)

        gen = None
        if test_mode:
            print(
                "\nTest mode - using fake TEST-SSCC-##### placeholders, "
                "not touching the real counter."
            )
        else:
            num_packages = -(-line_item.ship_quantity // units_per_package)  # ceil, confirmation only
            print(
                f"\nAbout to issue {num_packages} real SSCC number(s) for job {job_number}, "
                f"packing slip {slip.number} ({line_item.ship_quantity} units at "
                f"{units_per_package}/package). SSCCs can never be reused once issued."
            )
            confirm = input("Continue? [y/N]: ").strip().lower()
            if confirm != "y":
                print("Cancelled - no SSCCs were issued.")
                return

            gen = SSCCGenerator(
                settings.gs1_company_prefix,
                settings.sscc_extension_digit,
                settings.sscc_state_file,
            )

        rows = assemble_label_rows(
            conn=conn,
            sscc_generator=gen,
            job_number=job_number,
            line_item=line_item,
            units_per_package=units_per_package,
            labels_per_package=labels_per_package,
            production_date=production_date,
            gtin_override=gtin,
            audit_log_file=settings.audit_log_file,
            test_mode=test_mode,
        )

    flat_rows = record_generation_run(
        rows,
        units_per_package=units_per_package,
        labels_per_package=labels_per_package,
        test_mode=test_mode,
        db_path=settings.local_db_file,
    )

    out_path = write_csv(
        flat_rows, Path(settings.output_dir), job_number, slip.number, test_mode=test_mode
    )
    packages_used = len({r.sscc for r in rows})
    print(f"\nWrote {len(rows)} label row(s) covering {packages_used} package(s) to {out_path}")


if __name__ == "__main__":
    main()
