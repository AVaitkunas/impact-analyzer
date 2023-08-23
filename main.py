import os
import re
from pathlib import Path
from typing import Iterator, Optional


def scan_directory(directory: Path, exclude: Optional[str] = None) -> Iterator[Path]:
    """Scans a directory and gets all python files"""
    if not directory.is_dir():
        raise Exception(f"incorrect path received, '{directory}' is not a directory.")

    for root, dirs, files in os.walk(directory):
        for file in files:
            abs_path = Path(root) / file
            if exclude and exclude in str(abs_path):
                continue
            if file.endswith(".py"):
                yield Path(root) / file


def search_func_definition(function_name: str, files: Iterator[Path]) -> Optional[Path]:
    """Search within given files for function definition place"""
    for file in files:
        if not file.is_file() or not file.name.endswith(".py"):
            continue

        file_content = file.read_text(encoding='utf-8')
        pattern = f"def {function_name}\("

        func_definitions = re.findall(pattern, file_content)

        if not func_definitions:
            continue

        if len(func_definitions) > 1:
            raise Exception("more then one funtion definition is found")
        return file


if __name__ == '__main__':
    print(search_func_definition(function_name="scan_directory", files=scan_directory(Path(), exclude="venv")))
