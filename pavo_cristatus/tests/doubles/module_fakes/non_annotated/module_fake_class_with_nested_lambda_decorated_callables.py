from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

__all__ = ["ModuleFakeClassWithNestedLambdaDecoratedCallables"]

class ModuleFakeClassWithNestedLambdaDecoratedCallables(interoperable_with_metaclass_future(ModuleFakeClass)):

    def symbol_of_interest(self, a, b): pass

    def non_symbol_of_interest(self, a : int, b : str) -> bool:
        @(lambda f: lambda self, x, y: f(self, x, y))
        def nested(a, b): pass
