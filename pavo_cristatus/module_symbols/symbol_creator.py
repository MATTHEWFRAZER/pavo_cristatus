import inspect
import itertools

from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol
from pavo_cristatus.utilities import normalize_symbol, pavo_cristatus_get_source, pavo_cristatus_strip_source, \
    is_decorated_line, is_decorated_symbol

__all__ = ["create"]


def create(project_root_path, symbol):
    """
    create a symbol object that associates nested symbols with a symbol object
    :param project_root_path: the project root of the source
    :param symbol: used to construct symbol object
    :return: SymbolObject
    """
    symbol_name = get_bound_name_from_symbol(symbol)
    source = pavo_cristatus_get_source(symbol)
    if is_decorated_symbol(source):
        stripped_source = pavo_cristatus_strip_source(source)
        normalized_symbol = normalize_symbol(symbol, stripped_source, source, symbol_name)
        if normalized_symbol is None:
            normalized_symbol = symbol
        else:
            normalized_symbol.pavo_cristatus_original_source_file = inspect.getsourcefile(symbol)
    else:
        normalized_symbol = symbol
    return ClassSymbol(normalized_symbol, []) if inspect.isclass(normalized_symbol) else CallableSymbol(project_root_path, normalized_symbol, [])

def get_bound_name_from_symbol(symbol):
    if symbol.__name__ != "<lambda>":
        return symbol.__name__
    else:
        source = inspect.getsource(symbol)
        lines = source.split("\n")
        for line in lines:
            if is_decorated_line(line):
                function_name = line.strip().split()[1]
                return "".join(itertools.takewhile(lambda x: x not in ("(", ":", " "), function_name))
        else:
            return str()