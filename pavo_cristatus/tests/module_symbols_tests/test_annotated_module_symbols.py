import os
import sys

import pytest

from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_mixed_annotated_symbols import \
    ModuleFakeClassWithMixedAnnotatedSymbols
from pavo_cristatus.tests.doubles.module_fakes.non_annotated.module_fake_class_with_callable_and_default import ModuleFakeClassWithCallableAndDefault
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable_and_default import ModuleFakeClassWithCallableAndDefault\
    as AnnotatedModuleFakeClassWithCallableAndDefault

from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_annotated_callables import ModuleFakeClassWithNestedAnnotatedCallables
from pavo_cristatus.utilities import pavo_cristatus_get_source, pavo_cristatus_split

unit_test_path = os.path.split(__file__)[0]
annotated_path = os.path.normpath(os.path.join(unit_test_path, "doubles", "module_fakes", "annotated"))
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

symbols_under_test_1 = [ModuleFakeClassWithCallables.non_symbol_of_interest,
                        ModuleFakeClassWithClasses.NonSymbolOfInterest,
                        ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest,
                        ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest,
                        ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest,
                        ModuleFakeClassWithNestedAnnotatedCallables.non_symbol_of_interest,
                        ModuleFakeClassWithMixedAnnotatedSymbols.non_symbol_of_interest,
                        ModuleFakeClassWithCallableAndDefault.symbol_of_interest
                        ]

symbols_under_test_2 = [ModuleFakeClassWithCallables.symbol_of_interest,
                        ModuleFakeClassWithClasses.SymbolOfInterest,
                        ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest,
                        ModuleFakeClassWithNestedAnnotatedCallables.symbol_of_interest,
                        AnnotatedModuleFakeClassWithCallableAndDefault.symbol_of_interest
                        ]

# these are only supported by python 3.9 (all of the following symbols will cause syntax errors)
if sys.version_info >= (3, 9):
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_classes import \
        ModuleFakeClassWithLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_classes import \
        ModuleFakeClassWithMultiplyLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_classes import \
        ModuleFakeClassWithNestedLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables

    symbols_under_test_1.extend([ModuleFakeClassWithLambdaDecoratedCallables.non_symbol_of_interest,
                                ModuleFakeClassWithLambdaDecoratedClasses.NonSymbolOfInterest,
                                ModuleFakeClassWithMultiplyLambdaDecoratedCallables.non_symbol_of_interest,
                                ModuleFakeClassWithMultiplyLambdaDecoratedClasses.NonSymbolOfInterest,
                                ModuleFakeClassWithNestedLambdaDecoratedCallables.non_symbol_of_interest,
                                ModuleFakeClassWithNestedLambdaDecoratedClasses.non_symbol_of_interest])

    symbols_under_test_2.extend([ModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest,
                                ModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest,
                                ModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest,
                                ModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest,
                                ModuleFakeClassWithNestedLambdaDecoratedCallables.symbol_of_interest,
                                ModuleFakeClassWithNestedLambdaDecoratedClasses.symbol_of_interest])

class TestAnnotatedModuleSymbols:
    @pytest.mark.parametrize("symbol", symbols_under_test_1)
    def test_symbol_object_gives_correct_source_for_non_annotated_symbol(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, NormalizedSymbol(symbol, None, None), is_annotated_symbol_of_interest)
        non_annotated_source = symbol_object.get_non_annotated_source()
        assert non_annotated_source == pavo_cristatus_get_source(symbol)

    @pytest.mark.parametrize("symbol", symbols_under_test_2)
    def test_symbol_object_gives_correct_source_annotated_symbol(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, NormalizedSymbol(symbol, None, None), is_annotated_symbol_of_interest)
        non_annotated_source = symbol_object.get_non_annotated_source()
        annotated_source_lines = pavo_cristatus_split(pavo_cristatus_get_source(symbol))
        non_annotated_source_lines  = pavo_cristatus_split(non_annotated_source)
        assert len(non_annotated_source_lines) == len(annotated_source_lines)
        assert self.get_count_of_mismatched_lines(annotated_source_lines, non_annotated_source_lines) == 1

    @pytest.mark.parametrize("symbol", [ModuleFakeClassWithMixedAnnotatedSymbols.symbol_of_interest])
    def test_symbol_object_gives_correct_source_mixed_annotated_symbol(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                                  NormalizedSymbol(symbol, None, None),
                                                                  is_annotated_symbol_of_interest)
        non_annotated_source = symbol_object.get_non_annotated_source()
        annotated_source_lines = pavo_cristatus_split(pavo_cristatus_get_source(symbol))
        non_annotated_source_lines = pavo_cristatus_split(non_annotated_source)
        assert len(non_annotated_source_lines) == len(annotated_source_lines)
        assert self.get_count_of_mismatched_lines(annotated_source_lines, non_annotated_source_lines) == 2

    @staticmethod
    def get_count_of_mismatched_lines(expected_source_lines, non_annotated_source_lines):
        count = 0
        for i in range(len(expected_source_lines)):
            if expected_source_lines[i] != non_annotated_source_lines[i]:
                count += 1
        return count
