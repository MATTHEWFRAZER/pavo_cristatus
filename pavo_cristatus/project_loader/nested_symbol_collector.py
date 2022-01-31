from itertools import chain
from typing import Generator, Iterator, Union

from trochilidae.interoperable_filter import interoperable_filter

from pavo_cristatus.constants import LAMBDA_STRING
from pavo_cristatus.project_loader.normalized_module_symbol import NormalizedModuleSymbol
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol


__all__ = ["collect_nested_symbols_in_object_dict"]

def collect_nested_symbols(normalized_symbol):
    """
    from a symbol object, collect nested symbols
    :param normalized_symbol: used to collect nested symbols
    :return: iterable of nested symbols
    """
    dict_values = collect_nested_symbols_in_object_dict(normalized_symbol)
    nested_code_objects = collect_nested_symbols_in_object_source(normalized_symbol)
    return chain.from_iterable((dict_values, nested_code_objects))

def collect_nested_symbols_in_object_dict(normalized_symbol):
    """
    from a symbol object, get its values list
    :param normalized_symbol: used to find nested symbols in a a symbols object dict
    :return: generator of NormalizedSymbol
    """
    for nested_symbol_name, nested_symbol in normalized_symbol.symbol.__dict__.items():
        # TODO: handle properties
        if type(nested_symbol) == property:
            continue

        # TODO: handle static methods
        if type(nested_symbol) == staticmethod:
            continue

        if nested_symbol is None:
            continue
        # there is potential in the case of a decorator where the symbol's name does not match its name in the namespace
        try:
            yield NormalizedSymbol(nested_symbol, normalized_symbol, nested_symbol_name)
        except ValueError:
            continue

def collect_nested_symbols_in_object_source(normalized_symbol):
    """
    from a symbol object, get its values list
    :param normalized_symbol: used to find nested symbols in a a symbols object dict
    :return: generator of NormalizedSymbol
    """
    code_object = getattr(normalized_symbol.symbol, "__code__", tuple())
    nested_const = getattr(code_object, "co_consts", tuple())
    nested_code_objects = interoperable_filter(lambda x: code_object is not None and type(x) is type(code_object) and code_object.co_name != LAMBDA_STRING, nested_const)
    for nested_code_object in nested_code_objects:
        if nested_code_object is None:
            continue
        try:
            yield NormalizedSymbol.from_context_with_no_symbol(normalized_symbol, nested_code_object.co_name)
        except ValueError:
            continue


