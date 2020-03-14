import collections
import inspect
import os

import pytest
from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.utilities import is_non_annotated_symbol_of_interest
from pavo_cristatus.testability.hook_point import HookPoint
from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable import \
    ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_class_with_nested_annotated_function import \
    ModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import \
    ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_method import \
    ModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable import ModuleFakeClassWithCallables as AnnotatedModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses as AnnotatedModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_method import ModuleFakeClassWithInheritedAnnotatedMethod as AnnotatedModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_class_with_nested_annotated_function import ModuleFakeClassWithClassWithNestedAnnotatedFunction as AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.interactions.annotated_symbol_presenter_interaction.annotated_symbol_presenter_interaction import interact
from pavo_cristatus.presenters.console_presenter import present_annotated_symbols
from pavo_cristatus.tests.doubles.verifiers.write_verifier import WriteVerifier
from pavo_cristatus.tests.utilities import get_nested_argspecs, get_module_qualname, get_python_file_from_symbol_object
from pavo_cristatus.utilities import create_data_item_id


class ModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass

    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a : int, b : str) -> bool: pass


class AnnotatedModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass


    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a, b): pass

    symbol_of_interest.__qualname__ = ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest.__qualname__

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

write_verifier = WriteVerifier()

def print_hook(*args, **kwargs):
    return write_verifier(*args, **kwargs)

@pytest.mark.parametrize("symbol,arg_specs,annotated_symbol",
                             [
                                 (AnnotatedModuleFakeClassWithCallables.non_symbol_of_interest,
                                    get_nested_argspecs(ModuleFakeClassWithCallables.non_symbol_of_interest),
                                    ModuleFakeClassWithCallables.non_symbol_of_interest),
                                 (AnnotatedModuleFakeClassWithClasses.NonSymbolOfInterest,
                                    get_nested_argspecs(ModuleFakeClassWithClasses.NonSymbolOfInterest),
                                    ModuleFakeClassWithClasses.NonSymbolOfInterest),
                                 (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest,
                                    get_nested_argspecs(ModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest),
                                    ModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest),
                                (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest,
                                    get_nested_argspecs(ModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest),
                                    ModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest),
                                (AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest,
                                    get_nested_argspecs(ModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest),
                                    ModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest),
                                (AnnotatedModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest,
                                    get_nested_argspecs(ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                                    ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest)
                             ])
def test_annotated_symbol_presenter_interaction(symbol, arg_specs, annotated_symbol):
    HookPoint.register(print.__name__, print_hook)

    module_qualname = get_module_qualname(symbol, project_root_path)
    module_annotated_data_items = {
        create_data_item_id(module_qualname, symbol.__qualname__): arg_specs[symbol.__qualname__]}
    queue = collections.deque()
    symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                              symbol,
                                                              is_non_annotated_symbol_of_interest)
    queue.appendleft(symbol_object)
    while queue:
        current = queue.pop()
        for nested_symbol in current.nested_symbols:
            queue.appendleft(nested_symbol)
            data_item_id = create_data_item_id(module_qualname, nested_symbol.qualname)
            module_annotated_data_items[data_item_id] = arg_specs[nested_symbol.qualname]

    python_file = get_python_file_from_symbol_object(symbol_object)
    module_symbols = ModuleSymbols(inspect.getmodule(symbol_object.symbol), python_file,
                                   get_module_qualname(symbol_object.symbol, project_root_path),
                                   {symbol_object})
    write_verifier.reset(module_symbols.get_annotated_source(module_annotated_data_items))

    result = interact({module_symbols : module_annotated_data_items}, present_annotated_symbols)
    assert result.status == PavoCristatusStatus.SUCCESS
    write_verifier.verify()