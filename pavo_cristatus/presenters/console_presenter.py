__all__ = ["present_annotated_symbols"]

from collections import defaultdict
from typing import Any


def present_annotated_symbols(project_symbols_annotated_data_items):
    """
    print out project symbols to display annotated source
    :param project_symbols_annotated_data_items: ProjectSymbols object that we use to present annotated symbols
    :return: bool
    """
    for module_symbols, module_annotated_data_items in project_symbols_annotated_data_items.items():
        pavo_cristatus_print(module_symbols.get_annotated_source(module_annotated_data_items))
    return True

def pavo_cristatus_print(*args):
    print(*args)
