import shutil

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
from rich import print as rprint

from extension_mapper import EXTENSION_TO_CATEGORY


@dataclass
class MoveRecord:
    source: Path
    destination: Path
    category: str


@dataclass
class ErrorRecord:
    file: Path
    error: str


class FolderOrganizer:
    def __init__(self, downloads_path: Optional[Path] = None, dry_run: bool = False) -> None:
        """
        Organizes files in a folder (Downloads as the standard) by extension.
        """

        self.downloads_path: Path = (downloads_path if downloads_path is not None else Path.home() / "Downloads")
        self.dry_run: bool = dry_run
        self.moved_files: List[MoveRecord] = []
        self.errors: List[ErrorRecord] = []

        if not self.downloads_path.exists():
            raise ValueError(f"Folder {self.downloads_path} does not exist!")

    @staticmethod
    def get_category(extension: str) -> str:
        """
        Return the category name for a given file extension
        """
        return EXTENSION_TO_CATEGORY.get(extension.lower(), "Others")

    def should_skip_file(self, file_path: Path) -> bool:
        """
        Decide whether a file should be skipped.

        We skip:
        - Hidden files
        - System metadata files
        - Directories (except .app/.pkg bundles, which are treated as 'apps')
        """

        is_app_bundle = file_path.suffix.lower() in {".app", ".pkg"}
        if is_app_bundle:
            return False  # macOS app bundles are directories with a .app suffix — we want to process them

        hidden_file = file_path.name.startswith(".")
        system_file = file_path.name in {".DS_Store", "desktop.ini", "Thumbs.db"}
        is_directory = file_path.is_dir()

        if hidden_file or system_file or is_directory:
            return True

        return False

    def create_category_folder(self, folder: str) -> Path:
        """
        Ensure the category folder exists and return its Path.
        """
        folder_path = self.downloads_path / folder
        if not self.dry_run:
            folder_path.mkdir(exist_ok=True)
        return folder_path

    def move_file(self, source: Path, destination: Path) -> Path:
        """
        Move the file to the given destination.
        If a file with the same name exists, append a timestamp.
        """

        if destination.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            new_name = f"{destination.stem}_{timestamp}{destination.suffix}"
            destination = destination.parent / new_name

        if not self.dry_run:
            # shutil.move wants strings on some platforms
            shutil.move(str(source), str(destination))

        return destination

    def organize(self) -> Tuple[List[MoveRecord], List[ErrorRecord]]:
        """
        Organize files in the downloads_path, returning lists of
        successful moves and errors.
        """

        mode = ("[yellow]SIMULATING[/yellow]" if self.dry_run else "[green]ORGANIZING[/green]")
        rprint(f"{mode} folder...")
        rprint(f"Folder: [bold]{self.downloads_path}[/bold]\n")

        for file_path in self.downloads_path.iterdir():
            try:
                if self.should_skip_file(file_path):
                    continue

                extension = file_path.suffix
                if not extension: category = "NoExtension"
                else: category = self.get_category(extension)

                folder = self.create_category_folder(category)
                destination = folder / file_path.name
                final_destination = self.move_file(file_path, destination)

                move_record = move_record = MoveRecord(source=file_path, destination=final_destination, category=category)
                self.moved_files.append(move_record)

                verb = "📄 Would move" if self.dry_run else "✅ Moved"
                rprint(f"{verb}: [cyan]{file_path.name}[/cyan] → 📁 [magenta]{category}[/magenta]/{final_destination.name}")

            except Exception as e:
                error_record = ErrorRecord(file=file_path, error=str(e))
                self.errors.append(error_record)

                rprint(f"❌ Error with [red]{file_path.name}[/red]: {e}")

        return self.moved_files, self.errors

    def generate_report(self):
        """
        Generate a string report of the organization.
        """
        report: List[str] = ["\n" + "=" * 50]
        report.append(f"📈 Total moved files: {len(self.moved_files)}")
        report.append(f"📈 Total errors found: {len(self.errors)}")
        return "\n".join(report)

    def undo_last_organization(self, log_file="organization_log.json"):
        """
        (Future feature) Undo last organization based on a log file.
        Maybe using self.move_files (?)
        """
        # TODO: Implement this later
        pass
