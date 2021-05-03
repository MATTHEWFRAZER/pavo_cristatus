import inspect
import os

import pytest

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.interactions.symbol_signature_replacer_interaction.symbol_signature_replacer_interaction import interact
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest, is_non_annotated_symbol_of_interest
from pavo_cristatus import utilities
from pavo_cristatus.utilities import pavo_cristatus_open
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import \
    ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import \
    ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import \
    ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import \
    ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.verifiers.write_verifier import WriteVerifier
from pavo_cristatus.tests.utilities import get_module_qualname, get_python_file_from_symbol_object

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

file_write_verifier = WriteVerifier()

def safe_open_hook(*args, **kwargs):
    return file_write_verifier

symbols_under_test = [ModuleFakeClassWithCallables.non_symbol_of_interest,
                      ModuleFakeClassWithClasses.NonSymbolOfInterest,
                      ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest,
                      ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest,
                      ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest,
                      ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest]

@pytest.mark.parametrize("symbol", symbols_under_test)
def test_symbol_signature_replacer_interaction(monkeypatch, symbol):
    monkeypatch.setattr(utilities, pavo_cristatus_open.__name__, safe_open_hook)

    symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol, is_annotated_symbol_of_interest)
    python_file = get_python_file_from_symbol_object(symbol_object)
    module_symbols = ModuleSymbols(inspect.getmodule(symbol_object.symbol), python_file,
                                   get_module_qualname(symbol_object.symbol, project_root_path),
                                   {symbol_object})
    project_symbols = {module_symbols}
    file_write_verifier.reset(module_symbols.get_non_annotated_source())

    # Due to file_write_verifier's structure, there can only be one ModuleSymbols per test
    result = interact(project_symbols)
    assert result.status == PavoCristatusStatus.SUCCESS and result.result
    file_write_verifier.verify()
