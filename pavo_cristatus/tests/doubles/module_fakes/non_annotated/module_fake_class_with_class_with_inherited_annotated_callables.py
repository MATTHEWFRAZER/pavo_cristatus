from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithInheritedAnnotatedCallables"]

class ModuleFakeClassWithAnnotatedCallables(object):
    # although this is a symbol of interest in respect to the sub stub module, it should not be collected
    def non_symbol_of_interest(self): pass

class ModuleFakeClassWithInheritedAnnotatedCallables(with_metaclass(ModuleFakeClass)):
    class SymbolOfInterest(ModuleFakeClassWithAnnotatedCallables): pass

    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a : int, b : str) -> bool: pass
