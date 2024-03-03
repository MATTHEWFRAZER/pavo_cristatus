import collections
import inspect
from typing import Callable, Any

from pavo_cristatus.project_loader.nested_symbol_collector import collect_nested_symbols
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.utilities import is_symbol_callable


def breadth_first_search_for_symbol(normalized_symbol, predicate):
    queue = collections.deque()
    queue.appendleft(normalized_symbol)
    while queue:
        current = queue.pop()
        for nested_symbol in collect_nested_symbols(current):
            if predicate(nested_symbol):
                return True
            queue.appendleft(nested_symbol)
    return False

def does_symbol_contain_symbol_of_interest(module, normalized_symbol, is_symbol_of_interest):
    return breadth_first_search_for_symbol(normalized_symbol, lambda x: is_symbol_of_interest(module, x))

def does_symbol_have_type_hint_annotations(normalized_symbol):
    return bool(inspect.getfullargspec(normalized_symbol.symbol).annotations)

def is_symbol_defined_in_module(module, normalized_symbol):
    try:
        return module.__name__ == normalized_symbol.module
    except Exception:
        return False

def is_annotated_symbol_of_interest_inner(module, normalized_symbol):
    # TODO: get rid of these checks (they are already someplace else)
    if None in (module, normalized_symbol):
        return False

    # we check this because imported objects might get included
    if not is_symbol_defined_in_module(module, normalized_symbol):
        return False

    return is_symbol_callable(normalized_symbol.symbol) and does_symbol_have_type_hint_annotations(normalized_symbol)


def is_non_annotated_symbol_of_interest_inner(module, normalized_symbol):
    # TODO: get rid of these checks (they are already someplace else)
    if None in (module, normalized_symbol):
        return False
    # we check this because imported objects might get included
    if not is_symbol_defined_in_module(module, normalized_symbol):
        return False
    return is_symbol_callable(normalized_symbol.symbol) and not does_symbol_have_type_hint_annotations(normalized_symbol)

def is_annotated_symbol_of_interest(module, normalized_symbol):
    if not is_symbol_valid(module, normalized_symbol):
        return False

    return is_annotated_symbol_of_interest_inner(module, normalized_symbol) or does_symbol_contain_symbol_of_interest(module, normalized_symbol,
                                                           is_annotated_symbol_of_interest_inner)
def is_non_annotated_symbol_of_interest(module, normalized_symbol):
    if not is_symbol_valid(module, normalized_symbol):
        return False
    return is_non_annotated_symbol_of_interest_inner(module, normalized_symbol) or \
           does_symbol_contain_symbol_of_interest(module, normalized_symbol, is_non_annotated_symbol_of_interest_inner)

def is_symbol_valid(module, normalized_symbol):
    if None in (module, normalized_symbol):
        return False
    # we check this because imported objects might get included
    if not is_symbol_defined_in_module(module, normalized_symbol):
        return False

    return True
