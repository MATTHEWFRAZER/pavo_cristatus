from itertools import chain

__all__ = ["collect_nested_symbols_in_object_dict"]

from pavo_cristatus.utilities import collect_nested_symbols_in_object_source


def collect_nested_symbols(symbol):
    dict_values = collect_nested_symbols_in_object_dict(symbol)
    nested_code_objects = collect_nested_symbols_in_object_source(symbol)
    return chain.from_iterable((dict_values, nested_code_objects))

def collect_nested_symbols_in_object_dict(symbol):
    try:
        return symbol.__dict__.values()
    except AttributeError:
        return tuple()