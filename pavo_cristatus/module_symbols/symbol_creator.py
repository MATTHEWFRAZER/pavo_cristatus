import inspect
from typing import Any

from pavo_cristatus.module_symbols.abstract_symbol import AbstractSymbol
from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol

__all__ = ["create"]


def create(module_path, normalized_symbol):
    """
    create a symbol object that associates nested symbols with a symbol object
    :param module_path : the path of the module
    :param normalized_symbol: used to construct symbol object
    :return: SymbolObject
    """
    return ClassSymbol(normalized_symbol, []) if inspect.isclass(normalized_symbol.symbol) else CallableSymbol(module_path, normalized_symbol, [])
