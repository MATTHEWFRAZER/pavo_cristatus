from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

__all__ = ["ModuleFakeClassWithClassesWithNestedAnnotatedCallables"]

class ModuleFakeClassWithClassesWithNestedAnnotatedCallables(interoperable_with_metaclass_future(ModuleFakeClass)):
    class SymbolOfInterest:
        def symbol_of_interest(self):
            def nested_a(a, b ): pass

    class NonSymbolOfInterest:
        def non_symbol_of_interest(self):
            def nested_b(a : int, b : str) -> bool: pass