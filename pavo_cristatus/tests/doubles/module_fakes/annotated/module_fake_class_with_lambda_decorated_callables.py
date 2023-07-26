from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithLambdaDecoratedCallables"]

class ModuleFakeClassWithLambdaDecoratedCallables(with_metaclass(ModuleFakeClass)):

    @(lambda f: lambda self, x, y: f(self, x, y))
    def symbol_of_interest(self, a : int, b : str) -> bool: pass

    @(lambda f: lambda self, x, y: f(self, x, y))
    def non_symbol_of_interest(self, a, b): pass
