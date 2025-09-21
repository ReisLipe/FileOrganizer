import argparse

class ArgumentParser:
    # MARK: - Path
    path_long = "--path"
    path_short = "-p"
    path_help = "Path to downloads folder"

    # MARK: - Dry Run
    dry_run_long = "--dry-run"
    dry_run_shor = "-d"
    dry_run_help = "Simulates organization without actually moving files"

    # MARK: - Description
    description = "MacOs file organizer"

    def __init__(self):
        self.parser = argparse.ArgumentParser(description = description)
        self.parser.add_argument(path_long, path_shor, help = path_help, default = None)
        self.parser.add_argument(dry_run_long, dry_run_short, action="store_true", help = dry_run_help)
    
    def parse_args(self):
        return self.parser.parse_args()