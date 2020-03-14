import inspect
import re
import itertools
import operator
import os

from picidae import access_attribute, expand_parameter_list_by_x
from trochilidae.interoperable_reduce import interoperable_reduce

from pavo_cristatus.constants import DEF_STRING
from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol
from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import convert_python_file_to_module_qualname, get_data_item_id

__all__ = ["CallableSymbol"]

def_pattern = re.compile(DEF_STRING)


class CallableSymbol(AbstractSymbol):

    def __init__(self, project_root_path, symbol, nested_symbols):
        super().__init__(symbol, nested_symbols)
        self.arg_spec = inspect.getfullargspec(symbol)
        self.project_root_path = project_root_path

    def get_non_annotated_source(self):
        return self.get_current_source(self.get_non_annotated_signature, access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, module_annotated_data_items, module_qualname=None):
        if module_qualname is None:
            package_path, file_name = os.path.split(inspect.getsourcefile(self.symbol))
            python_file = PythonFile(file_name, package_path)
            module_qualname = convert_python_file_to_module_qualname(self.project_root_path, python_file)
        return self.get_current_source(lambda line: self.get_annotated_signature(line, module_annotated_data_items, module_qualname),
                                       access_attribute(self.get_annotated_source.__name__),
                                       module_annotated_data_items,
                                       module_qualname)

    def get_annotated_signature(self, line, module_annotated_data_items, module_qualname):
        arg_spec =  module_annotated_data_items[get_data_item_id(module_qualname, self.qualname)]
        if arg_spec is None:
            return line
        return self.get_annotated_signature_inner(line, arg_spec)

    def get_current_source(self, get_current_signature, get_current_source_of_symbol, *args):
        tabs  = itertools.takewhile(lambda x: x in (" ", "\t"), self.source)
        tabs  = interoperable_reduce(operator.add, tabs, str())
        lines = self.source.split("\n")
        lines = self.replace_current_signature(lines, get_current_signature)
        lines = self.replace_nested_signatures(lines, tabs, get_current_source_of_symbol, *args)
        return "\n".join(lines)

    def handle_tabs_in_signature(self, line, signature):
        match = def_pattern.search(line)
        prefix_end_index = match.span()[0]
        prefix = line[:prefix_end_index]
        postfix_start_index = line.rfind(":") + 1
        postfix = line[postfix_start_index:]
        return prefix + signature + postfix

    def get_non_annotated_signature(self, line):
        return self.handle_tabs_in_signature(line, self.get_non_annotated_signature_inner())

    def get_annotated_signature_inner(self, line, arg_spec):
        signature = "{0} {1}(".format(DEF_STRING, self.name)

        signature += self.get_annotated_arguments(arg_spec)

        signature += self.get_annotated_variable_arguments(arg_spec)

        signature += self.get_annotated_variable_keyword_arguments(arg_spec)

        signature += self.get_annotated_keyword_only_arguments(arg_spec)

        try:
            return_annotation = " -> {0}".format(arg_spec.annotations["return"].__name__)
        except:
            return_annotation = str()

        signature += "){0}:".format(return_annotation)

        return self.handle_tabs_in_signature(line, signature)

    def get_annotated_arguments(self, arg_spec):
        reversed_arguments = reversed(list(arg_spec.args))
        length_of_default_tuple = 0 if arg_spec.defaults is None else len(arg_spec.defaults)
        arguments = str()
        for argument in reversed_arguments:
            argument_slot = ", " + argument
            try:
                argument_slot += " : {0}".format(arg_spec.annotations[argument].__name__)
            except:
                pass
            default_argument_slot = str()
            if length_of_default_tuple > 0:
                length_of_default_tuple -= 1

                try:
                    default_argument_annotation = arg_spec.annotations[argument].__name__
                    default_argument_slot = " : {0} = {1}".format(default_argument_annotation,
                                                                  arg_spec.defaults[length_of_default_tuple])
                except KeyError:
                    default_argument_slot = " = {0}".format(arg_spec.defaults[length_of_default_tuple])
            argument_slot += default_argument_slot
            arguments = argument_slot + arguments
        return arguments[2:]

    def replace_nested_signatures(self, lines, current_tabs, get_current_source_of_symbol, *args):
        for symbol in self.nested_symbols:
            line_number = symbol.find_line_number_of_symbol_in_source(self.source)
            current_source = current_tabs + "    " + get_current_source_of_symbol(symbol)(*args)
            for line in current_source.split("\n"):
                lines[line_number] = line
                line_number += 1
        return lines

    def get_non_annotated_signature_inner(self):
        signature = "{0} {1}(".format(DEF_STRING, self.name)

        reversed_arguments = reversed(list(self.arg_spec.args))
        length_of_default_tuple = 0 if self.arg_spec.defaults is None else len(self.arg_spec.defaults)
        arguments = str()
        for argument in reversed_arguments:
            argument_slot = ", " + argument
            if length_of_default_tuple > 0:
                length_of_default_tuple -= 1
                argument_slot += " = {0}".format(self.arg_spec.defaults[length_of_default_tuple])
            arguments = argument_slot + arguments
        signature += arguments[2:]

        if self.arg_spec.varargs is not None:
            signature += ", *" + self.arg_spec.varargs
        if self.arg_spec.varkw is not None:
            signature += ", **" + self.arg_spec.varkw

        for argument in self.arg_spec.kwonlyargs:
            signature += ", {0} = {1}".format(argument, self.arg_spec.kwonlydefaults[argument])

        signature += "):"

        return signature

    @staticmethod
    def replace_current_signature(lines, get_current_signature):
        i = 0
        while i < len(lines):
            line = lines[i]
            # we have to skip over decorators as they appear in source lines of callable
            if line.strip().startswith(DEF_STRING):
                lines[i] = get_current_signature(line)
                break
            else:
                i += 1
        return lines

    @staticmethod
    def get_annotated_variable_arguments(arg_spec):
        vararg_annotation = str()
        if arg_spec.varargs is not None:
            vararg_annotation += ", *" + arg_spec.varargs
            try:
                vararg_annotation += (" : " + arg_spec.annotations[arg_spec.varargs].__name__)
            except:
                vararg_annotation = str()
        return vararg_annotation

    @staticmethod
    def get_annotated_variable_keyword_arguments(arg_spec):
        keyword_annotation = str()
        if arg_spec.varkw is not None:
            keyword_annotation += ", **" + arg_spec.varkw
            try:
                keyword_annotation += " : " + arg_spec.annotations[arg_spec.varkw].__name__
            except:
                keyword_annotation = str()
        return keyword_annotation

    @staticmethod
    def get_annotated_keyword_only_arguments(arg_spec):
        keyword_only_annotations = str()
        for argument in arg_spec.kwonlyargs:
            try:
                keyword_only_annotations += " : " + arg_spec.annotations[argument].__name__
            except:
                keyword_only_annotations = str()
            keyword_only_annotations += ", {0}{1} = {2}".format(argument, keyword_only_annotations,
                                                                arg_spec.kwonlydefaults[argument])
        return keyword_only_annotations