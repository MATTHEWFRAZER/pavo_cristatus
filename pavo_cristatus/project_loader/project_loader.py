import importlib

from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest, is_non_annotated_symbol_of_interest
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.utilities import collect_python_files_under_project_root, convert_python_file_to_module_qualname
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols

__all__ = ["load_annotated_project", "load_non_annotated_project"]

def load_modules_into_module_symbol_objects(project_root_path, python_files, is_symbol_of_interest):
    """
    given a number of PythonFile objects we use them to construct a set of ModuleSymbols objects
    :param project_root_path: symbols we will use to write out new source code
    :param python_files: PythonFile objects that we use to get a ModuleSymbols object
    :param is_symbol_of_interest: predicate that determines if a symbol is of interest
    :return: set of ModuleSymbols objects
    """

    project_symbols = set()
    for python_file in python_files:
        module_qualname = convert_python_file_to_module_qualname(project_root_path, python_file)
        # TODO: figure out how to avoid filtering __init__ files
        if module_qualname.endswith("__init__"):
            continue
        try:
            module = importlib.import_module(module_qualname)
        except (ValueError, ModuleNotFoundError):
            continue
            #raise ValueError("given module_qualname could not be imported: {0}".format(module_qualname))
        symbols = symbol_collector.collect(project_root_path, module, is_symbol_of_interest)
        module_symbols = ModuleSymbols(module, python_file, module_qualname, symbols)
        project_symbols.add(module_symbols)
    return project_symbols

def load_annotated_project(project_root_path):
    """
    loads annotated symbols into a set of ModuleSymbols
    :param project_root_path: symbols we will use to write out new source code
    :return: set of ModuleSymbols objects
    """
    return load_modules_into_module_symbol_objects(project_root_path,
                                                   collect_python_files_under_project_root(project_root_path),
                                                   is_annotated_symbol_of_interest)

def load_non_annotated_project(project_root_path):
    """
    loads non annotated symbols into a set of ModuleSymbols
    :param project_root_path: symbols we will use to write out new source code
    :return: set of ModuleSymbols objects
    """
    return load_modules_into_module_symbol_objects(project_root_path,
                                                   collect_python_files_under_project_root(project_root_path),
                                                   is_non_annotated_symbol_of_interest)