import collections
import sys
import os

import pytest
from six import with_metaclass

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.project_loader.utilities import is_non_annotated_symbol_of_interest
from pavo_cristatus.presenters import console_presenter
from pavo_cristatus.presenters.console_presenter import pavo_cristatus_print
from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import \
    ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import \
    ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import \
    ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import \
    ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import ModuleFakeClassWithCallables as AnnotatedModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses as AnnotatedModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import ModuleFakeClassWithInheritedAnnotatedCallables as AnnotatedModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import ModuleFakeClassWithClassesWithNestedAnnotatedCallables\
    as AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.interactions.annotated_symbol_presenter_interaction.annotated_symbol_presenter_interaction import interact
from pavo_cristatus.presenters.console_presenter import present_annotated_symbols
from pavo_cristatus.tests.doubles.verifiers.write_verifier import WriteVerifier
from pavo_cristatus.tests.utilities import get_nested_arg_specs, get_module_qualname, get_python_file_from_symbol_object
from pavo_cristatus.utilities import create_data_item_id


class ModuleFakeClassWithNestedAnnotatedFunction(with_metaclass(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass

    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a : int, b : str) -> bool: pass


class AnnotatedModuleFakeClassWithNestedAnnotatedFunction(with_metaclass(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass


    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a, b): pass

    symbol_of_interest.__qualname__ = ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest.__qualname__

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

write_verifier = WriteVerifier()

def print_hook(*args, **kwargs):
    return write_verifier(*args, **kwargs)

symbols_under_test = [(AnnotatedModuleFakeClassWithCallables.non_symbol_of_interest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithCallables.non_symbol_of_interest, None, None)),
                        ModuleFakeClassWithCallables.non_symbol_of_interest),
                     (AnnotatedModuleFakeClassWithClasses.NonSymbolOfInterest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithClasses.NonSymbolOfInterest, None, None)),
                        ModuleFakeClassWithClasses.NonSymbolOfInterest),
                     (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest, None, None)),
                        ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest),
                    (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest, None, None)),
                        ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest),
                    (AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest, None, None)),
                        ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest),
                    (AnnotatedModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest,
                        get_nested_arg_specs(NormalizedSymbol(ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest, None, None)),
                        ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest)]

@pytest.mark.parametrize("symbol,arg_specs,annotated_symbol", symbols_under_test)
def test_annotated_symbol_presenter_interaction(monkeypatch, symbol, arg_specs, annotated_symbol):
    monkeypatch.setattr(console_presenter, pavo_cristatus_print.__name__, print_hook)

    module_qualname = get_module_qualname(symbol, project_root_path)
    module_annotated_data_items = {
        create_data_item_id(module_qualname, symbol.__qualname__): arg_specs[symbol.__qualname__]}
    queue = collections.deque()
    normalized_symbol = NormalizedSymbol(symbol, None, None)
    symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                              normalized_symbol,
                                                              is_non_annotated_symbol_of_interest)
    queue.appendleft(symbol_object)
    while queue:
        current = queue.pop()
        for nested_symbol in current.nested_symbols:
            queue.appendleft(nested_symbol)
            data_item_id = create_data_item_id(module_qualname, nested_symbol.qualname)
            module_annotated_data_items[data_item_id] = arg_specs[nested_symbol.qualname]

    python_file = get_python_file_from_symbol_object(symbol_object)
    module = sys.modules[symbol_object.normalized_symbol.module]
    module_symbols = ModuleSymbols(module, python_file,
                                   module_qualname,
                                   {symbol_object})

    write_verifier.reset(module_symbols.get_annotated_source(module_annotated_data_items))

    result = interact({module_symbols : module_annotated_data_items}, present_annotated_symbols)
    assert result.status == PavoCristatusStatus.SUCCESS
    write_verifier.verify()