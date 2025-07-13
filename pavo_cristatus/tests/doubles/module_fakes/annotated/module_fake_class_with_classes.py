from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithClasses"]

class ModuleFakeClassWithClasses(with_metaclass(ModuleFakeClass)):
    class SymbolOfInterest:
        def symbol_of_interest(self, a : int, b : str) -> bool: pass
    class NonSymbolOfInterest:
        def non_symbol_of_interest(self, a, b): pass

    class SymbolOfInterestClassMethod:
        @classmethod
        def class_method(cls, a: int, b : str) -> bool: pass
    
    class SymbolOfInterestStaticMethod:
        @staticmethod
        def static_method(a : int, b : str) -> bool: pass
