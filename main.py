from pathlib import Path

from utils.search import get_files, function_dependency_data

if __name__ == '__main__':
    files = get_files(directory=Path(), exclude=["venv", "tests", ".pytest_cache", ".idea"])
    # print(list(function_definition_file_mapping(files)))
    print(list(function_dependency_data(files)))
