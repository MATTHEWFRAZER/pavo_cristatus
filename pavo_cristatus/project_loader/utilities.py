import collections
import inspect

__all__ = ["is_symbol_of_interest"]

from pavo_cristatus.project_loader.nested_symbol_collector import collect_nested_symbols
from pavo_cristatus.utilities import is_symbol_callable


def breadth_first_search_for_symbol(symbol, predicate):
    queue = collections.deque()
    queue.appendleft(symbol)
    while queue:
        current = queue.pop()
        for nested_symbol in collect_nested_symbols(current):
            if predicate(nested_symbol):
                return True
            queue.appendleft(nested_symbol)
    return False

def does_symbol_contain_symbol_of_interest(module, symbol, is_symbol_of_interest):
    return breadth_first_search_for_symbol(symbol, lambda x: is_symbol_of_interest(module, x))

def does_symbol_have_type_hint_annotations(symbol):
    return bool(inspect.getfullargspec(symbol).annotations)

def is_symbol_defined_in_module(module, symbol):
    try:
        return module == symbol.__module__
    except:
        return False

def is_annotated_symbol_of_interest_inner(module, symbol):
    if None in (module, symbol):
        return False
    # we check this because imported objects might get included
    if not is_symbol_defined_in_module(module, symbol):
        return False
    return is_symbol_callable(symbol) and does_symbol_have_type_hint_annotations(symbol)

def is_non_annotated_symbol_of_interest_inner(module, symbol):
    if None in (module, symbol):
        return False
    # we check this because imported objects might get included
    if not is_symbol_defined_in_module(module, symbol):
        return False
    return is_symbol_callable(symbol) and not does_symbol_have_type_hint_annotations(symbol)

def is_annotated_symbol_of_interest(module, symbol):
    return is_annotated_symbol_of_interest_inner(module, symbol) or \
           does_symbol_contain_symbol_of_interest(module, symbol, is_annotated_symbol_of_interest_inner)

def is_non_annotated_symbol_of_interest(module, symbol):
    return is_non_annotated_symbol_of_interest_inner(module, symbol) or \
           does_symbol_contain_symbol_of_interest(module, symbol, is_non_annotated_symbol_of_interest_inner)