from itertools import chain

from pavo_cristatus.utilities import resolve_correct_symbol
from pavo_cristatus.utilities import collect_nested_symbols_in_object_source


__all__ = ["collect_nested_symbols_in_object_dict"]

def collect_nested_symbols(symbol):
    """
    from a symbol object, collect nested symbols
    :param symbol: used to collect nested symbols
    :return: iterable of nested symbols
    """
    dict_values = collect_nested_symbols_in_object_dict(symbol)
    nested_code_objects = collect_nested_symbols_in_object_source(symbol)
    return chain.from_iterable((dict_values, nested_code_objects))

def collect_nested_symbols_in_object_dict(symbol):
    """
    from a symbol object, get its values list
    :param symbol: used to find nested symbols in a a symbols object dict
    :return: dict values from symbol
    """
    try:
        for nested_symbol_name, nested_symbol in symbol.__dict__.items():
            # there is potential in the case of a decorator where the symbol's name does not match its name in the namespace
            resolved_symbol = resolve_correct_symbol(nested_symbol_name, nested_symbol)
            if resolved_symbol is not None:
                resolved_symbol.__module__ = symbol.__module__
                yield resolved_symbol
    except AttributeError:
        return tuple()

