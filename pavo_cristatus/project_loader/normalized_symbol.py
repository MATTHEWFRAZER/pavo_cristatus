import inspect
import itertools
import re

import more_itertools

from pavo_cristatus.constants import LAMBDA_STRING
from pavo_cristatus.module_symbols.regex_patterns import get_class_pattern, get_function_pattern
from pavo_cristatus.pavo_cristatus_namespace import PavoCristatusNamespace
from pavo_cristatus.utilities import pavo_cristatus_split, is_decorator_line


class NormalizedSymbol(object):
    def __init__(self, symbol, normalized_parent_symbol, normalized_child_name):
        self.original_symbol = symbol
        self.original_source = self.get_original_source(self.original_symbol, normalized_parent_symbol, normalized_child_name)
        # TODO: why do we strip + \n here?
        self.original_source = self.original_source.strip() + "\n"
        self.normalized_source = self.get_normalized_source(self.original_source)
        self._name = self.get_name(self.original_symbol, self.normalized_source, normalized_child_name)

        if symbol is not None and self.original_symbol.__name__ == self._name:
            self._symbol = self.original_symbol
        else:
            self._symbol = self.normalize_symbol(self.normalized_source, self._name)

        self._file = self.get_file(normalized_parent_symbol)
        self._qualname = self.get_qualname(self._name, self._symbol, normalized_parent_symbol)
        self._arg_spec = self.get_arg_spec(self._symbol)
        self._indent = self.find_symbol_indent_in_source(self.original_symbol, normalized_parent_symbol, self.name)
        self._module = self.get_module(symbol, normalized_parent_symbol)

    @classmethod
    def from_context_with_no_symbol(cls, normalized_parent_symbol, normalized_child_name):
        instance = cls(None, normalized_parent_symbol, normalized_child_name)
        instance.original_symbol = instance.symbol
        instance.original_source = instance.normalized_source
        return instance

    @property
    def file(self):
        return self._file

    @property
    def module(self):
        return self._module

    @property
    def source(self):
        if not is_decorator_line(self.original_source):
            return self.original_source
        else:
            return self.indent + self.original_source

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @property
    def qualname(self):
        return self._qualname

    @property
    def arg_spec(self):
        return self._arg_spec

    @property
    def indent(self):
        return self._indent

    def get_file(self, normalized_parent_symbol):
        if normalized_parent_symbol is not None:
            return normalized_parent_symbol.file
        else:
            return inspect.getsourcefile(self.original_symbol)

    def get_arg_spec(cls, symbol):
        try:
            return inspect.getfullargspec(symbol)
        except Exception:
            return None

    @classmethod
    def get_module(cls, symbol, normalized_parent_symbol):
        if normalized_parent_symbol is not None:
            return normalized_parent_symbol.module
        else:
            return symbol.__module__

    @classmethod
    def get_qualname(cls, name, symbol, normalized_parent_symbol):
        try:
            return symbol.__qualname__
        except AttributeError:
            # TODO: handle the case where there are nested sibling symbols
            if normalized_parent_symbol is None:
                raise ValueError("normalized parent symbol required to get qualname for nested symbols")
            return ".".join((normalized_parent_symbol.qualname, name))

    @classmethod
    def normalize_symbol(cls, normalized_source, normalized_child_name):
        namespace = PavoCristatusNamespace(lambda x, y: True)

        normalized_source = normalized_source.strip()
        try:
            compiled_source = compile(normalized_source, '<string>', 'exec')
        except Exception:
            raise ValueError("normalized source could not be compiled: {0}".format(normalized_source))

        try:
            # TODO: find out if I can eliminate this security risk. Right now it is what I have for retrieving nested symbols
            exec(compiled_source, namespace)
        except Exception:
            raise ValueError("normalized source could not be loaded: {0}".format(normalized_source))

        try:
            nested_symbol = namespace[normalized_child_name]
        except KeyError:
            raise ValueError("normalized source could not be resolved with name {0}: {1}".format(normalized_child_name, normalized_source))

        return nested_symbol

    @classmethod
    def get_normalized_source(cls, original_source):
        normalized_source = ""
        lines = pavo_cristatus_split(original_source)
        for line in lines:
            if line and not is_decorator_line(line):
                normalized_source += line + "\n"
        return normalized_source.strip() + "\n"

    @classmethod
    def get_original_source(cls, symbol, normalized_parent_symbol, normalized_child_name):
        if normalized_parent_symbol is not None:
            if normalized_child_name is None:
                raise ValueError("normalized parent must provide child to normalize with its name")
            normalized_parent_source = normalized_parent_symbol.source
            class_pattern = get_class_pattern(normalized_child_name)
            function_pattern = get_function_pattern(normalized_child_name)
            class_pattern_matches = list(re.finditer(class_pattern, normalized_parent_source))
            function_pattern_matches = list(re.finditer(function_pattern, normalized_parent_source))
            if len(class_pattern_matches) + len(function_pattern_matches) > 1:
                # TODO: write a specific test case for this
                return cls.resolve_source_with_conflicts_in_parent_source(normalized_parent_source, class_pattern,
                                                                          function_pattern)
            elif class_pattern_matches:
                return cls.resolve_source_from_match(normalized_parent_source, class_pattern_matches[0], class_pattern)
            elif function_pattern_matches:
                return cls.resolve_source_from_match(normalized_parent_source, function_pattern_matches[0],
                                                     function_pattern)
            else:
                raise ValueError("source does not contain callable or class definitions")
        else:
            if symbol is None:
                raise ValueError("None symbol provided where it was required")
            return inspect.getsource(symbol)

    def find_line_number_of_symbol_in_module(self):

        # we need to handle decorated symbols (inspect.findsource returns the line number before the top decorator in source)
        lines = pavo_cristatus_split(self.original_source)
        decorator_offset = 0
        for line in lines:
            if not is_decorator_line(line):
                break
            else:
                decorator_offset += 1

        return inspect.findsource(self.original_symbol)[1] + decorator_offset


    def find_line_number_of_symbol_in_source(self, source):
        class_pattern = get_class_pattern(self.name)
        function_pattern = get_function_pattern(self.name)
        class_pattern_matches = list(re.finditer(class_pattern, source))
        function_pattern_matches = list(re.finditer(function_pattern, source))
        if len(class_pattern_matches) + len(function_pattern_matches) > 1:
            return self.resolve_line_number_with_conflicts_in_source(source, class_pattern, function_pattern)
        elif class_pattern_matches:
            return self.resolve_line_number_from_match(source, class_pattern)
        elif function_pattern_matches:
            return self.resolve_line_number_from_match(source, function_pattern)
        else:
            raise ValueError("source does not contain callable or class definitions")

    def resolve_line_number_with_conflicts_in_source(self, source, class_pattern, function_pattern):
        lines = pavo_cristatus_split(source)
        if len(lines) < 2:
            raise ValueError("symbol source is only one line, can not resolve pattern match conflicts")

        source_indent = self.get_indentation_level(lines[0])

        # we need to find the base unit for the indent
        number_of_characters_in_indent = self.get_indentation_level(lines[1]) - source_indent
        if number_of_characters_in_indent != 0:
            number_of_indents_for_parent = source_indent / number_of_characters_in_indent
        else:
            number_of_indents_for_parent = 0

        line_number = -1
        for i, line in enumerate(lines):
            if re.match(class_pattern, line) or re.match(function_pattern, line):
                child_indent = self.get_indentation_level(line)
                # need to handle the case where we overwrite symbols in namespace
                # example:
                # def x():
                #       class a: pass
                #       def a(): pass
                # we should resolve function a
                if source_indent == 0 or (child_indent / number_of_characters_in_indent) - number_of_indents_for_parent == 1:
                    line_number = i

        return line_number

    def resolve_line_number_from_match(self, source, pattern):
        lines = pavo_cristatus_split(source)
        if len(lines) < 2:
            return 0

        source_indent = self.get_indentation_level(lines[0])

        # we need to find the base unit for the indent
        number_of_characters_in_indent = self.get_indentation_level(lines[1]) - source_indent
        if number_of_characters_in_indent != 0:
            number_of_indents_for_parent = source_indent / number_of_characters_in_indent
        else:
            number_of_indents_for_parent = 0

        for i, line in enumerate(lines):
            if re.search(pattern, line):
                child_indent = self.get_indentation_level(line)
                if source_indent == 0 or number_of_characters_in_indent == 0 or ((child_indent / number_of_characters_in_indent) - number_of_indents_for_parent) == 1:
                    return i
        else:
            return -1

    @classmethod
    def resolve_source_with_conflicts_in_parent_source(cls, normalized_parent_source, class_pattern, function_pattern):
        lines = pavo_cristatus_split(normalized_parent_source)
        if len(lines) < 2:
            raise ValueError("symbol source is only one line, can not resolve pattern match conflicts")

        parent_indent = cls.get_indentation_level(lines[0])

        # we need to find the base unit for the indent
        number_of_characters_in_indent = cls.get_indentation_level(lines[1]) - parent_indent
        if number_of_characters_in_indent != 0:
            number_of_indents_for_parent = parent_indent / number_of_characters_in_indent
        else:
            number_of_indents_for_parent = 0

        resolved_source = ""
        found_match = False
        for line in lines:
            stripped_line = line.strip()
            if re.match(class_pattern, stripped_line) or re.match(function_pattern, stripped_line):
                child_indent = cls.get_indentation_level(line)
                # need to handle the case where we overwrite symbols in namespace
                # example:
                # def x():
                #       class a: pass
                #       def a(): pass
                # we should resolve function a
                if number_of_characters_in_indent == 0 or ((child_indent / number_of_characters_in_indent) - number_of_indents_for_parent) == 1:
                    resolved_source = ""
                    found_match = True
            if found_match:
                resolved_source += line

        return resolved_source

    @classmethod
    def resolve_source_from_match(cls, normalized_parent_source, pattern_match, child_symbol_pattern):
        it = iter(normalized_parent_source)
        more_itertools.consume(it, pattern_match.start())
        modified_parent_source = "".join(it)
        lines = pavo_cristatus_split(modified_parent_source)

        # iterate until we find an indentation level that is less than what the child symbol starts at, construct source as we go
        resolved_source = ""
        expected_indent_level = cls.find_symbol_indent_in_parent_symbol_source(normalized_parent_source,
                                                                               child_symbol_pattern)
        for line in lines:
            if cls.get_indentation_level(line) < expected_indent_level:
                break
            resolved_source += line + "\n"
        return resolved_source

    @classmethod
    def get_indentation_level(cls, line):
        return len(line) - len(line.strip())

    @classmethod
    def get_name(cls, original_symbol, source, normalized_child_name):
        if original_symbol is not None and original_symbol.__name__ != LAMBDA_STRING:
            return original_symbol.__name__
        elif normalized_child_name is not None:
            return normalized_child_name
        else:
            lines = pavo_cristatus_split(source)
            for line in lines:
                if cls.is_decorated_line(line):
                    function_name = line.strip().split()[1]
                    return "".join(itertools.takewhile(lambda x: x not in ("(", ":", " ", "\t"), function_name))
            else:
                raise ValueError("symbol {0} does not have resolvable name".format(original_symbol))

    @classmethod
    def is_decorated_line(cls, line):
        return line.strip().startswith("def") or line.strip().startswith("class")

    @classmethod
    def find_symbol_indent_in_parent_symbol_source(cls, parent_source, child_symbol_pattern):
        """
        given a parent source and a child symbol pattern to match, we find the indentation for the child symbol
        we will use the result of this function to find the end of a child symbol's source inside of the parent's source
        """
        # Here we assume:
        # 1) you can not mix indents with spaces so this should work
        # 2) we are in a state where there will be only one match to the pattern
        lines = pavo_cristatus_split(parent_source)
        parent_indent = cls.get_indentation_level(lines[0])
        for line in lines:
            try:
                if re.search(child_symbol_pattern, line):
                    matched_line = line
                    break
            except re.error:
                raise ValueError("ran into error at line {0}".format(line))
        else:
            raise ValueError("source does not contain callable or class definitions")

        child_indent = cls.get_indentation_level(matched_line)
        return parent_indent - child_indent

    @classmethod
    def find_symbol_indent_in_source(cls, symbol, normalized_parent_symbol, name):
        if normalized_parent_symbol is not None:
            return cls.find_symbol_indent_in_source_inner(normalized_parent_symbol.source, name)
        else:
            return cls.find_symbol_indent_in_source_inner(inspect.getsource(symbol), name)

    @classmethod
    def find_symbol_indent_in_source_inner(cls, source, name):
        class_pattern = get_class_pattern(name)
        function_pattern = get_function_pattern(name)
        if re.search(class_pattern, source):
            child_symbol_pattern = class_pattern
        elif re.search(function_pattern, source):
            child_symbol_pattern = function_pattern
        else:
            raise ValueError("Could not find pattern match on {0} to get indent".format(name))

        lines = pavo_cristatus_split(source)
        for line in lines:
            try:
                match = re.search(child_symbol_pattern, line)
                if match:
                    return line[: match.start()]
            except re.error:
                raise ValueError("ran into error at line {0}".format(line))



