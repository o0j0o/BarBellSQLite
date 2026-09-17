# Changelog

Version and build date are tracked in a single place, `src/version.py` -
never hardcoded anywhere else. See that file for the versioning rules.

## 1.0.3 Beta - 2026-09-16

- Job/Label History screen now supports selecting rows and reprinting them to CSV.
  A checkbox column (leftmost) lets you check individual rows; the header
  checkbox selects/deselects all *currently filtered/visible* rows only. A new
  "Reprint Selected (Export to CSV)" button confirms the count, writes the
  selected rows to a `reprint_<timestamp>.csv` (`DEMO_` prefixed in Demo Mode)
  using the same Jobs+Labels join/flatten as normal CSV export, and logs one new
  `labels` row per selection with `status='reprint'` and `superseded_id` pointing
  back at the original - the original row is never changed or deleted. Running a
  new search/filter clears all checkboxes (including select-all) so a stale
  selection can't carry over. `src/db/local_store.py` gained
  `create_reprint_rows()` and a shared `write_flat_csv()`/`CSV_FIELDNAMES` that
  `generate_labels.write_csv()` and `BarBellApp._write_csv()` now both delegate to,
  so the flat CSV format is defined in exactly one place. See QUESTIONS.md #16.

## 1.0.2 Beta - 2026-09-16

- Added Demo Mode (`Settings.demo_mode`, "Run as Demo" checkbox in `setup_gui.py`) -
  runs BarBell entirely on local, self-contained sample data (`src/demo_data.py`: a
  handful of obviously-fake DEMO- jobs/packing slips/products, including a
  multi-product packing slip and a product with no GTIN on file) with zero Label
  Traxx/ODBC or network calls, for demoing the app somewhere with no access to
  either. `DemoConnection` is a drop-in stand-in for `ReadOnlyConnection` - none of
  `src/labels.py`'s business logic changed. While on: SSCCs are always the existing
  fake `TEST-SSCC-#####` placeholders (never the real counter), CSVs are prefixed
  `DEMO_`, and the Jobs/Labels DB + GTIN audit log are written to separate
  `demo_*` files - real data is never touched. The main window shows an unmissable
  red "DEMO MODE" banner and title-bar tag whenever it's on, and the Test Mode
  checkbox is forced on and locked. `generate_labels.py` (the CLI) supports it too.
  See QUESTIONS.md #15. Also fixes a pre-existing bug in `setup_gui.py`'s Save:
  it was rebuilding `Settings` from only the fields shown in that dialog, silently
  resetting every other setting (password, audit log path, DB path, etc.) to its
  default on every save.

## 1.0.1 Beta - 2026-09-14

- Added a local SQLite database (`src/db/local_store.py`, `barbell.db` - gitignored)
  with a `jobs` table (one row per Job No, upserted per run: packing slip, P/N, item
  number, batch, production date, customer, GTIN used, package sizing, test-mode flag)
  and a `labels` table (one row per label actually written to a CSV: auto-increment id,
  Job No FK, SSCC, carton sequence, label copy index, quantity, status
  original/void/reprint, nullable superseded_id for reprint history, timestamp).
  CSV export now sources its rows from a Jobs+Labels join instead of directly from the
  in-memory generation result - the CSV format on disk is unchanged. Added a
  "Job/Label History..." screen (next to About) to browse logged jobs/labels, filterable
  by Job No and/or date. See QUESTIONS.md #14.

## 1.0.0 Beta - 2026-09-14

- Version reset to mark the start of the SQLite-backed rewrite (Greg's
  instruction). No functional change in this commit - the pre-reset history
  (0.1.0-0.1.4 Beta) is preserved in git and tagged `BarBellSQLite`, and a
  full folder snapshot was saved to `BarBell_v1_backup` before this point.
  New GitHub repo: https://github.com/o0j0o/BarBellSQLite.

## 0.1.4 Beta - 2026-09-10

- The "No GTIN on file" warning (dialog box, status label, and the CLI
  equivalent) now names the Product No (P/N) instead of the item number,
  matching how the operator identifies the product on the packing slip.
  The `require_valid_gtin()` blocking message was likewise simplified to
  reference the P/N only.

## 0.1.3 Beta - 2026-09-10

- Amendment to item 3: manual GTIN entry is available for every run while in
  Beta (`Settings.allow_manual_gtin_override`, default True), not only when
  `Product.BC_Start` is empty - CLC is still registering GTINs into Label
  Traxx. A valid BC_Start is prefilled as the default and can be accepted or
  overridden; overriding requires explicit confirmation showing both values.
  Every run is recorded in a new audit log (`src/audit.py`,
  `gtin_audit_log.jsonl`) naming the BC_Start value, the value used, the
  source (Label Traxx / manual entry / override), username, and timestamp.
  See QUESTIONS.md #13 - revisit before 1.0.0.

## 0.1.2 Beta - 2026-09-10

- Item 3: GTIN is now sourced from `Product.BC_Start` ("Barcode Start"),
  validated (empty/non-numeric/wrong-length/bad-checksum), and blocking -
  no more manual "enter a GTIN for this run" override. As a consequence,
  item 1's bold-digit styling (which only applied to that now-removed line)
  was removed along with it - see QUESTIONS.md #12.

## 0.1.1 Beta - 2026-09-10

- Item 1: GTIN digits on the "entered for this run" line now render in bold
  (prefix, "(not saved to Label Traxx)" note, and layout/spacing unchanged).

## 0.1.0 Beta - 2026-09-10

- Added version tracking (`src/version.py`), displayed in the About dialog
  below "Designed by: Greg Coles", and this changelog.
