from picidae import access_attribute

from pavo_cristatus.utilities import write_new_source

__all__ = ["restore"]

def restore(project_symbols_annotated_data_items):
    for module_symbols, module_annotated_data_items in project_symbols_annotated_data_items.items():
        if not write_new_source(module_symbols, access_attribute("get_annotated_source"), module_annotated_data_items):
            return False
    return True