#!/usr/bin/env python3

"""
File organizer for macOS Downloads folder
This organizer separetes files for type/extensions in subfolders
"""

import argparse

from arguments import ArgumentParser
from organizer import DownloadsOrganizer


def main():
    arg_parser = ArgumentParser()
    args = arg_parser.parse_args()

    try:
        organizer = DownloadsOrganizer(downloads_path=args.path, dry_run=False)
        moved, errors = organizer.organize()
        print(organizer.generate_report())

        if args.dry_run and moved:
            response = input("\n Would you like to execute the real organization? (s/n):")
            if response.lower() == "s":
                organizer_real = DownloadsOrganizer(downloads_path=args.path, dry_run=False)
                organizer_real.organize()
                print(organizer_real.generate_report())

    except Exception as e:
        print(f"Erro: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
