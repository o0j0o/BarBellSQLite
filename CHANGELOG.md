# Changelog

Version and build date are tracked in a single place, `src/version.py` -
never hardcoded anywhere else. See that file for the versioning rules.

## 1.1.17 Beta - 2026-11-10

- **Setup password can be changed from Setup.** A new "Setup Password" section has **New password** and
  **Confirm password** boxes, each with an eye icon that shows/hides what is typed. At least 6 characters, typed
  twice. It changes only the standard Setup password (still `change4GOOD` until someone changes it - nothing was
  changed in this release); the Admin (Greg) password is fixed and untouched. The new password is saved only as a
  salted PBKDF2 hash in the SQLite database (new `setup_credentials` table), never as plain text.
- **Reset to Default** (same section) puts the original Setup password back. It needs the Admin password - asked
  for on the spot, or just a confirmation if Setup was already opened with it.
- Restoring an older database backup also restores that backup's Setup password.
- **New Job Report screen.** Type a Job Number (exact match) and see every pallet - its SSCC barcode and number plus the
  GS1-128 text (GTIN, description, production date, pallet quantity, batch, cartons on the pallet) - with its
  cartons listed beneath (SSCC, description, production date, quantity per carton, batch). Cartons on no pallet
  come last under "No Associated Pallet SSCC". An unknown job shows "Job is Not in BarBell". Voided pallets and
  cartons are left out. Read entirely from BarBell's own SQLite data - no Label Traxx or ODBC. Shown on screen
  and exported to a US Letter landscape PDF (`Job_report_<job>.pdf` in the output folder), in the Pallet Report's style.
