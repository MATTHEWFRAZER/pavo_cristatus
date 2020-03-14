import inspect
import re

from pavo_cristatus.module_symbols.regex_patterns import get_class_pattern, get_function_pattern, all_whitespace_pattern

class AbstractSymbol(object):
    """
    Abstract class for Symbol, handles finding line numbers of a this symbol in the source.
    """
    def __init__(self, symbol, nested_symbols):
        self.symbol = symbol
        # getsource and accessing __qualname__ or __name__ can can raise an exception
        # get full argspec has a try/except because we need those symbols that are annotated or not
        try:
            self.source = inspect.getsource(symbol)
        except OSError:
            # we can not use getsource on nested symbols, since we generate the nested symbol, we tack this
            # attribute on to it and pass it along
            self.source = symbol.pavo_cristatus_nested_symbol_source

        self.qualname = symbol.__qualname__
        self.module = symbol.__module__
        self.name = symbol.__name__
        try:
            self.arg_spec = inspect.getfullargspec(symbol)
        except Exception:
            self.arg_spec = None
        self.nested_symbols = nested_symbols

    def find_line_number_of_symbol_in_source(self, source):
        pattern_to_match = get_class_pattern(self.symbol) if inspect.isclass(self.symbol) else get_function_pattern(self.symbol)
        lines = source.split("\n")
        for line_number, line in enumerate(lines):
            line_without_whitespace = re.sub(all_whitespace_pattern, '', line)
            if re.match(pattern_to_match, line_without_whitespace):
                return line_number
        return -1
