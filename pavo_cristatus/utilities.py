import inspect
import os
import re

from trochilidae.interoperable_filter import interoperable_filter
from picidae import access_attribute

from pavo_cristatus.python_file import PythonFile

PYTHON_EXTENSION = ".py"

access_interaction_callable = access_attribute("interact")

def create_data_item_id(module_qualname, symbol_qualname):
    return "{0}.{1}".format(module_qualname, symbol_qualname)

def convert_python_file_to_module_qualname(project_root_path, python_file):
    split_file_name = os.path.splitext(python_file.file_name)

    if project_root_path == python_file.package_path:
        length = len(python_file.package_path)
        span = (length, length)
    else:
        try:
            # Windows path separator cases issues with re, so we temporarily get rid of it
            normalized_project_root_path = project_root_path.replace("\\", "/")
            normalized_package_path = python_file.package_path.replace("\\", "/")
            match = re.search(normalized_project_root_path, normalized_package_path)
        except re.error:
            return str()

        if match is None:
            return str()

        span = match.span()

    start_index = len(" ".join(os.path.split(project_root_path)[: -1])) + 1
    first = python_file.package_path[start_index: span[0]]
    second = python_file.package_path[span[1]:]
    new_package_path = (first + second).split(os.sep)
    package = ".".join(new_package_path)
    try:
        package = package if package[0] != "." else package[1:]
    except Exception:
        return str()
    else:
        return ".".join((package, split_file_name[0]))

def collect_python_files_under_project_root(project_root_path):
    for package_path, _, file_names in os.walk(project_root_path):
        for file_name in file_names:
            if file_name.endswith(PYTHON_EXTENSION):
                yield PythonFile(file_name, package_path)

def collect_nested_symbols_in_object_source(symbol):
    code_object = getattr(symbol, "__code__", tuple())
    nested_const = getattr(code_object, "co_consts", tuple())
    nested_code_objects = interoperable_filter(lambda x: code_object is not None and type(x) is type(code_object), nested_const)


    for nested_code_object in nested_code_objects:
        # first -> we need to solve how to get dependencies of the target (separate module) -> we then need to import those (load the module here?)
        # -> then we continue
        # 1. problem is what if we have a version conflict? (virtual env? Can we sandbox things where within the process, we have a separate env)
        # 2. what is an alternative
        try:
            source = inspect.getsource(nested_code_object).strip()
        except OSError:
            continue

        nested_symbol = resolve_nested_symbol(source, symbol, nested_code_object)
        if nested_symbol is None:
            continue

        yield nested_symbol

def resolve_nested_symbol(source, symbol, nested_code_object):
    try:
        compiled_source = compile(source, '<string>', 'exec')
    except Exception:
        return None

    namespace = {}
    try:
        # TODO: find out if I can eliminate this security risk. Right now it is what I have for retrieving nested symbols
        exec(compiled_source, namespace)
    except Exception:
        return None

    try:
        nested_symbol = namespace[nested_code_object.co_name]
    except KeyError:
        return None

    nested_symbol.__module__ = symbol.__module__
    nested_symbol.pavo_cristatus_nested_symbol_source = source

    return nested_symbol

def is_symbol_callable(symbol):
    return callable(symbol) or is_dereferenceable_function(symbol)

def is_dereferenceable_function(symbol):
    try:
        dereferenced_function = getattr(symbol, "__func__")
        return callable(dereferenced_function)
    except Exception:
        return False

def write_new_source(module_symbols, get_new_source, *args):
    new_source = get_new_source(module_symbols)(*args)
    with pavo_cristatus_open(module_symbols.path, "w") as project_file:
        project_file.write(new_source)
    return True

def pavo_cristatus_open(module_symbols_path, mode):
    return open(module_symbols_path, mode)
