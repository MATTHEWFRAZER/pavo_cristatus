import inspect
import re

from pavo_cristatus.module_symbols.regex_patterns import get_class_pattern, get_function_pattern
from pavo_cristatus.utilities import pavo_cristatus_get_source, pavo_cristatus_split


class AbstractSymbol(object):
    """
    Abstract class for Symbol, handles finding line numbers of a this symbol in the source.
    """
    def __init__(self, normalized_symbol, nested_symbols):
        self.normalized_symbol = normalized_symbol
        # getsource and accessing __qualname__ or __name__ can can raise an exception
        # get full argspec has a try/except because we need those symbols that are annotated or not
        self.source = normalized_symbol.source

        self.qualname = normalized_symbol.qualname
        self.module = normalized_symbol.module
        self.name = normalized_symbol.name
        self.arg_spec = normalized_symbol.arg_spec
        self.nested_symbols = nested_symbols

    def find_line_number_of_symbol_in_source(self, source):
        # pattern_to_match = get_class_pattern(self.name) if inspect.isclass(self.symbol.symbol) else get_function_pattern(self.name)
        # lines = pavo_cristatus_split(source)
        # for line_number, line in enumerate(lines):
        #     if re.search(pattern_to_match, line):
        #         return line_number
        # return -1
        return self.normalized_symbol.find_line_number_of_symbol_in_source(source)

    def find_line_number_of_symbol_in_module(self):
        return self.normalized_symbol.find_line_number_of_symbol_in_module()