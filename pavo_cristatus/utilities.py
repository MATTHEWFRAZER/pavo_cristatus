import inspect
import os
import re
import itertools

from trochilidae.interoperable_filter import interoperable_filter
from picidae import access_attribute

from pavo_cristatus.pavo_cristatus_namespace import PavoCristatusNamespace
from pavo_cristatus.python_file import PythonFile

PYTHON_EXTENSION = ".py"

access_interaction_callable = access_attribute("interact")

def pavo_cristatus_strip_source(source):
    new_source = ""
    lines = source.split("\n")
    found_end_to_decorators = False
    for line in lines:
        if is_decorated_line(line):
            found_end_to_decorators = True
        if found_end_to_decorators:
            new_source += line + "\n"

    return new_source.strip()

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
            source = pavo_cristatus_get_source(nested_code_object).strip()
        except OSError:
            continue

        nested_symbol = normalize_nested_symbol(source, symbol, nested_code_object.co_name)
        if nested_symbol is None:
            continue

        nested_symbol.pavo_cristatus_original_source = source

        yield nested_symbol

def pavo_cristatus_getsourcefile(symbol):
    if not hasattr(symbol, "pavo_cristatus_original_source_file"):
        return inspect.getsource(symbol)
    else:
        return symbol.pavo_cristatus_original_source_file

def normalize_nested_symbol(source, symbol, symbol_name):
    nested_symbol = normalize_symbol(symbol, source, source, symbol_name)
    if nested_symbol is not None:
        nested_symbol.pavo_cristatus_original_source = source
        return nested_symbol
    else:
        return None

def normalize_symbol(original_symbol, stripped_source, source, symbol_name):
    namespace = PavoCristatusNamespace(resolve_symbol_in_namespace, stripped_source)
    normalized_symbol = normalize_symbol_from_source(stripped_source, namespace, lambda x: x[symbol_name])#get_first(x, symbol_name))
    if normalized_symbol is not None:
        normalized_symbol.pavo_cristatus_original_source = source
        normalized_symbol.__module__ = original_symbol.__module__
    return normalized_symbol

def get_first(namespace, symbol_name):
    dropped = itertools.dropwhile(lambda x: get_symbol_name(x) != symbol_name, namespace.values())
    return next(dropped, None)

def get_symbol_name(symbol):
    try:
        return symbol.__name__
    except Exception:
        return str()

def resolve_symbol_in_namespace(namespace, symbol_name, symbol, source):
    # needs to be update otherwise we end up calling __setitem__ which is what this function hooks
    namespace.update({symbol_name: resolve_correct_symbol(symbol_name, symbol, source)})
    return not hasattr(namespace[symbol_name], "pavo_cristatus_original_source")

def resolve_correct_symbol(symbol_name, symbol, source=None):
    try:
        if symbol_name == symbol.__name__:
            return symbol
        elif symbol.__name__ == "<lambda>":
            if source is None:
                source = pavo_cristatus_get_source(symbol)
            return resolve_decorated_symbol(symbol_name, source)
        else:
            return None
    except AttributeError:
        return None

def resolve_decorated_symbol(name_to_resolve, source):
    """
    in the case the symbol was generated through lambda decoration, we need to get retrieve the decorated symbol
    :name_to_resolve: the name we want the symbol to be bound to
    :symbol: the lambda decorator
    :return: lambda decorated function
    """
    lines = source.split('\n')
    modified_source = ""
    skipped_decorators = False
    for line in lines:
        if is_decorated_line(line):
            skipped_decorators = True
        if skipped_decorators:
            modified_source += line
    namespace = PavoCristatusNamespace(lambda a, b, c, d: True)
    resolved_symbol = normalize_symbol_from_source(modified_source.strip(), namespace, lambda x: x[name_to_resolve])
    resolved_symbol.pavo_cristatus_original_source = source
    return resolved_symbol

def is_decorated_symbol(source):
    lines = source.split("\n")
    for line in lines:
        if line.strip().startswith("@"):
            return True
        if is_decorated_line(line):
            return False
    else:
        return False

def is_decorated_line(line):
    return line.strip().startswith("def") or line.strip().startswith("class")

def normalize_symbol_from_source(source, namespace, access):
    try:
        compiled_source = compile(source, '<string>', 'exec')
    except Exception:
        return None

    try:
        # TODO: find out if I can eliminate this security risk. Right now it is what I have for retrieving nested symbols
        exec(compiled_source, namespace)
    except Exception:
        return None

    try:
        nested_symbol = access(namespace)
    except KeyError:
        return None

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

def pavo_cristatus_get_source(symbol):
    if not hasattr(symbol, "pavo_cristatus_original_source"):
        return inspect.getsource(symbol)
    else:
        return symbol.pavo_cristatus_original_source
