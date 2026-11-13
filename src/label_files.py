"""
The label CSV files BarTender Print Station reads.

BarTender needs to open the SAME file in the SAME folder every time, so the operator never has to
load a file. Real labels are therefore always written to exactly:

    carton_jwn_labels.csv      (carton labels)
    pallet_jwn_labels.csv      (pallet labels)

in the "CSV output directory" from Setup (that setting is never changed here).

Every time a new file is made, the file already there is first moved into an `archive` folder inside
that directory (created only if it is missing) and renamed with the date and time it was archived:

    archive\\carton_jwn_labels_20261113_143052.csv

Test mode and Demo mode runs do NOT use the real names, so a practice run can never replace the file
the Print Station is reading: they write carton_jwn_labels_TEST.csv / pallet_jwn_labels_TEST.csv, and
Demo adds a DEMO_ prefix. They are archived the same way.

Nothing is ever deleted: the old file is moved, not removed.
"""

from __future__ import annotations

import datetime
import os
from pathlib import Path

from src.db.local_store import LABEL_TYPE_CARTON, LABEL_TYPE_PALLET, write_flat_csv

CARTON_FILE_NAME = "carton_jwn_labels.csv"
PALLET_FILE_NAME = "pallet_jwn_labels.csv"
ARCHIVE_FOLDER_NAME = "archive"
ARCHIVE_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"  # e.g. 20261113_143052


class ArchiveError(OSError):
    """The file already in the output folder could not be moved into the archive folder (most often
    because BarTender Print Station or Excel has it open). The old file is left exactly as it was."""


def label_file_name(label_type: str, test_mode: bool = False, demo_mode: bool = False) -> str:
    """The fixed file name for this kind of label. Real runs get the exact generic name."""
    if label_type == LABEL_TYPE_CARTON:
        base = CARTON_FILE_NAME
    elif label_type == LABEL_TYPE_PALLET:
        base = PALLET_FILE_NAME
    else:
        raise ValueError(f"Unknown label type: {label_type!r}")
    stem, suffix = base[: -len(".csv")], ".csv"
    if test_mode:
        stem += "_TEST"
    if demo_mode:
        stem = "DEMO_" + stem
    return stem + suffix


def label_file_path(output_dir: Path | str, label_type: str, test_mode: bool = False, demo_mode: bool = False) -> Path:
    return Path(output_dir) / label_file_name(label_type, test_mode, demo_mode)


def archived_name(file_name: str, when: datetime.datetime) -> str:
    """carton_jwn_labels.csv -> carton_jwn_labels_20261113_143052.csv"""
    path = Path(file_name)
    return f"{path.stem}_{when.strftime(ARCHIVE_TIMESTAMP_FORMAT)}{path.suffix}"


def ensure_archive_folder(output_dir: Path | str) -> Path:
    """Creates <output_dir>\\archive if it is missing; if it already exists nothing happens (it is
    never an error and nothing in it is touched). Raises ArchiveError if it cannot be made."""
    archive_dir = Path(output_dir) / ARCHIVE_FOLDER_NAME
    try:
        archive_dir.mkdir(exist_ok=True)
    except OSError as exc:
        raise ArchiveError(f"The archive folder {archive_dir} could not be created ({exc}).") from exc
    return archive_dir


def archive_existing(target: Path | str, now: datetime.datetime | None = None) -> Path | None:
    """Moves `target` (if it exists) into <its folder>\\archive under a name with the date and time
    appended, creating the archive folder only if it is missing. Returns the archived file's path,
    or None if there was nothing to archive. Raises ArchiveError (leaving `target` untouched) if
    it cannot be moved. A rename on the same drive, never a copy-then-delete, so a file that is open
    elsewhere is never half-moved."""
    target = Path(target)
    if not target.exists():
        return None
    when = now or datetime.datetime.now()
    archive_dir = target.parent / ARCHIVE_FOLDER_NAME
    try:
        archive_dir.mkdir(exist_ok=True)  # already there is fine - nothing is changed
        destination = archive_dir / archived_name(target.name, when)
        counter = 1
        while destination.exists():  # two files archived in the same second: never overwrite
            counter += 1
            destination = archive_dir / f"{Path(archived_name(target.name, when)).stem}_{counter}{target.suffix}"
        os.rename(target, destination)  # fails (does not overwrite) if the target is open elsewhere
    except OSError as exc:
        raise ArchiveError(
            f"{target.name} could not be moved into the archive folder ({exc}). It is probably open in "
            "another program, such as BarTender Print Station or Excel."
        ) from exc
    return destination


def write_label_file(rows, target: Path | str, now: datetime.datetime | None = None) -> tuple[Path, Path | None]:
    """Archives the current `target` (if there is one) and then writes `rows` as the new `target`.
    Returns (the new file, the archived copy of the old one or None).

    The new rows are first written to a temporary file beside `target`, so that if writing fails
    (disk full, say) the old file is still in place; the old file is then archived; and only then is
    the new file put in place under the generic name. If the archive step fails the old file is left
    untouched and the new file is not written."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    pending = target.with_name(target.name + ".tmp")
    try:
        write_flat_csv(rows, pending)
        ensure_archive_folder(target.parent)  # always there after a run, even the very first one
        archived = archive_existing(target, now)
        try:
            os.replace(pending, target)
        except OSError:
            if archived is not None:  # put the old file back rather than leave no file at all
                try:
                    os.rename(archived, target)
                except OSError:
                    pass
            raise
    finally:
        try:
            pending.unlink()
        except FileNotFoundError:
            pass
        except OSError:
            pass
    return target, archived
