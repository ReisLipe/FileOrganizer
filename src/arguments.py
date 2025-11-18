import argparse
from pathlib import Path


DESCRIPTION = "macOS file organizer"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        help="Path to downloads folder (defaults to ~/Downloads)",
        default=None,
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Simulate organization without actually moving files",
    )

    return parser


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments and return a namespace."""
    return build_parser().parse_args()
