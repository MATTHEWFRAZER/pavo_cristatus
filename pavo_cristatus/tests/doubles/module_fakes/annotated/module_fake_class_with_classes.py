from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

__all__ = ["ModuleFakeClassWithClasses"]

class ModuleFakeClassWithClasses(interoperable_with_metaclass_future(ModuleFakeClass)):
    class SymbolOfInterest:
        def symbol_of_interest(self, a : int, b : str) -> bool: pass
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a, b): pass
