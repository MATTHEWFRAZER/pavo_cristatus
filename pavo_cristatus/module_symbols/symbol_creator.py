import inspect

from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol

__all__ = ["create"]

def create(project_root_path, symbol):
    """
    create a symbol object that associates nested symbols with a symbol object
    :param project_root_path: the project root of the source
    :param symbol: used to construct symbol object
    :return: SymbolObject
    """
    return ClassSymbol(symbol, []) if inspect.isclass(symbol) else CallableSymbol(project_root_path, symbol, [])