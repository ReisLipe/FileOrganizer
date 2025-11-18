# FileOrganizer
FileOrganizer is a small command-line tool that tidies up a macOS folder by
sorting files into subfolders based on their extension (documents, images,
videos, archives, etc.). 

I’m also using this project as a playground to learn **Docker** and **Python linting** with
[Ruff](https://github.com/astral-sh/ruff). The Docker image can be found on
[Docker Hub](https://hub.docker.com/repository/docker/lipereis/file_organizer/general)

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

## Run with Docker
- Install Docker
- Pull the image from Docker Hub with: `docker pull lipereis/file_organizer:v1`
- To execute the container, run: `docker run --rm -v $HOME/<path>:/data <image_name>:<tag>`

