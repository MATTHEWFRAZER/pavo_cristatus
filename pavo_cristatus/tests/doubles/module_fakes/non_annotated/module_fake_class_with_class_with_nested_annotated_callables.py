from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithClassesWithNestedAnnotatedCallables"]

class ModuleFakeClassWithClassesWithNestedAnnotatedCallables(with_metaclass(ModuleFakeClass)):
    class SymbolOfInterest:
        def symbol_of_interest(self):
            def nested_a(a, b ): pass

    class NonSymbolOfInterest:
        def non_symbol_of_interest(self):
            def nested_b(a : int, b : str) -> bool: pass