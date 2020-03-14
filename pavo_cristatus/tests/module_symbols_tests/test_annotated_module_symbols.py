import inspect
import os

import pytest

from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable import ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_method import ModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_class_with_nested_annotated_function import ModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_annotated_function import ModuleFakeClassWithNestedAnnotatedFunction

unit_test_path = os.path.split(__file__)[0]
annotated_path = os.path.normpath(os.path.join(unit_test_path, "doubles", "module_fakes", "annotated"))
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

class TestAnnotatedModuleSymbols:
    @pytest.mark.parametrize("symbol", [ModuleFakeClassWithCallables.non_symbol_of_interest,
                                        ModuleFakeClassWithClasses.NonSymbolOfInterest,
                                        ModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest,
                                        ModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest,
                                        ModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest,
                                        ModuleFakeClassWithNestedAnnotatedFunction.non_symbol_of_interest])
    def test_symbol_object_gives_correct_source_for_non_annotated_symbol(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol, is_annotated_symbol_of_interest)
        non_annotated_source = symbol_object.get_non_annotated_source()
        assert non_annotated_source == inspect.getsource(symbol)

    @pytest.mark.parametrize("symbol", [ModuleFakeClassWithCallables.symbol_of_interest,
                                        ModuleFakeClassWithClasses.SymbolOfInterest,
                                        ModuleFakeClassWithClassWithNestedAnnotatedFunction.SymbolOfInterest,
                                        ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest])
    def test_symbol_object_gives_correct_source_annotated_symbol(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol, is_annotated_symbol_of_interest)
        non_annotated_source = symbol_object.get_non_annotated_source()
        expected_source_lines = inspect.getsource(symbol).split("\n")
        non_annotated_source_lines  = non_annotated_source.split("\n")
        assert len(non_annotated_source_lines) == len(expected_source_lines)
        assert self.get_count_of_mismatched_lines(expected_source_lines, non_annotated_source_lines) == 1

    @staticmethod
    def get_count_of_mismatched_lines(expected_source_lines, non_annotated_source_lines):
        count = 0
        for i in range(len(expected_source_lines)):
            if expected_source_lines[i] != non_annotated_source_lines[i]:
                count += 1
        return count
