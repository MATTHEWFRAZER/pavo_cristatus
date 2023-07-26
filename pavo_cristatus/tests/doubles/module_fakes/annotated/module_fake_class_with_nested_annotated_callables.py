from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithNestedAnnotatedCallables"]

class ModuleFakeClassWithNestedAnnotatedCallables(with_metaclass(ModuleFakeClass)):
    def symbol_of_interest(self, a, b):
        def nested(a : int, b : str) -> bool: pass

    def non_symbol_of_interest(self, a, b): pass
