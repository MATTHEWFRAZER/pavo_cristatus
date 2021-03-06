from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

__all__ = ["ModuleFakeClassWithInheritedAnnotatedMethod"]

class ModuleFakeClassWithAnnotatedMethod(object):
    # although this is a symbol of interest in respect to the sub stub module, it should not be collected
    def non_symbol_of_interest(self): pass

class ModuleFakeClassWithInheritedAnnotatedMethod(interoperable_with_metaclass_future(ModuleFakeClass)):
    class SymbolOfInterest(ModuleFakeClassWithAnnotatedMethod): pass

    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a : int, b : str) -> bool: pass
