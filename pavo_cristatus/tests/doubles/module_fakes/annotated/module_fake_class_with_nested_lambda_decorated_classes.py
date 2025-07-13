from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithNestedLambdaDecoratedClasses"]

class ModuleFakeClassWithNestedLambdaDecoratedClasses(with_metaclass(ModuleFakeClass)):

    def symbol_of_interest(self, a, b):
        # TODO: investigate other ways in which we can retrieve a class, right now it is only if we do a lambda return
        @(lambda c: lambda: None)
        class SymbolOfInterest:
            def symbol_of_interest(self, a: int, b: str) -> bool: pass

    def non_symbol_of_interest(self, a, b): pass
