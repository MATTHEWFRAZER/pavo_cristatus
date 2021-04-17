import inspect

from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol

__all__ = ["create"]


def create(project_root_path, normalized_symbol):
    """
    create a symbol object that associates nested symbols with a symbol object
    :param project_root_path: the project root of the source
    :param normalized_symbol: used to construct symbol object
    :return: SymbolObject
    """
    return ClassSymbol(normalized_symbol, []) if inspect.isclass(normalized_symbol.symbol) else CallableSymbol(project_root_path, normalized_symbol, [])