- The Job Report opens from **Home > Job Report...** and from a **Job Report** button next to Pallet Report (PDF)
  on the Job/Label History form (pre-filled with the checked rows' job, or the Job No box).
- Operator Guide updated with both features and screenshots (made from a dummy database).
- Job Report fix: it listed only one carton per SSCC, so a job made in Test mode several times (whose test SSCCs
  restart at TEST-SSCC-00001 each run) showed 5 of its 11 cartons. It now lists every carton label logged for the
  job (one per label printed in a run; extra print copies and reprints still count once, voided labels are left out).
- Job Report for jobs with several products: the carton table is now **# | Carton SSCC | Description | GTIN |
  Production Date (centred) | Qty per Carton | Batch (Job No. - P/N)**. The page header no longer shows GTIN, Item or
  Batch (they belong to each carton, not the job).
  Every label now saves its own product (item number, description, GTIN, batch, P/N) when it is logged - before,
  only the job's *latest* run was kept, so a job run for Coconut, Coffee and plain Rum Cream showed all of them
  as one product. New `labels` columns are added automatically the first time a database is opened (the file is
  backed up first, as for earlier upgrades). A pallet takes its product from its cartons; reprints copy it.
  Labels logged before this version have no saved product and still show the job's latest run's product.
- Job Report: cartons under "No Associated Pallet SSCC" are grouped by product, each with a small header (description,
  GTIN, batch, number of cartons and total quantity). A product that runs onto a new page repeats its header.

## 1.1.16 Beta - 2026-11-06

- Job/Label History: the list is now short by default. It shows the **last 90 days** of **real** labels;
  a new **Show** box (30 days / 90 days / 6 months / year / All history), a **Hide test labels** checkbox
  (ticked by default) and a **Show all history** button change that. A line at the bottom says exactly what is
  hidden - e.g. "Showing 22 of 1,086 label row(s). Hidden: 1,064 test label(s)." The age is when the label was
  logged. On the development database this takes the list from 1,086 rows to 22 (1,064 of the rows were test labels).
- **Searching always covers all history, test labels included.** Typing in Job No, Date or SSCC contains ignores
  the period and the Hide-test checkbox (they grey out while a search is active), so a box that comes back for
  rework months after it shipped is found by its SSCC. Clearing the search returns to the short list.
- Installer package renamed **BarBell-Setup-1.2.1-Beta.exe** (the 1.2.0 package had already been tried out); it
  includes this History filter. The development copy stays on 1.1.x.
- Nothing is deleted or moved: this only limits what is listed. `fetch_label_history()` takes `since_days` and
  `hide_test`, and `count_label_history()` gives the matching counts used for the "hidden" line.

## 1.1.15 Beta - 2026-11-04

- Installer build: the finished `BarBell-Setup-1.2.0-Beta.exe` is now copied to `installer/Output/` in the
  project (git-ignored) so it can actually be found and handed out. It used to be left in
  `%LOCALAPPDATA%\BarBellBuild\Output`, which - when built from inside the Claude desktop app - Windows silently
  redirects into the app's private storage, so File Explorer reported "Location is not available". The test
  script looks in `installer\Output` first.

## 1.1.14 Beta - 2026-11-04

- Windows installer (`installer/`), producing **BarBell-Setup-1.2.0-Beta.exe** - the production package is
  labelled 1.2.0 Beta; this development copy stays on 1.1.x (the build stamps the version into a staged copy
  only). Built with PyInstaller (the app and a small helper) and Inno Setup. Windows 11 only. Wizard: a
  Label Traxx ODBC check/prompt, the install folder (default `C:\BarBell`), detection of an existing
  installation with a verified backup of its database and both SSCC counters *before anything is changed*, a
  keep / restore-from-file-or-backup / start-blank choice, and the Label Traxx login. Desktop and Start menu
  icons use BarBell's own icon. Uninstalling never removes the data or the backups. See `installer/README.md`.
- The app now runs correctly when installed as an .exe: data (settings.json, barbell.db, counters, .env) lives
  in `<install folder>\data` (`src/paths.py`; from source nothing changes), Setup is started with
  `BarBell.exe --setup`, and `--version` / `--selftest FILE` exist for checks. BarBell also names itself with a
  mutex so the installer asks to close it before upgrading.
- `src/installer_support.py`: the data logic the installer calls - find an existing install (installed layout or
  a manual copy), verified pre-install backup (raw copy if the database is too damaged to verify), restore
  from a backup folder or a bare database file (checked first), start blank. A counter never moves backwards.
- `installer/test_installer.ps1` runs the installer unattended (install and start, upgrade keeps data, restore
  paths, uninstall keeps data).
- The installer and `BarBell.exe` are unsigned, which security software such as CylancePROTECT blocks - see
  `installer/README.md`.

## 1.1.13 Beta - 2026-11-04

- Help > Help now opens the BarBell Operator Guide in the PC's default web browser
  (it was a placeholder window). The address lives in one place, `HELP_URL` in
  `src/help_link.py`; a machine can point somewhere else with `help_url` in
  `settings.json` (only http/https addresses are ever used - anything else is ignored).
  If no browser can be opened, BarBell shows the address and copies it to the clipboard
  instead. Contacts is still a placeholder.

## 1.1.12 Beta - 2026-11-04

- Contents barcode AIs now follow the customer's rules. **Carton label:** (01) GTIN,
  (11) production date, (37) count in the carton, (10) batch. **Pallet label:** (02) GTIN,
  (11) production date, (37) total count of product on the pallet (product, not cartons),
  (10) batch - and a pallet label is only made for a pallet holding all the same product.
  The main screen's Preview Barcode window and the Generate Labels confirmation box (and the
  command-line preview) are about cartons, so they now show (01) and (37); they used to list
  (02) and (37). The pallet screen's preview is unchanged. `src/gs1.py` takes the GTIN AI
  as `gtin_ai` (`GTIN_AI_CARTON` "01" / `GTIN_AI_PALLET` "02", default "02"). The Pallet Report's
  small per-carton contents barcodes still use the default (02) - not changed here.

## 1.1.11 Beta - 2026-11-04

