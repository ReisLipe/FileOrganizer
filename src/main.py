#!/usr/bin/env python3

"""
File organizer initially built for macOS Downloads folder
This organizer separetes files for type/extensions in subfolders
"""

from arguments import parse_args
from organizer import FolderOrganizer


def main():
    args = parse_args()

    organizer = FolderOrganizer(downloads_path=args.path, dry_run=args.dry_run)
    moved, errors = organizer.organize()
    print(organizer.generate_report())

    # If it was a dry run and we actually would move files, offer to run for real
    if args.dry_run and moved:
        response = input("\n Would you like to run for real? (y/n):")
        if response.lower() == "y":
            real_organizer = FolderOrganizer(downloads_path=args.path, dry_run=False)
            real_organizer.organize()
            print(real_organizer.generate_report())

if __name__ == "__main__":
    raise SystemExit(main())