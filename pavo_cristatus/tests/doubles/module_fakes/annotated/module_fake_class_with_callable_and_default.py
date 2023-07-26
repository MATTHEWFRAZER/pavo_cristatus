from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass

from six import with_metaclass

__all__ = ["ModuleFakeClassWithCallableAndDefault"]

class ModuleFakeClassWithCallableAndDefault(with_metaclass(ModuleFakeClass)):
    def symbol_of_interest(self, a : int, b : str = 9) -> bool: pass