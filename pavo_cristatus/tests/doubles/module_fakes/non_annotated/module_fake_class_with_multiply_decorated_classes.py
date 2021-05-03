from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

__all__ = ["ModuleFakeClassWithMultiplyDecoratedClasses"]

def decorator1(c):
    def nested():
        return None
    return nested

def decorator2(c):
    def nested():
        return None
    return nested

def decorator3(c):
    def nested():
        return None
    return nested

class ModuleFakeClassWithMultiplyDecoratedClasses(interoperable_with_metaclass_future(ModuleFakeClass)):
    # TODO: investigate other ways in which we can retrieve a class, right now it is only if we do a lambda return
    @decorator1
    @decorator2
    @decorator3
    class SymbolOfInterest:
        def symbol_of_interest(self, a, b): pass

    @decorator1
    @decorator2
    @decorator3
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a : int, b : str) -> bool: pass