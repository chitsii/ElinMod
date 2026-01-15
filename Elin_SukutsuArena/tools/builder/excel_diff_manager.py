"""
excel_diff_manager.py - Build-time Excel Diff Management

Manages Excel file backups and shows content-level differences after builds.

Usage:
    # Before build: backup current Excel files (only if no backup exists)
    python excel_diff_manager.py backup

    # Force overwrite existing backup
    python excel_diff_manager.py backup --force

    # After build: show differences from backup
    python excel_diff_manager.py diff

    # Clean up backup directory (allows next backup to be created)
    python excel_diff_manager.py clean

The backup is stored in tools/.excel_backup/ and preserved across builds
until explicitly cleaned or force-overwritten.
"""

import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from diff_excel import compare_excel_files, compare_directories

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
TOOLS_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = TOOLS_DIR.parent
BACKUP_DIR = TOOLS_DIR / ".excel_backup"

# Excel directories to track
EXCEL_DIRS = [
    PROJECT_ROOT / "LangMod" / "JP" / "Dialog" / "Drama",
    PROJECT_ROOT / "LangMod" / "JP",
    PROJECT_ROOT / "LangMod" / "EN",
]


def get_all_excel_files() -> list[Path]:
    """Get all Excel files to track."""
    files = []
    for dir_path in EXCEL_DIRS:
        if dir_path.exists():
            # Get xlsx files directly in the directory (not recursive for LangMod/JP)
            if "Dialog" in str(dir_path):
                files.extend(dir_path.glob("*.xlsx"))
            else:
                # For LangMod/JP and LangMod/EN, only get Source*.xlsx
                files.extend(dir_path.glob("Source*.xlsx"))
    return sorted(files)


def backup_excel_files(force: bool = False) -> int:
    """Backup all Excel files before build.

    Args:
        force: If True, overwrite existing backup. If False, skip if backup exists.
    """
    # Check if backup already exists
    if BACKUP_DIR.exists() and not force:
        backup_files = list(BACKUP_DIR.rglob("*.xlsx"))
        if backup_files:
            print(f"[Excel Diff] Backup exists ({len(backup_files)} files). Use --force to overwrite.")
            return len(backup_files)

    # Clean and recreate backup directory
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    BACKUP_DIR.mkdir(parents=True)

    files = get_all_excel_files()
    if not files:
        print("[Excel Diff] No Excel files found to backup")
        return 0

    backed_up = 0
    for file_path in files:
        # Create relative path structure in backup
        rel_path = file_path.relative_to(PROJECT_ROOT)
        backup_path = BACKUP_DIR / rel_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, backup_path)
        backed_up += 1

    print(f"[Excel Diff] Backed up {backed_up} files")
    return backed_up


def show_diff() -> int:
    """Show differences between backup and current files."""
    if not BACKUP_DIR.exists():
        print("[Excel Diff] No backup found. Run 'backup' first.")
        return 2

    # Get backup files
    backup_files = list(BACKUP_DIR.rglob("*.xlsx"))
    if not backup_files:
        print("[Excel Diff] Backup is empty")
        return 2

    total_files = 0
    changed_files = 0
    new_files = 0

    # Compare each backed up file with current
    for backup_path in sorted(backup_files):
        rel_path = backup_path.relative_to(BACKUP_DIR)
        current_path = PROJECT_ROOT / rel_path

        total_files += 1

        if not current_path.exists():
            print(f"[DELETED] {rel_path}")
            changed_files += 1
            continue

        identical, diffs = compare_excel_files(backup_path, current_path)

        if not identical:
            changed_files += 1
            print(f"[CHANGED] {rel_path}")
            # Show first few differences
            for diff in diffs[:5]:
                print(f"  {diff}")
            if len(diffs) > 5:
                print(f"  ... and {len(diffs) - 5} more changes")

    # Check for new files
    current_files = get_all_excel_files()
    for current_path in current_files:
        rel_path = current_path.relative_to(PROJECT_ROOT)
        backup_path = BACKUP_DIR / rel_path
        if not backup_path.exists():
            new_files += 1
            print(f"[NEW] {rel_path}")

    # Summary
    print()
    if changed_files == 0 and new_files == 0:
        print(f"[Excel Diff] All {total_files} files unchanged")
        return 0
    else:
        print(f"[Excel Diff] {changed_files} changed, {new_files} new (of {total_files} tracked)")
        return 1


def clean_backup() -> None:
    """Remove backup directory."""
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
        print("[Excel Diff] Backup cleaned")
    else:
        print("[Excel Diff] No backup to clean")


def main():
    parser = argparse.ArgumentParser(
        description="Manage Excel file backups and show build differences"
    )
    parser.add_argument(
        "command",
        choices=["backup", "diff", "clean"],
        help="backup: save current files, diff: show changes, clean: remove backup"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Force overwrite existing backup"
    )

    args = parser.parse_args()

    if args.command == "backup":
        backup_excel_files(force=args.force)
        sys.exit(0)
    elif args.command == "diff":
        result = show_diff()
        sys.exit(result)
    elif args.command == "clean":
        clean_backup()
        sys.exit(0)


if __name__ == "__main__":
    main()
