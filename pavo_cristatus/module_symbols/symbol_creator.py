import inspect

from pavo_cristatus.module_symbols.callable_symbol import CallableSymbol
from pavo_cristatus.module_symbols.class_symbol import ClassSymbol

__all__ = ["create"]

def create(project_root_path, symbol):
    return ClassSymbol(symbol, []) if inspect.isclass(symbol) else CallableSymbol(project_root_path, symbol, [])