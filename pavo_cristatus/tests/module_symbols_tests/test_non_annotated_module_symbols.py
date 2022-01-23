import inspect
import os
import collections
import sys

import pytest

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.project_loader.utilities import is_non_annotated_symbol_of_interest, is_annotated_symbol_of_interest
from pavo_cristatus.tests.doubles.module_fakes.module_fake_class import ModuleFakeClass
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_callables import ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_class_with_inherited_annotated_callables import ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_class_with_nested_annotated_callables import ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import ModuleFakeClassWithCallables as AnnotatedModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses as AnnotatedModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import ModuleFakeClassWithInheritedAnnotatedCallables as AnnotatedModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import ModuleFakeClassWithClassesWithNestedAnnotatedCallables as AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable_and_default import ModuleFakeClassWithCallableAndDefault \
    as AnnotatedModuleFakeClassWithCallableAndDefault
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_callable_and_default import ModuleFakeClassWithCallableAndDefault
from pavo_cristatus.tests.doubles.special_argument_callables_annotated import all_callables as all_callables_annotated
from pavo_cristatus.tests.doubles.special_argument_callables_non_annotated import all_callables as all_callables_non_annotated

from pavo_cristatus.tests.utilities import get_module_qualname, get_nested_arg_specs
from pavo_cristatus.utilities import create_data_item_id, pavo_cristatus_get_source, pavo_cristatus_split

unit_test_path = os.path.split(__file__)[0]
annotated_path = os.path.normpath(os.path.join(unit_test_path, "doubles", "module_fakes", "annotated"))
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

def normalize_symbol_with_name_as_qualname(symbol):
    normalized_symbol = NormalizedSymbol(symbol, None, None)
    normalized_symbol._qualname = normalized_symbol._name
    return normalized_symbol

symbols_under_test_1 = [
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
                         ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                        (ModuleFakeClassWithCallableAndDefault.symbol_of_interest,
                         {ModuleFakeClassWithCallableAndDefault.symbol_of_interest.__qualname__ : inspect.getfullargspec(AnnotatedModuleFakeClassWithCallableAndDefault.symbol_of_interest)},
                         AnnotatedModuleFakeClassWithCallableAndDefault.symbol_of_interest)
                        ]

