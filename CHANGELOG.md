# Changelog

Version and build date are tracked in a single place, `src/version.py` -
never hardcoded anywhere else. See that file for the versioning rules.

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
