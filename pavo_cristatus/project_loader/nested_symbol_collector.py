from itertools import chain

__all__ = ["collect_nested_symbols_in_object_dict"]

from pavo_cristatus.utilities import collect_nested_symbols_in_object_source


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
        return symbol.__dict__.values()
    except AttributeError:
        return tuple()