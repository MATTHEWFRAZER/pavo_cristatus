from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

__all__ = ["ModuleFakeClassWithDecoratedCallables"]

def decorator(func):
    def nested(self, x, y):
        return func(self, x, y)
    return nested

class ModuleFakeClassWithDecoratedCallables(interoperable_with_metaclass_future(ModuleFakeClass)):

    @decorator
    def symbol_of_interest(self, a, b): pass

    @decorator
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass