from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithDecoratedClasses"]

def decorator(c):
    def nested():
        return None
    return nested

class ModuleFakeClassWithDecoratedClasses(with_metaclass(ModuleFakeClass)):
    # TODO: investigate other ways in which we can retrieve a class, right now it is only if we do a lambda return
    @decorator
    class SymbolOfInterest:
        def symbol_of_interest(self, a, b): pass

    @decorator
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a : int, b : str) -> bool: pass