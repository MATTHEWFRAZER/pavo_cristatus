from pavo_cristatus.testability.hook_point import HookPoint

__all__ = ["present_annotated_symbols"]

def present_annotated_symbols(project_symbols_annotated_data_items):
    for module_symbols, module_annotated_data_items in project_symbols_annotated_data_items.items():
        HookPoint.call(print.__name__, print, module_symbols.get_annotated_source(module_annotated_data_items))
    return True