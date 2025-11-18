# FileOrganizer
FileOrganizer is a small command-line tool that tidies up a macOS folder by
sorting files into subfolders based on their extension (documents, images,
videos, archives, etc.). 

I’m also using this project as a playground to learn **Docker** and **Python linting** with
[Ruff](https://github.com/astral-sh/ruff).

---

## Features
- Automatically organizes files in folder into category folders
- Categories are defined by file extension (easily configurable in `extension_mapper.py`)
- Supports a **dry-run** mode so you can see what would be moved before changing anything
- Skips hidden/system files and macOS metadata like `.DS_Store`

---

## Requirements

- macOS (default behavior assumes a `~/Downloads` folder)
- Python 3.9+ (tested with 3.9 and 3.11)

---
