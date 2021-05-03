import inspect
import os
import collections

import pytest

from trochilidae.interoperable_with_metaclass import interoperable_with_metaclass_future

from pavo_cristatus.project_loader import symbol_collector
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
from pavo_cristatus.tests.utilities import get_module_qualname, get_nested_argspecs
from pavo_cristatus.utilities import create_data_item_id, pavo_cristatus_get_source

unit_test_path = os.path.split(__file__)[0]
annotated_path = os.path.normpath(os.path.join(unit_test_path, "doubles", "module_fakes", "annotated"))
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

class ModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass

    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a : int, b : str) -> bool: pass

class ModuleFakeClassWithAnnotatedFunctionAndDefault(interoperable_with_metaclass_future(ModuleFakeClass)):
    def symbol_of_interest(self, a : int, b : str = 9) -> bool: pass

class ModuleFakeClassWithNonAnnotatedFunctionAndDefault(interoperable_with_metaclass_future(ModuleFakeClass)):
    def symbol_of_interest(self, a, b = 9): pass


class AnnotatedModuleFakeClassWithNestedAnnotatedFunction(interoperable_with_metaclass_future(ModuleFakeClass)):
    def non_symbol_of_interest(self, a : int, b : str) -> bool: pass


    def symbol_of_interest(self, a : int, b : str) -> bool:
        def nested(a, b): pass

    symbol_of_interest.__qualname__ = ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest.__qualname__


class TestNonAnnotatedModuleSymbols:
    @pytest.mark.parametrize("symbol,arg_specs,annotated_symbol",
                             [
                                 (AnnotatedModuleFakeClassWithCallables.non_symbol_of_interest,
                                  get_nested_argspecs(ModuleFakeClassWithCallables.non_symbol_of_interest),
                                  ModuleFakeClassWithCallables.non_symbol_of_interest),
                                 (AnnotatedModuleFakeClassWithClasses.NonSymbolOfInterest,
                                  get_nested_argspecs(ModuleFakeClassWithClasses.NonSymbolOfInterest),
                                  ModuleFakeClassWithClasses.NonSymbolOfInterest),
                                 (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest,
                                  get_nested_argspecs(ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest),
                                  ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest),
                                (AnnotatedModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest,
                                 get_nested_argspecs(ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest),
                                 ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest),
                                (AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest,
                                 get_nested_argspecs(ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest),
                                 ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest),
                                (AnnotatedModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest,
                                 get_nested_argspecs(ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                                 ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                                (ModuleFakeClassWithNonAnnotatedFunctionAndDefault.symbol_of_interest,
                                 {ModuleFakeClassWithNonAnnotatedFunctionAndDefault.symbol_of_interest.__qualname__ : inspect.getfullargspec(ModuleFakeClassWithAnnotatedFunctionAndDefault.symbol_of_interest)},
                                 ModuleFakeClassWithAnnotatedFunctionAndDefault.symbol_of_interest)
                             ])
    def test_symbol_object_gives_correct_source_for_annotated_symbol(self, symbol, arg_specs, annotated_symbol):
        module_qualname = get_module_qualname(symbol, project_root_path)
        module_annotated_data_items = {create_data_item_id(module_qualname, symbol.__qualname__): arg_specs[symbol.__qualname__]}
        queue = collections.deque()
        annotated_symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                                            symbol,
                                                                            is_non_annotated_symbol_of_interest)
        queue.appendleft(annotated_symbol_object)
        while queue:
            current = queue.pop()
            for nested_symbol in current.nested_symbols:
                queue.appendleft(nested_symbol)
                data_item_id = create_data_item_id(module_qualname, nested_symbol.qualname)
                module_annotated_data_items[data_item_id] = arg_specs[nested_symbol.qualname]

        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol, is_non_annotated_symbol_of_interest)
        symbol_object.module = module_qualname
        symbol_object.qualname = symbol.__qualname__
        annotated_source = symbol_object.get_annotated_source(module_annotated_data_items)
        assert annotated_source == pavo_cristatus_get_source(annotated_symbol)

    @pytest.mark.parametrize("symbols", [(ModuleFakeClassWithCallables.symbol_of_interest, AnnotatedModuleFakeClassWithCallables.symbol_of_interest),
                                         (ModuleFakeClassWithClasses.SymbolOfInterest, AnnotatedModuleFakeClassWithClasses.SymbolOfInterest),
                                         (ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest, AnnotatedModuleFakeClassWithClassWithNestedAnnotatedFunction.SymbolOfInterest),
                                         (AnnotatedModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest, ModuleFakeClassWithNestedAnnotatedFunction.symbol_of_interest),
                                         (ModuleFakeClassWithNonAnnotatedFunctionAndDefault.symbol_of_interest, ModuleFakeClassWithAnnotatedFunctionAndDefault.symbol_of_interest)])
    def test_symbol_object_gives_correct_source_for_non_annotated_symbol(self, symbols):
        non_annotated_symbol, annotated_symbol = symbols
        module_qualname = get_module_qualname(non_annotated_symbol, project_root_path)
        module_annotated_data_items = {create_data_item_id(module_qualname, non_annotated_symbol.__qualname__): inspect.getfullargspec(annotated_symbol)}

        queue = collections.deque()
        queue.appendleft(annotated_symbol)
        while queue:
            current = queue.pop()
            for nested_symbol in symbol_collector.convert_to_symbol_object(project_root_path,
                                                                           current,
                                                                           is_annotated_symbol_of_interest).nested_symbols:
                queue.appendleft(nested_symbol.symbol)
                module_annotated_data_items[create_data_item_id(module_qualname, nested_symbol.qualname)] = inspect.getfullargspec(nested_symbol.symbol)


        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, non_annotated_symbol, is_non_annotated_symbol_of_interest)
        annotated_source = symbol_object.get_annotated_source(module_annotated_data_items)
        expected_source_lines = pavo_cristatus_get_source(annotated_symbol).split("\n")
        annotated_source_lines  = annotated_source.split("\n")
        assert len(annotated_source_lines) == len(expected_source_lines)
        assert self.get_count_of_mismatched_lines(expected_source_lines, annotated_source_lines) == 0

    @staticmethod
    def get_count_of_mismatched_lines(expected_source_lines, non_annotated_source_lines):
        count = 0
        for i in range(len(expected_source_lines)):
            if expected_source_lines[i] != non_annotated_source_lines[i]:
                count += 1
        return count