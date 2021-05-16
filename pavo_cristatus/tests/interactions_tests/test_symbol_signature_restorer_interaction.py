import collections
import inspect
import os
import sys

import pytest
from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.interactions.symbol_signature_restorer_interaction.symbol_signature_restorer_interaction import interact
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.project_loader.utilities import is_non_annotated_symbol_of_interest
from pavo_cristatus import utilities
from pavo_cristatus.utilities import pavo_cristatus_open
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
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import ModuleFakeClassWithClassesWithNestedAnnotatedCallables as AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.doubles.verifiers.write_verifier import WriteVerifier
from pavo_cristatus.tests.utilities import get_module_qualname_from_source, get_python_file_from_symbol_object, get_nested_arg_specs
from pavo_cristatus.utilities import create_data_item_id

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

class ModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass

    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a : int, b : str) -> bool: pass


class AnnotatedModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass


    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a, b): pass

    symbol_of_interest.__qualname__ = ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest.__qualname__

write_verifier = WriteVerifier()

def safe_open_hook(*args, **kwargs):
    return write_verifier

symbols_under_test = [
                         (AnnotatedModuleFakeClassWithCallables.non_symbol_of_interest,
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
                         ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest)
                    ]

# these are only supported by python 3.9 (all of the following symbols will cause syntax errors)
if sys.version_info >= (3, 9):
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables as AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables as AnnotatedModuleFakeClassWithNestedLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables as AnnotatedModuleFakeClassWithLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables

    symbols_under_test.extend([
                                (AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables.non_symbol_of_interest,
                                 get_nested_arg_specs(NormalizedSymbol(
                                     ModuleFakeClassWithMultiplyLambdaDecoratedCallables.non_symbol_of_interest, None,
                                     None)),
                                 ModuleFakeClassWithMultiplyLambdaDecoratedCallables.non_symbol_of_interest),
                                (AnnotatedModuleFakeClassWithNestedLambdaDecoratedCallables.non_symbol_of_interest,
                                 get_nested_arg_specs(NormalizedSymbol(
                                     ModuleFakeClassWithNestedLambdaDecoratedCallables.non_symbol_of_interest, None,
                                     None)),
                                 ModuleFakeClassWithNestedLambdaDecoratedCallables.non_symbol_of_interest
                                 ),
                                (AnnotatedModuleFakeClassWithLambdaDecoratedCallables.non_symbol_of_interest,
                                 get_nested_arg_specs(NormalizedSymbol(
                                     ModuleFakeClassWithLambdaDecoratedCallables.non_symbol_of_interest, None,
                                     None)),
                                 ModuleFakeClassWithLambdaDecoratedCallables.non_symbol_of_interest
                                 )
                               ])

@pytest.mark.parametrize("symbol,arg_specs,annotated_symbol", symbols_under_test)
def test_symbol_signature_restorer_interaction(monkeypatch, symbol, arg_specs, annotated_symbol):
    monkeypatch.setattr(utilities, pavo_cristatus_open.__name__, safe_open_hook)

    normalized_symbol = NormalizedSymbol(symbol, None, None)

    module_qualname = get_module_qualname_from_source(normalized_symbol.source, project_root_path)

    module_annotated_data_items = {create_data_item_id(module_qualname, normalized_symbol.qualname): arg_specs[normalized_symbol.qualname]}

    queue = collections.deque()
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
    module_symbols = ModuleSymbols(inspect.getmodule(symbol_object.normalized_symbol), python_file,
                                                     symbol_object.normalized_symbol.qualname,
                                                     {symbol_object})
    write_verifier.reset(module_symbols.get_annotated_source(module_annotated_data_items))

    # Due to file_write_verifier's structure, there can only be one ModuleSymbols per test
    result = interact({module_symbols : module_annotated_data_items})
    assert result.status == PavoCristatusStatus.SUCCESS and result.result
    write_verifier.verify()