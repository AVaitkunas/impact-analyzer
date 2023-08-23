import os
from pathlib import Path
from typing import Generator


def scan_directory(directory: Path) -> Generator:
    """Scans a directory and gets all python files"""
    if not directory.is_dir():
        raise Exception(f"incorrect path received, '{directory}' is not a directory.")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                yield Path(root) / file


if __name__ == '__main__':
    print(list(scan_directory(Path())))
