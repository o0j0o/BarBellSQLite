# Changelog

Version and build date are tracked in a single place, `src/version.py` -
never hardcoded anywhere else. See that file for the versioning rules.

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
