import collections
import inspect
import os
import sys

from pavo_cristatus.project_loader.nested_symbol_collector import collect_nested_symbols
from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import convert_python_file_to_module_qualname, create_data_item_id, is_symbol_callable


def get_module_qualname(symbol, project_root_path):
    package_path, file_name = os.path.split(inspect.getsourcefile(symbol))
    return convert_python_file_to_module_qualname(project_root_path, PythonFile(file_name, package_path))


def get_python_file_from_symbol_object(symbol):
    module = sys.modules[symbol.module]
    split_path = os.path.split(module.__file__)
    return PythonFile(split_path[1], split_path[0])


def get_nested_argspecs(symbol):
    arg_specs = {}
    queue = collections.deque()
    queue.appendleft(symbol)
    while queue:
        current = queue.pop()
        if is_symbol_callable(current):
            arg_specs[current.__qualname__] = inspect.getfullargspec(current)
        for nested_symbol in collect_nested_symbols(current):
            queue.appendleft(nested_symbol)
    return arg_specs