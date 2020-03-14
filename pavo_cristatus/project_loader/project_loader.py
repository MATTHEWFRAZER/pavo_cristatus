import importlib

from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest, is_non_annotated_symbol_of_interest
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.utilities import collect_python_files_under_project_root, convert_python_file_to_module_qualname
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols

__all__ = ["load_annotated_project", "load_non_annotated_project"]

def load_modules_into_module_symbol_objects(project_root_path, python_files, is_symbol_of_interest):
    project_symbols = set()
    for python_file in python_files:
        module_qualname = convert_python_file_to_module_qualname(project_root_path, python_file)
        module = importlib.import_module(module_qualname)
        symbols = symbol_collector.collect(project_root_path, module, is_symbol_of_interest)
        module_symbols = ModuleSymbols(module, python_file, module_qualname, symbols)
        project_symbols.add(module_symbols)
    return project_symbols

def load_annotated_project(project_root_path):
    return load_modules_into_module_symbol_objects(project_root_path,
                                                   collect_python_files_under_project_root(project_root_path),
                                                   is_annotated_symbol_of_interest)

def load_non_annotated_project(project_root_path):
    return load_modules_into_module_symbol_objects(project_root_path,
                                                   collect_python_files_under_project_root(project_root_path),
                                                   is_non_annotated_symbol_of_interest)