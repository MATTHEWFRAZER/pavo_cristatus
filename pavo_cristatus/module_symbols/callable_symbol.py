import re
import os
from inspect import FullArgSpec
from typing import List, Callable, Any

from picidae import access_attribute

from pavo_cristatus.constants import DEF_STRING
from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol
from pavo_cristatus.python_file import PythonFile
from pavo_cristatus.utilities import convert_python_file_to_module_qualname, create_data_item_id, pavo_cristatus_split, \
    is_decorator_line, pavo_cristatus_get_argument_annotation

__all__ = ["CallableSymbol"]

def_pattern = re.compile(DEF_STRING)


class CallableSymbol(AbstractSymbol):
    """
    represents a callable as a symbol object
    """

    def __init__(self, module_path, normalized_symbol, nested_normalized_symbols):
        super().__init__(normalized_symbol, nested_normalized_symbols)
        self.arg_spec = normalized_symbol.arg_spec
        self.module_path = module_path

    def get_non_annotated_source(self):
        """
        gets the non annotated source of a symbol
        :return: the symbol's source as a string
        """
        return self.get_source(self.get_non_annotated_signature, access_attribute(self.get_non_annotated_source.__name__))

    def get_annotated_source(self, module_annotated_data_items, module_qualname = None):
        """
        gets the annotated source of a symbol
        :param module_annotated_data_items:
        :param module_qualname:
        :return: the symbol's source as a string
        """
        if module_qualname is None:
            package_path, file_name = os.path.split(self.normalized_symbol.file)
            python_file = PythonFile(file_name, package_path)
            module_qualname = convert_python_file_to_module_qualname(self.module_path, python_file)
        return self.get_source(lambda lines, signature_start_index: self.get_annotated_signature(lines, signature_start_index, module_annotated_data_items, module_qualname),
                               access_attribute(self.get_annotated_source.__name__),
                               module_annotated_data_items,
                               module_qualname)

    def get_annotated_signature(self, lines, signature_start_index, module_annotated_data_items, module_qualname):
        """
        gets the annotated source of a symbol
        :param lines: used to get an annotated signature
        :param signature_start_index: used to get correct signature
        :param module_annotated_data_items: dictionary used to retrieve the desired arg_spec used to get an annotated signature
        :param module_qualname: used to create a data_item_id
        :return: the symbol's source as a string
        """
        arg_spec = module_annotated_data_items.get(create_data_item_id(module_qualname, self.qualname), None)
        if arg_spec is None:
            return lines[signature_start_index]
        return self.get_annotated_signature_inner(lines, arg_spec)

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

    @staticmethod
    def create_new_signature(lines : List[str], signature_start_index : int, signature : str) -> str:
        """
        construct new signature from existing signature line
        :param lines: used to get an annotated signature
        :param signature_start_index: start of signature
        :param signature: used to construct a new signature
        :return: signature as a string
        """
        # find "def" string in line
        match = def_pattern.search(lines[signature_start_index])
        # get the end index of the "def" string
        prefix_end_index = match.start()
        # get "def" string from line
        prefix = lines[signature_start_index][:prefix_end_index]

        # find the line to get the postfix from
        open_parenthesis = 0
        i = signature_start_index
        postfix_line = lines[signature_start_index]

        while i < len(lines):
            line = lines[i]
            # handle comments
            no_comment_line = line.split("#")[0]
            open_parenthesis += no_comment_line.count("(")
            open_parenthesis -= no_comment_line.count(")")
            if open_parenthesis == 0:
                postfix_line = line
                break
            i += 1

        # find the start of any type hints pattern after the symbol signature
        comment = "#".join(postfix_line.split("#")[1:])
        postfix_line = postfix_line.split("#")[0]

        lambda_string = "lambda :".join(re.split("lambda\s*:", postfix_line)[1:])
        postfix_line = re.split("lambda\s*:", postfix_line)[0]

        if lambda_string:
            lambda_string = "lambda :" + lambda_string

        postfix_start_index = postfix_line.rfind(":") + 1
        # get postfix string from line
        postfix = postfix_line[postfix_start_index:] + lambda_string + comment

        # new signature
        return prefix + signature + postfix

    def get_non_annotated_signature(self, lines, signature_start_index):
        """
        :param lines: used to get a non annotated signature
        :param signature_start_index: start of signature
        :return: signature as a string
        """
        signature = self.get_non_annotated_signature_inner()
        return self.create_new_signature(lines, signature_start_index, signature)

    def get_annotated_signature_inner(self, lines, arg_spec):
        """
        gets the annotated source of a symbol
        :param lines: used to get an annotated signature
        :param arg_spec: used to create an annotated signature
        :return: signature as a string
        """
        signature = "{0} {1}(".format(DEF_STRING, self.name)

        signature_inner = self.get_annotated_arguments(arg_spec)

        signature_inner += self.get_annotated_variable_arguments(arg_spec)

        signature_inner += self.get_annotated_keyword_arguments(arg_spec)

        signature_inner += self.get_annotated_keyword_only_arguments(arg_spec)

        if signature_inner.startswith(","):
            signature_inner = signature_inner[1:]

        signature += signature_inner
        return_annotation = pavo_cristatus_get_argument_annotation(arg_spec, "return")
        if return_annotation:
            return_annotation = " -> {0}".format(return_annotation)

        signature += "){0}:".format(return_annotation)

        # find start of signature
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith(DEF_STRING):
                break
            i += 1

        return self.create_new_signature(lines, i, signature)

    @staticmethod
    def get_annotated_arguments(arg_spec : FullArgSpec) -> str:
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

            annotation = pavo_cristatus_get_argument_annotation(arg_spec, argument)
            if annotation:
                argument_slot += " : {0}".format(annotation)
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
            signature += (", *" if arguments else "*") + self.arg_spec.varargs
        if self.arg_spec.varkw is not None:
            signature += (", **" if (arguments or self.arg_spec.varargs is not None) else "**") + self.arg_spec.varkw

        for i, argument in enumerate(self.arg_spec.kwonlyargs):
            if i == 0 and (arguments or self.arg_spec.varargs is not None or self.arg_spec.varkw is not None):
                signature += ", *"
            elif i == 0:
                signature += "*"
            if self.arg_spec.kwonlydefaults is not None:
                signature += ", {0} = {1}".format(argument, self.arg_spec.kwonlydefaults[argument])
            else:
                signature += ", {0}".format(argument)


        signature += "):"

        return signature

    @staticmethod
    def replace_signature(lines : List[str], indent : str, get_signature_strategy : Callable) -> List[str]:
        """
        replace signatures of each "def"
        :param lines: lines of the module that contains the symbol
        :param indent: indent used to construct signature
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
        open_parenthesis = 0
        encountered_decorated_line = False
        is_multiline = False
        while i < len(lines):
            line = lines[i]
            no_comment_line = line.split("#")[0]
            open_parenthesis += no_comment_line.count("(")
            open_parenthesis -= no_comment_line.count(")")
            if is_decorator_line(line):
                encountered_decorated_line = True
            is_multiline = open_parenthesis != 0
            # we have to skip over decorators as they appear in source lines of callable
            if not encountered_decorated_line and line.strip().startswith(DEF_STRING):
                lines[i] = indent + get_signature_strategy(lines, i)
                break
            elif encountered_decorated_line and line.strip().startswith(DEF_STRING):
                lines[i] = get_signature_strategy(lines, i)
                break
            else:
                i += 1
            is_multiline = False

        if is_multiline:
            signature_line = i
            i += 1
            while i < len(lines):
                line = lines[i]
                no_comment_line = line.split("#")[0]
                open_parenthesis += no_comment_line.count("(")
                open_parenthesis -= no_comment_line.count(")")
                if open_parenthesis == 0:
                    lambda_string =  "lambda :".join(re.split("lambda\s*:", no_comment_line)[1:])

                    if lambda_string:
                        lambda_string = "lambda :" + lambda_string


                    no_comment_line = re.split("lambda\s*:", no_comment_line)[0]


                    # we can possibly get an incorrect postfix from the first line of the signature, correct it here
                    postfix_index = no_comment_line.rfind(":") + 1
                    postfix = no_comment_line[postfix_index:]

                    comment = "#".join(line.split("#")[1:])

                    # find the correct start of postfixes with the new and corrected signature
                    signature_no_comment_line = lines[signature_line].split("#")[0]
                    signature_no_lambda_line = re.split("lambda\s*:", signature_no_comment_line)[0]


                    lines[signature_line] = lines[signature_line][:signature_no_lambda_line.rfind(":") + 1] + postfix + lambda_string + comment
                    lines[i] = str()
                    break
                lines[i] = str()
                i += 1
        return lines

    @staticmethod
    def get_annotated_variable_arguments(arg_spec : FullArgSpec) -> str:
        """
        gets annotated variable arguments string
        :param arg_spec: used to construct annotated variable arguments string
        :return: vararg annotated string
        """
        vararg_annotation = str()
        if arg_spec.varargs is not None:
            vararg_annotation += ", *" + arg_spec.varargs
            annotation = pavo_cristatus_get_argument_annotation(arg_spec, arg_spec.varargs)
            if annotation:
                vararg_annotation += (" : " + annotation)

        return vararg_annotation

    @staticmethod
    def get_annotated_keyword_arguments(arg_spec : FullArgSpec) -> str:
        """
        gets annotated keyword arguments string
        :param arg_spec: used to construct annotated keyword arguments string
        :return: keyword annotated string
        """
        keyword_annotation = str()
        if arg_spec.varkw is not None:
            keyword_annotation += ", **" + arg_spec.varkw
            annotation = pavo_cristatus_get_argument_annotation(arg_spec, arg_spec.varkw)
            if annotation:
                keyword_annotation += " : " + annotation
        return keyword_annotation

    # TODO: test key work only annotations!
    @staticmethod
    def get_annotated_keyword_only_arguments(arg_spec : FullArgSpec) -> str:
        """
        gets annotated keyword only arguments string
        :param arg_spec: used to construct annotated keyword only arguments string
        :return: keyword only annotated string
        """
        if arg_spec.kwonlyargs:
            keyword_only_annotations = ",*"
            for argument in arg_spec.kwonlyargs:
                annotation = pavo_cristatus_get_argument_annotation(arg_spec, argument)
                if annotation:
                    annotation = " : " + annotation

                if arg_spec.kwonlydefaults is not None:
                    keyword_only_annotations += ", {0}{1} = {2}".format(argument, annotation,
                                                                    arg_spec.kwonlydefaults[argument])
                else:
                    keyword_only_annotations += ", {0}{1}".format(argument, annotation)
            return keyword_only_annotations
        else:
            return str()