- Pallet Labels: the last scan message no longer stays on the screen after a pallet is
  generated. Previously a red message from an earlier mis-scan (for example "That is the
  contents barcode...") was still showing on the fresh, empty screen. It is cleared when
  the pallet is successfully generated; backing out of the confirmation leaves it as is.

## 1.1.10 Beta - 2026-11-04

- Setup form: the form now scrolls (scrollbar on the right, mouse wheel works), so the
  whole thing is reachable on a short screen. The window opens sized to fit the screen,
  and **Save Settings is pinned to the bottom** so it's always visible.
- Setup form: the explanatory notes (Plant, Demo Mode, Disable Test Mode, Backup) now
  wrap to the full width of their section instead of a narrow hand-broken column, so
  they take fewer lines.

## 1.1.9 Beta - 2026-11-04

- Backup and restore (`src/backup.py`). A backup is one timestamped folder holding a
  consistent set: the SQLite database (copied with SQLite's own online-backup call,
  so it's safe even if another process has it open), **both SSCC counter files**,
  `settings.json` and the GTIN audit log, plus a `manifest.json` with SHA-256 hashes.
- BarBell backs up automatically when it closes (Home > Exit, or the window's X) and
  on **Home > Back Up Now**. It keeps the newest 10 (`Settings.backup_keep_count`),
  skips a backup when nothing has changed since the last one (so repeated open/close
  doesn't push older, different backups out), and never prunes before the new backup
  has passed an integrity check - a failing backup can't rotate good ones away. A
  failed backup on exit asks "Exit anyway?" so it never traps you in the app. Off in
  Demo Mode, and off until a backup directory is set.
- Setup: new "Backup and Restore" section - **Backup directory** field with Browse,
  **Back Up Now**, and **Restore from Backup...** (browse to a backup folder; shows
  what will change before asking; needs the administrator Setup password). Saving a
  backup directory inside OneDrive asks first, since OneDrive syncing a live database
  can corrupt it.
- Restore rules: the backup is verified first (hashes + integrity check); a safety
  backup of the current data is taken; the database is restored; and **no SSCC
  counter is ever moved backwards** - each ends at the highest of the backup's, the
  live file's, and the highest serial found in the restored database. Settings and the
  audit log are kept in backups for manual recovery but are not overwritten by a
  restore.

## 1.1.8 Beta - 2026-11-04

- Main screen: the CLC and LCJ logos are removed from the header, leaving only the
  "Making Ideas Take Shape!" logo (same size, right edge). The About screen now shows
  the LCJ logo beside the CLC logo.
- Menu bar: the top-level items are now **Home** (Setup, Exit) and **Help** (Help,
  Contacts, About). Setup and Exit behave exactly as before - they just moved under
  Home.

## 1.1.7 Beta - 2026-11-04

- Menu bar across the top of the main form: **Setup**, **Exit**, **Help** (Help,
  Contacts, About). The About button at the bottom of the main form is gone - About
  is reached from the Help menu. Exit asks "Are you sure you want to exit BarBell?"
  and only closes on Yes. Help and Contacts are placeholder screens for now (there
  was no existing help content).
- Setup is now also a top-level menu item. It and the Setup button on the About
  screen (unchanged) call the same method, so the password prompt and everything
  after it behave identically.
- Second Setup password. The existing one (`change4GOOD`, from `settings.json`) works
  exactly as before; the second also opens Setup and additionally shows "Welcome
  Greg". Setup is told which level was used (`SetupAccessLevel.Standard`/`Admin`,
  passed to `setup_gui.py` as `--access-level`) so it can branch on it later - both
  levels get identical Setup functionality for now. Both passwords are defined only
  in `src/setup_access.py`, and neither is ever logged or shown in a message.
- Setup: new "Disable Test Mode checkbox on main form" checkbox in the Demo Mode
  area (`Settings.disable_test_mode_checkbox`, saved with the other settings). When
  on, the main form's Test mode checkbox starts unchecked and greyed out; applied
  when the main form loads. Demo Mode still forces Test mode on and locked.
- Production date is now **YYMMDD** (4 Nov 2026 = `261104`) everywhere: entered
  (main form, CLI), validated (`src/dates.py`), stored (SQLite), shown (pallet
  screens, report), exported (CSV `ProductionDate` column), and in the AI (11)
  barcode (which was already YYMMDD). Existing databases are converted in place the
  first time they're opened (the `.db` file is backed up first); old YYYY-MM-DD
  values are still understood everywhere, so nothing reads them wrong.
- Main-form header: LCJ logo on the left in line with the CLC logo, and the "Making
  Ideas Take Shape!" logo directly under CLC, all in the header's existing height
  (logos rescaled with high-quality resampling, aspect ratio kept). New assets:
  `assets/lcj_logo.png`, `assets/making_ideas_logo.png` (the "Making Ideas Take Shape!" wordmark).

## 1.1.6 Beta - 2026-10-26

- Job/Label History: Reprint Selected, Void Pallet and Pallet Report (PDF) now sit on
  their own "Checked rows:" row under the filters. On one line with them they ran past
  the right edge of the window at its default width, hiding Void Pallet and Pallet
  Report unless the window was widened.
- Pallet Report: a long batch number now shrinks to fit its column instead of running
  into the contents barcode beside it. (Real 11-digit batches already fit; this guards
  longer product numbers.)

## 1.1.5 Beta - 2026-10-26

- Pallet Report: the company name is now printed above the title on every page -
  "Caribbean Label Crafts Ltd." when Setup's Plant is Barbados, "Label Crafts Jamaica
  Ltd." when it's Jamaica (`Settings.company_name`, same plant signal as the SSCC
  config). Each carton's SSCC number now has its own GS1-128 SSCC barcode directly
  beneath it, 7.5 mm tall with no human-readable line (the digits are already printed
  above it); test-mode placeholder SSCCs can't be encoded and get no barcode.

## 1.1.4 Beta - 2026-10-23

- Pallet Report is now US Letter (8.5" x 11", landscape) instead of A4, with the
  table columns narrowed to fit the slightly shorter page width.

## 1.1.3 Beta - 2026-10-23

- Pallet Labels: added a "Select Carton SSCC..." button as a fallback for when the
  scanner isn't working (scanning stays the default). It opens a list of every carton
  not yet on a pallet - SSCC, description, batch, quantity, job, production date -
  filterable by job number and SSCC fragment; check one or more and "Add Selected to
  Pallet". Cartons already on a pallet or voided never appear, only cartons of the
  same kind as the pallet (test vs. production) are listed, and once the pallet has a
  carton the list narrows to that carton's batch/GTIN. Picked cartons go through the
  exact same checks and confirmations as a scan (same code path), so nothing can be
  added by hand that a scan would have blocked. Like the scan box, the button is
  enabled once an expected carton count is entered.

## 1.1.2 Beta - 2026-10-23

- Added the Pallet Report: in Job/Label History, check a pallet's row (or any carton
  already on it) and click "Pallet Report (PDF)" to get an A4-landscape PDF of the
  pallet's contents, saved to the output folder as `Pallet_report_<pallet SSCC>.pdf`
  and opened automatically. The top of the first page carries the pallet's SSCC
  barcode (a smaller copy repeats on every later page) with its job, packing slip,
  production date, carton count and total quantity; below, one row per carton shows
  its SSCC, description, quantity, batch, and a small GS1-128 contents barcode
  (`(02)(11)(37)(10)`) built by the same code as the carton's own label. Multi-page
  for large pallets, with a totals row at the end. Test-mode pallets print a "TEST
  PALLET" placeholder in place of the pallet barcode, since a fake SSCC can't be
  encoded. A voided pallet is refused (a void frees all its cartons). Pages are
  drawn with Pillow - no new dependency - so the text isn't selectable in the PDF.

## 1.1.1 Beta - 2026-09-25

- Fixed a silent CSV write failure in Generate Labels (missed its own version bump
  when it shipped, corrected here): a write failure - most commonly the target file
  locked open in another program - was previously swallowed with no error shown,
  even though the labels had already been logged to the database. Now caught and
  surfaced with a specific message.
- Added per-plant SSCC counters: Barbados and Jamaica each get their own GS1 Company
  Prefix, extension digit, and counter file (`Settings.jamaica_*`), selected by the
  same Plant dropdown Setup already uses for the Label Traxx DSN. Switching the
  dropdown swaps the whole GS1/SSCC Configuration section (labeled "Editing:
  Barbados"/"Editing: Jamaica") and the counter status shown below it; saving only
  touches whichever plant is currently selected, never the other one. Every SSCC
  BarBell issues - carton generation, pallet generation, the CLI - now resolves the
  *active* plant's config via `Settings.active_gs1_company_prefix`/
  `active_sscc_extension_digit`/`active_sscc_state_file` rather than one fixed set
  of fields. Allocation: Barbados uses even extension digits (0, then 2/4/6/8 once
  a digit's 100,000-serial range is exhausted), Jamaica uses odd (1, then 3/5/7/9) -
  Greg's scheme, fully GS1-compliant and collision-proof by construction since the
  extension digit is the first digit of every SSCC. See QUESTIONS.md #19.

## 1.1.0 Beta - 2026-09-25

- Added Pallet Labels: scan-to-build pallet labels for mono-lot (one product, one
  batch) pallets, using a Bluetooth barcode scanner as a keyboard wedge. New
  "Pallet Labels..." button on the home screen opens a screen to enter the
  expected carton count, scan each carton's SSCC (cleaned up and validated -
  AIM prefix/GS-FNC1/AI-prefix stripped, 18 digits, valid GS1 check digit, a
  specific message if the contents barcode was scanned by mistake), and see
  a running grid/totals. Scans are checked against BarBell's own label history:
  blocked outright if the SSCC isn't found, belongs to a pallet already, is
  voided, is already on another pallet, is a duplicate on this pallet, has a
  different GTIN/batch, the expected count is already reached, or it mixes
  test and production cartons; warned-and-confirmed if the production date,
  packing slip, or printing plant differs from the first carton scanned (the
  pallet uses the earliest production date). Generate Pallet Label allocates a
  new SSCC from the same counter/extension digit cartons use, links every
  scanned carton to it, and writes a `Pallet_labels_<job>_<sscc>.csv` in one
  DB transaction before the CSV is attempted - a failed CSV write never burns
  a second SSCC, since the pallet row (and its SSCC) is already safely saved
  and can be re-exported via Job/Label History's existing Reprint. Preview
  Barcode shows the pallet's contents barcode without reserving an SSCC.
- Pallets are rows in the existing `labels` table (`label_type` CARTON/PALLET),
  not a separate table - `pallet_sscc` links a carton to its pallet,
  `carton_count` records how many cartons a pallet actually carries. Added
  per-row `production_date`/`packing_slip_number` snapshots (previously only
  on `jobs`, one value per job number) so a carton's own history is preserved
  even if its job is later regenerated with different values - needed for the
  pallet screen's differs-from-the-rest checks to mean anything. Migration is
  additive, backfills pre-existing rows best-effort from their current jobs
  row, and backs up the `.db` file first - see QUESTIONS.md #18.
- Job/Label History: added Pallet SSCC and Label Type columns; searching by a
  pallet's SSCC now also finds its cartons. New "Void Pallet" action marks a
  pallet's rows void in place and frees its cartons to be re-scanned onto a
  rebuilt pallet - the SSCC itself is never reused.
- Built on branch `pallet-labels`, not merged to `main`.

## 1.0.5 Beta - 2026-09-24

- Added multi-plant Label Traxx support: a "Label Traxx Connection" section in
  Setup with a "Plant" dropdown - "Barbados (LT64)" / "Jamaica (LCJ JAM)" -
  selects which Windows ODBC DSN BarBell connects with. `Settings.label_traxx_dsn`
  (empty by default - falls back to `LT_DSN` from `.env`, so an untouched
  install keeps working unchanged); username/password are unaffected, both
  plants share the same Label Traxx login. Both DSNs must already exist in a
  given machine's ODBC Data Source Administrator - Setup only picks between
  them, it doesn't create them. Takes effect on next BarBell start. See
  QUESTIONS.md #17.

## 1.0.4 Beta - 2026-09-21

- Job/Label History: added vertical and horizontal scrollbars (the vertical one
  was being pushed off-screen by the wide table; the grid now uses a proper
  grid layout, columns keep their width, and the SSCC column no longer clips).
  Added a live "SSCC contains:" search box - case-insensitive substring match
  against the full SSCC as you type (GS1 prefix, sequence number, or a fragment
  spanning both; the full number is never required). Combines with the Job No
  and Date filters, cleared by "Clear filters", and - like any new search -
  clears ticked checkboxes. `fetch_label_history()` gained `sscc_contains`
  (LIKE wildcards in the typed text are escaped, so they match literally).

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
