from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithMultiplyLambdaDecoratedCallables"]

class ModuleFakeClassWithMultiplyLambdaDecoratedCallables(with_metaclass(ModuleFakeClass)):

    @(lambda f1: lambda self, x, y: f1(self, x, y))
    @(lambda f2: lambda self, x, y: f2(self, x, y))
    @(lambda f3: lambda self, x, y: f3(self, x, y))
    def symbol_of_interest(self, a : int, b : str) -> bool: pass

    @(lambda f1: lambda self, x, y: f1(self, x, y))
    @(lambda f2: lambda self, x, y: f2(self, x, y))
    @(lambda f3: lambda self, x, y: f3(self, x, y))
    def non_symbol_of_interest(self, a, b): pass