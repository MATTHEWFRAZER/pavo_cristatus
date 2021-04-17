import re
import os

from picidae import access_attribute

from pavo_cristatus.constants import DEF_STRING
from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol
from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import convert_python_file_to_module_qualname, create_data_item_id, pavo_cristatus_split, \
    is_decorator_line

__all__ = ["CallableSymbol"]

def_pattern = re.compile(DEF_STRING)


class CallableSymbol(AbstractSymbol):
    """
    represents a callable as a symbol object
    """

    def __init__(self, project_root_path, normalized_symbol, nested_normalized_symbols):
        super().__init__(normalized_symbol, nested_normalized_symbols)
        self.arg_spec = normalized_symbol.arg_spec
        self.project_root_path = project_root_path

    def get_non_annotated_source(self):
        """
        gets the non annotated source of a symbol
        :return: the symbol's source as a string
        """
        return self.get_source(self.get_non_annotated_signature, access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, module_annotated_data_items, module_qualname=None):
        """
        gets the annotated source of a symbol
        :param module_annotated_data_items:
        :param module_qualname:
        :return: the symbol's source as a string
        """
        if module_qualname is None:
            package_path, file_name = os.path.split(self.normalized_symbol.file)
            python_file = PythonFile(file_name, package_path)
            module_qualname = convert_python_file_to_module_qualname(self.project_root_path, python_file)
        return self.get_source(lambda line: self.get_annotated_signature(line, module_annotated_data_items, module_qualname),
                               access_attribute(self.get_annotated_source.__name__),
                               module_annotated_data_items,
                               module_qualname)

    def get_annotated_signature(self, line, module_annotated_data_items, module_qualname):
        """
        gets the annotated source of a symbol
        :param line: used to get an annotated signature
        :param module_annotated_data_items: dictionary used to retrieve the desired arg_spec used to get an annotated signature
        :param module_qualname: used to create a data_item_id
        :return: the symbol's source as a string
        """
        arg_spec = module_annotated_data_items.get(create_data_item_id(module_qualname, self.qualname), None)
        if arg_spec is None:
            return line
        return self.get_annotated_signature_inner(line, arg_spec)

    def get_source(self, get_signature_strategy, get_source_strategy, *args):
        """
        gets the source of a callable symbol
        :param get_signature_strategy: the strategy (e.g. get_annotated_signature) for getting the symbol's signature
        :param get_source_strategy: the strategy (e.g. get_annotated_source) for getting the symbol's source
        :param args: contextual data required for replacing nested symbols' signatures
        :return: symbol source as a string
        """
        lines = pavo_cristatus_split(self.source)
        lines = self.replace_signature(lines, self.normalized_symbol.indent, get_signature_strategy)
        lines = self.replace_nested_signatures(lines, get_source_strategy, *args)
        return "\n".join(lines)

    def create_new_signature(self, line, signature):
        """
        construct new signature from existing signature line
        :param line: used to get an annotated signature
        :param signature: used to construct a new signature
        :return: signature as a string
        """
        # find "def" string in line
        match = def_pattern.search(line)
        # get the end index of the "def" string
        prefix_end_index = match.start()
        # get "def" string from line
        prefix = line[:prefix_end_index]
        # find the start of any type hints pattern after the symbol signature
        postfix_start_index = line.rfind(":") + 1
        # get postfix string from line
        postfix = line[postfix_start_index:]
        # new signature
        return prefix + signature + postfix

    def get_non_annotated_signature(self, line):
        """
        :param line: used to get a non annotated signature
        :return: signature as a string
        """
        return self.create_new_signature(line, self.get_non_annotated_signature_inner())

    def get_annotated_signature_inner(self, line, arg_spec):
        """
        gets the annotated source of a symbol
        :param line: used to get an annotated signature
        :param arg_spec: used to create an annotated signature
        :return: signature as a string
        """

        signature = "{0} {1}(".format(DEF_STRING, self.name)

        signature += self.get_annotated_arguments(arg_spec)

        signature += self.get_annotated_variable_arguments(arg_spec)

        signature += self.get_annotated_keyword_arguments(arg_spec)

        signature += self.get_annotated_keyword_only_arguments(arg_spec)

        try:
            return_annotation = " -> {0}".format(arg_spec.annotations["return"].__name__)
        except Exception:
            return_annotation = str()

        signature += "){0}:".format(return_annotation)

        return self.create_new_signature(line, signature)

    def get_annotated_arguments(self, arg_spec):
        """
        gets the annotated arguments for a signature
        :param arg_spec: used to construct the annotated arguments string
        :return: annotated arguments string
        """
        # reverse the argument list because we construct the annotated arguments string from right to left
        # we construct the string right to left because it is the only way we can associate defaults in the right order
        reversed_arguments = reversed(list(arg_spec.args))

        length_of_default_tuple = 0 if arg_spec.defaults is None else len(arg_spec.defaults)

        # we are doing this arguments = argument_slot + arguments, thus at the start we don't have anything to add
        arguments = str()
        for argument in reversed_arguments:
            argument_slot = ", " + argument
            try:
                # retrieve type from annotations dictionary and the type's name
                argument_slot += " : {0}".format(arg_spec.annotations[argument].__name__)
            except Exception:
                pass
            default_argument_slot = str()
            if length_of_default_tuple > 0:
                length_of_default_tuple -= 1
                default_argument_slot = " = {0}".format(arg_spec.defaults[length_of_default_tuple])
            argument_slot += default_argument_slot
            arguments = argument_slot + arguments
        # in case we don't have arguments
        if not arguments:
            return str()
        return arguments[2:]

    def replace_nested_signatures(self, lines, get_source_strategy, *args):
        """
        replace each nested signature with new source
        :param lines: lines of the module that contains the symbol
        :param get_source_strategy: the strategy (e.g. get_annotated_source) for getting the symbol's source
        :param args: contextual data for get_source_strategy
        :return: modified lines
        """
        for normalized_symbol in self.nested_symbols:
            line_number = normalized_symbol.find_line_number_of_symbol_in_source(self.source)

            if line_number < 0:
                raise ValueError("source does not contain a line number for {0}".format(normalized_symbol.name))

            source = get_source_strategy(normalized_symbol)(*args)
            for line in pavo_cristatus_split(source):
                lines[line_number] = line
                line_number += 1
        return lines

    def get_non_annotated_signature_inner(self):
        """
        :return: non annotated signature as a string
        """
        signature = "{0} {1}(".format(DEF_STRING, self.name)

        # reverse the argument list because we construct the annotated arguments string from right to left
        # we construct the string right to left because it is the only way we can associate defaults in the right order
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
    def replace_signature(lines, indent, get_signature_strategy):
        """
        replace signatures of each "def"
        :param lines: lines of the module that contains the symbol
        :param get_signature_strategy: the strategy (e.g. get_annotated_signature) for getting the symbol's signature
        :return: modified lines
        """
        # i = 0
        # while i < len(lines):
        #     line = lines[i]
        #     # we have to skip over decorators as they appear in source lines of callable
        #     if line.strip().startswith(DEF_STRING):
        #         lines[i] = indent + get_signature_strategy(line)
        #         break
        #     else:
        #         i += 1
        # return lines
        i = 0
        # TODO: HACK ALERT, figure out why the indent differs for decorated lines
        encountered_decorated_line = False
        while i < len(lines):
            line = lines[i]
            if is_decorator_line(line):
                encountered_decorated_line = True
            # we have to skip over decorators as they appear in source lines of callable
            if not encountered_decorated_line and line.strip().startswith(DEF_STRING):
                lines[i] = indent + get_signature_strategy(line)
                break
            elif encountered_decorated_line and line.strip().startswith(DEF_STRING):
                lines[i] = get_signature_strategy(line)
                break
            else:
                i += 1
        return lines

    @staticmethod
    def get_annotated_variable_arguments(arg_spec):
        """
        gets annotated variable arguments string
        :param arg_spec: used to construct annotated variable arguments string
        :return: vararg annotated string
        """
        vararg_annotation = str()
        if arg_spec.varargs is not None:
            vararg_annotation += ", *" + arg_spec.varargs
            try:
                vararg_annotation += (" : " + arg_spec.annotations[arg_spec.varargs].__name__)
            except Exception:
                vararg_annotation = str()
        return vararg_annotation

    @staticmethod
    def get_annotated_keyword_arguments(arg_spec):
        """
        gets annotated keyword arguments string
        :param arg_spec: used to construct annotated keyword arguments string
        :return: keyword annotated string
        """
        keyword_annotation = str()
        if arg_spec.varkw is not None:
            keyword_annotation += ", **" + arg_spec.varkw
            try:
                keyword_annotation += " : " + arg_spec.annotations[arg_spec.varkw].__name__
            except Exception:
                keyword_annotation = str()
        return keyword_annotation

    @staticmethod
    def get_annotated_keyword_only_arguments(arg_spec):
        """
        gets annotated keyword only arguments string
        :param arg_spec: used to construct annotated keyword only arguments string
        :return: keyword only annotated string
        """
        keyword_only_annotations = str()
        for argument in arg_spec.kwonlyargs:
            try:
                keyword_only_annotations += " : " + arg_spec.annotations[argument].__name__
            except Exception:
                keyword_only_annotations = str()
            keyword_only_annotations += ", {0}{1} = {2}".format(argument, keyword_only_annotations,
                                                                arg_spec.kwonlydefaults[argument])
        return keyword_only_annotations