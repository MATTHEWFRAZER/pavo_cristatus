from typing import Generator, List, IO, Any, Callable

import inspect
from inspect import FullArgSpec
import os
import re

from picidae import access_attribute

from pavo_cristatus.constants import DECORATOR_STRING
from pavo_cristatus.python_file import PythonFile

PYTHON_EXTENSION = ".py"
NONE_TYPE = "NoneType"

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

def collect_python_files_under_project_root(project_root_path, directories_to_ignore):
    for package_path, _, file_names in os.walk(project_root_path):
        if not any(package_path.startswith(directory_to_ignore) for directory_to_ignore in directories_to_ignore):
            for file_name in file_names:
                if file_name.endswith(PYTHON_EXTENSION):
                    yield PythonFile(file_name, package_path)

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

def pavo_cristatus_split(line):
    return line.split("\n")

def pavo_cristatus_get_source(symbol):
    if not hasattr(symbol, "pavo_cristatus_original_source"):
        return inspect.getsource(symbol)
    else:
        return symbol.pavo_cristatus_original_source

def pavo_cristatus_get_source_for_module(module):
    """
    this function is needed for the edge case that a module is empty, that will cause on OSError
    """
    try:
        return pavo_cristatus_get_source(module)
    except Exception:
        return ""

def pavo_cristatus_get_argument_annotation(arg_spec, argument):
    result = str()
    try:
        # if we get a type, we retrieve its name
        result = arg_spec.annotations[argument].__name__
    except AttributeError:
        try:
            # for other things like typing stuff, we put it directly into string form
            result = str(arg_spec.annotations[argument])
        except KeyError:
            pass
    except KeyError:
        pass


    if result == NONE_TYPE:
        return "None"
    else:
        # normalize qualname
        return pavo_cristatus_handle_nested_types(result)

def is_decorator_line(line):
        return line.strip().startswith(DECORATOR_STRING)

def remove_qualname(string):
    return string.split(".")[-1]


class PavoCristatusStackFrame(object):
    def __init__(self, middle, postfix):
        self.middle = middle
        self.postfix = postfix


def do_brackets_close_too_early(annotation, open_bracket_index):
    i = open_bracket_index + 1
    closed_bracket = 1

    annotation = annotation.strip()
    while i < len(annotation):
        if annotation[i] == "[":
            closed_bracket += 1
        if annotation[i] == "]":
            closed_bracket -= 1
        if closed_bracket == 0 and annotation[i] == "]":
            break
        i += 1
    return i < len(annotation) - 1


def bracket_split(annotation):
    split = []
    string = str()
    closed_bracket = 0
    for x in annotation:
        if x == "[":
            closed_bracket += 1
        if x == "]":
            closed_bracket -= 1

        if closed_bracket == 0 and x == ",":
            split.append(string.strip())
            string = str()
            continue

        string += x
    split.append(string.strip())
    return split


def pavo_cristatus_handle_nested_types(annotation):
    # typing inserts ~ to represent AnyStr, not sure why or where else this could pop up, but it is
    # invalid so we replace it and try to move on
    stack = [PavoCristatusStackFrame(annotation.replace("~", ""), "")]
    result_stack = []

    while stack:
        stack_frame = stack.pop()
        middle = stack_frame.middle
        postfix = stack_frame.postfix

        open_bracket_index = middle.find("[")
        close_bracket_index = middle.rfind("]")

        if open_bracket_index < 0 and close_bracket_index < 0:
            middle = re.sub(NONE_TYPE, "None", middle)
            result_stack.append(remove_qualname(middle) + postfix)
            continue

        new_prefix = remove_qualname(middle[: open_bracket_index])
        new_middle = middle[open_bracket_index + 1: close_bracket_index]

        result_stack.append(remove_qualname(new_prefix))
        result_stack.append("[")
        if do_brackets_close_too_early(middle, open_bracket_index) and "," in middle:
            result_stack.pop()
            result_stack.pop()
            i = 0
            for sibling in reversed(bracket_split(middle)):
                if i == 0:
                    stack.append(PavoCristatusStackFrame(sibling.strip(), postfix))
                else:
                    stack.append(PavoCristatusStackFrame(sibling.strip(), ", "))
                i += 1
        else:
            stack.append(PavoCristatusStackFrame(new_middle.strip(), "]" + postfix))

    return "".join(result_stack)
