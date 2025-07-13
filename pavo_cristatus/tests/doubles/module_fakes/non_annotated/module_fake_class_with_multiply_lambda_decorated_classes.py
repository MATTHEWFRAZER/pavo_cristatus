from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithMultiplyLambdaDecoratedClasses"]

class ModuleFakeClassWithMultiplyLambdaDecoratedClasses(with_metaclass(ModuleFakeClass)):
    # TODO: investigate other ways in which we can retrieve a class, right now it is only if we do a lambda return
    @(lambda c1: lambda: None)
    @(lambda c2: lambda: None)
    @(lambda c3: lambda: None)
    class SymbolOfInterest:
        def symbol_of_interest(self, a, b): pass

    @(lambda c1: lambda: None)
    @(lambda c2: lambda: None)
    @(lambda c3: lambda: None)
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a : int, b : str) -> bool: pass