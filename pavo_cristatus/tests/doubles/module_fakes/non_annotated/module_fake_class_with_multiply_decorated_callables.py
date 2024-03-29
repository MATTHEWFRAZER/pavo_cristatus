from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithMultiplyDecoratedCallables"]

def decorator(func):
    def nested(self, x, y):
        return func(self, x, y)
    return nested

def decorator2(func):
    def nested(self, x, y):
        return func(self, x, y)
    return nested

def decorator3(func):
    def nested(self, x, y):
        return func(self, x, y)
    return nested

class ModuleFakeClassWithMultiplyDecoratedCallables(with_metaclass(ModuleFakeClass)):

    @decorator
    @decorator2
    @decorator3
    def symbol_of_interest(self, a, b): pass

    @decorator
    @decorator2
    @decorator3
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass