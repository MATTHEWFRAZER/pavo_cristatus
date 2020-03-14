from picidae import access_attribute

from pavo_cristatus.utilities import write_new_source

__all__ = ["replace"]

def replace(project_symbols):
       """
       replace old source with non annotated signatures
       :param project_symbols: symbols we will use to write out new source code
       :return: bool
       """
       for module_symbols in project_symbols:
              if not write_new_source(module_symbols, access_attribute("get_non_annotated_source")):
                     return False
       return True




