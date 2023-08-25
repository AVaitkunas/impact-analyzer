import ast
import os
from _ast import AST
from pathlib import Path
from typing import Optional, Iterator, List, Tuple
from collections import deque


def get_files(directory: Path, extension: str = ".py", exclude: Optional[List[str]] = None) -> Iterator[Path]:
    """Scans a directory and gets all files with extension specified"""
    if not directory.is_dir():
        raise Exception(f"incorrect path received, '{directory}' is not a directory.")

    for root, dirs, files in os.walk(directory):
        for file in files:
            abs_path = Path(root) / file
            if exclude and any(item in str(abs_path) for item in exclude):
                continue
            if file.endswith(extension):
                yield Path(root) / file


def function_definition_file_mapping(files: Iterator[Path]) -> Iterator[Tuple[Path, List[str]]]:
    """From given files get function definition to file mapping"""

    for file in files:
        tree = ast.parse(file.read_text("utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                print(node.name)
                yield file, node.name


def function_definition_nodes(module: AST) -> Iterator[AST]:
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef):
            yield node


def function_calls(node: AST) -> Iterator[AST]:
    for elem in ast.walk(node):
        if isinstance(elem, ast.Call) and isinstance(elem.func, ast.Name):
            yield elem.func.id


def function_dependency_data(files: Iterator[Path]):
    for file in files:
        tree = ast.parse(file.read_text("utf-8"))
        for def_node in function_definition_nodes(tree):
            # todo: return in a way that function name is also visible. best is from root. path.to.file.function: [calls...]
            # or have a namedtuple
            yield file.absolute(), def_node.name,  list(function_calls(def_node))

