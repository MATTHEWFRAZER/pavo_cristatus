from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithNestedLambdaDecoratedCallables"]

class ModuleFakeClassWithNestedLambdaDecoratedCallables(with_metaclass(ModuleFakeClass)):

    def symbol_of_interest(self, a, b):
        @(lambda f: lambda self, x, y: f(self, x, y))
        def nested(a, b): pass

    def non_symbol_of_interest(self, a : int, b : str) -> bool:
        @(lambda f: lambda self, x, y: f(self, x, y))
        def nested(a, b): pass
