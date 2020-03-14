from pavo_cristatus.dependency_injection.ploceidae_configurator import pavo_cristatus_dependency_wrapper
from picidae import lazily_echo, access_attribute

from pavo_cristatus.symbol_signature_replacer import symbol_signature_replacer

dependency_module_name = "symbol_signature_replacer"

__all__ = [dependency_module_name]

pavo_cristatus_dependency_wrapper(resolvable_name=dependency_module_name,
                                  transformation=access_attribute("interaction"))(lambda: symbol_signature_replacer)

