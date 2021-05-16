from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

__all__ = ["ModuleFakeClassWithLambdaDecoratedClasses"]

class ModuleFakeClassWithLambdaDecoratedClasses(interoperable_with_metaclass_future(ModuleFakeClass)):
    # TODO: investigate other ways in which we can retrieve a class, right now it is only if we do a lambda return
    @(lambda c: lambda: None)
    class SymbolOfInterest:
        def symbol_of_interest(self, a : int, b : str) -> bool: pass

    @(lambda c: lambda: None)
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a, b): pass

