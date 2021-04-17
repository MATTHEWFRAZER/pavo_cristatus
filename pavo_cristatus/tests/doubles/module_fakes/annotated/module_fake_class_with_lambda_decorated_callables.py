from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

__all__ = ["ModuleFakeClassWithLambdaDecoratedCallables"]

class ModuleFakeClassWithLambdaDecoratedCallables(interoperable_with_metaclass_future(ModuleFakeClass)):

    @(lambda f: lambda self, x, y: f(self, x, y))
    def symbol_of_interest(self, a : int, b : str) -> bool: pass

    @(lambda f: lambda self, x, y: f(self, x, y))
    def non_symbol_of_interest(self, a, b): pass