symbols_under_test_2 = [(ModuleFakeClassWithCallables.symbol_of_interest, AnnotatedModuleFakeClassWithCallables.symbol_of_interest),
                         (ModuleFakeClassWithClasses.SymbolOfInterest, AnnotatedModuleFakeClassWithClasses.SymbolOfInterest),
                         (ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest, AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction.SymbolOfInterest),
                         (AnnotatedModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest, ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                         (ModuleFakeClassWithCallableAndDefault.symbol_of_interest, ModuleFakeClassWithCallableAndDefault.symbol_of_interest)
                         ]

# these are only supported by python 3.9 (all of the following symbols will cause syntax errors)
if sys.version_info >= (3, 9):
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_multiply_lambda_decorated_classes import \
        ModuleFakeClassWithMultiplyLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_classes import \
        ModuleFakeClassWithMultiplyLambdaDecoratedClasses as AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables as AnnotatedModuleFakeClassWithLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_lambda_decorated_classes import \
        ModuleFakeClassWithLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_classes import \
        ModuleFakeClassWithLambdaDecoratedClasses as AnnotatedModuleFakeClassWithLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables as AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables as AnnotatedModuleFakeClassWithNestedLambdaDecoratedCallables

    symbols_under_test_1.extend([(AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest,
                                get_nested_arg_specs(normalize_symbol_with_name_as_qualname(AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest)),
                                AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest),
                                 (ModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest,
                                  get_nested_arg_specs(normalize_symbol_with_name_as_qualname(AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest)),
                                  AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest),
                                 (ModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest,
                                  get_nested_arg_specs(normalize_symbol_with_name_as_qualname(
                                      AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest)),
                                  AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest),
                                 (ModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest,
                                  get_nested_arg_specs(normalize_symbol_with_name_as_qualname(
                                      AnnotatedModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest)),
                                  AnnotatedModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest),
                                 (ModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest,
                                  get_nested_arg_specs(normalize_symbol_with_name_as_qualname(
                                      AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest)),
                                  AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest),
                                 (ModuleFakeClassWithNestedLambdaDecoratedCallables.symbol_of_interest,
                                  get_nested_arg_specs(NormalizedSymbol(
                                      AnnotatedModuleFakeClassWithNestedLambdaDecoratedCallables.symbol_of_interest,
                                      None, None)),
                                  AnnotatedModuleFakeClassWithNestedLambdaDecoratedCallables.symbol_of_interest
                                  )
                                 ])

    symbols_under_test_2.extend([(ModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest, AnnotatedModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest),
                                 (ModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest, AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest),
                                 (ModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest,
                                  AnnotatedModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest),
                                 (ModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest,
                                  AnnotatedModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest)])

class TestNonAnnotatedModuleSymbols:
    @pytest.mark.parametrize("symbol,arg_specs,annotated_symbol", symbols_under_test_1)
    def test_symbol_object_gives_correct_source_for_annotated_symbol(self, symbol, arg_specs, annotated_symbol):
        normalized_symbol = NormalizedSymbol(symbol, None, None)
        module_qualname = get_module_qualname(symbol, project_root_path)

        module_annotated_data_items = {create_data_item_id(module_qualname, normalized_symbol.qualname): arg_specs[normalized_symbol.qualname]}

        queue = collections.deque()
        annotated_symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                                            NormalizedSymbol(symbol, None, None),
                                                                            is_non_annotated_symbol_of_interest)
        queue.appendleft(annotated_symbol_object)
        while queue:
            current = queue.pop()
            for nested_symbol in current.nested_symbols:
                queue.appendleft(nested_symbol)
                data_item_id = create_data_item_id(module_qualname, nested_symbol.qualname)
                module_annotated_data_items[data_item_id] = arg_specs[nested_symbol.qualname]

        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, NormalizedSymbol(symbol, None, None), is_non_annotated_symbol_of_interest)
        symbol_object.module = module_qualname
        symbol_object.qualname = normalized_symbol.qualname

        annotated_source = symbol_object.get_annotated_source(module_annotated_data_items)

        assert annotated_source == pavo_cristatus_get_source(annotated_symbol)

    @pytest.mark.parametrize("symbols", symbols_under_test_2)
    def test_symbol_object_gives_correct_source_for_non_annotated_symbol(self, symbols):
        non_annotated_symbol, annotated_symbol = symbols
        self.verify_symbol_gives_correct_source_for_non_annotated_symbol(non_annotated_symbol, annotated_symbol)

    @pytest.mark.parametrize("non_annotated_symbol,annotated_symbol", zip(all_callables_non_annotated, all_callables_annotated))
    def test_symbol_object_gives_correct_source_for_non_annotated_symbol_for_special_callables(self, non_annotated_symbol, annotated_symbol):
        self.verify_symbol_gives_correct_source_for_non_annotated_symbol(non_annotated_symbol, annotated_symbol)

    def verify_symbol_gives_correct_source_for_non_annotated_symbol(self, non_annotated_symbol, annotated_symbol):
        non_annotated_normalized_symbol = NormalizedSymbol(non_annotated_symbol, None, None)
        annotated_normalized_symbol = NormalizedSymbol(annotated_symbol, None, None)
        module_qualname = get_module_qualname(non_annotated_symbol, project_root_path)
        module_annotated_data_items = {
            create_data_item_id(module_qualname, non_annotated_normalized_symbol.qualname): inspect.getfullargspec(
                annotated_normalized_symbol.symbol)}

        queue = collections.deque()
        queue.appendleft(annotated_normalized_symbol)
        while queue:
            current = queue.pop()
            for nested_symbol in symbol_collector.convert_to_symbol_object(project_root_path,
                                                                           current,
                                                                           is_annotated_symbol_of_interest).nested_symbols:
                queue.appendleft(nested_symbol.normalized_symbol)
                module_annotated_data_items[
                    create_data_item_id(module_qualname, nested_symbol.qualname)] = inspect.getfullargspec(
                    nested_symbol.normalized_symbol.symbol)

        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, non_annotated_normalized_symbol,
                                                                  is_non_annotated_symbol_of_interest)
        annotated_source = symbol_object.get_annotated_source(module_annotated_data_items)
        expected_source_lines = pavo_cristatus_split(pavo_cristatus_get_source(annotated_symbol))
        annotated_source_lines = pavo_cristatus_split(annotated_source)

        assert len(annotated_source_lines) == len(expected_source_lines)
        assert self.get_count_of_mismatched_lines(expected_source_lines, annotated_source_lines) == 0

    @staticmethod
    def get_count_of_mismatched_lines(expected_source_lines, non_annotated_source_lines):
        count = 0
        for i in range(len(expected_source_lines)):
            if expected_source_lines[i] != non_annotated_source_lines[i]:
                count += 1
        return count