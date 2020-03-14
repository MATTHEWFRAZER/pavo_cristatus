import inspect
import os
import pickle

import pytest

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.interactions.repository_interaction import sql_repository_write_interaction, sql_repository_read_interaction
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest
from pavo_cristatus.repositories import SQLiteRepository
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callable import \
    ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_class_with_nested_annotated_function import \
    ModuleFakeClassWithClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import \
    ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_method import \
    ModuleFakeClassWithInheritedAnnotatedMethod
from pavo_cristatus.tests.doubles.spies.sqlite_cursor_spy import SQLiteCursorSpy
from pavo_cristatus.tests.doubles.spies.sqlite_query_result_spy import SQLiteQueryResultSpy
from pavo_cristatus.tests.module_symbols_tests.test_non_annotated_module_symbols import \
    ModuleFakeClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.utilities import get_module_qualname, get_python_file_from_symbol_object
from pavo_cristatus.utilities import get_data_item_id

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

symbols_under_test = [#ModuleFakeClassWithCallables.non_symbol_of_interest,
                      #ModuleFakeClassWithClasses.NonSymbolOfInterest,
                      #ModuleFakeClassWithInheritedAnnotatedMethod.SymbolOfInterest,
                      #ModuleFakeClassWithInheritedAnnotatedMethod.NonSymbolOfInterest,
                      #ModuleFakeClassWithClassWithNestedAnnotatedFunction.NonSymbolOfInterest,
                      ModuleFakeClassWithClassWithNestedAnnotatedFunction.SymbolOfInterest,]
                      #ModuleFakeClassWithNestedAnnotatedFunction.non_symbol_of_interest]

class DummyPickled(object): pass

def symbols_object_generator(symbol_object):
    yield get_data_item_id(get_module_qualname(symbol_object.symbol, project_root_path), symbol_object.qualname), pickle.dumps(DummyPickled())
    for nested_symbol in symbol_object.nested_symbols:
        yield get_data_item_id(get_module_qualname(nested_symbol.symbol, project_root_path), symbol_object.qualname), pickle.dumps(DummyPickled())

class TestRepositoryInteraction:

    @pytest.mark.parametrize("symbol", symbols_under_test)
    def test_write_interaction(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol,
                                                                  is_annotated_symbol_of_interest)

        python_file = get_python_file_from_symbol_object(symbol_object)

        module_symbols = ModuleSymbols(inspect.getmodule(symbol_object), python_file, symbol_object.module, {symbol_object})

        sqlite_query_result_spy = SQLiteQueryResultSpy(1, lambda: {module_symbols})
        sqlite_cursor_spy = SQLiteCursorSpy(sqlite_query_result_spy)
        sqlite_repository = SQLiteRepository(str(), sqlite_cursor_spy)
        assert sql_repository_write_interaction(sqlite_repository).interact({module_symbols}).status == PavoCristatusStatus.SUCCESS
        assert sqlite_cursor_spy.execute_calls == len(symbol_object.nested_symbols) + 3

    @pytest.mark.parametrize("symbol", symbols_under_test)
    def test_read_interaction(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, symbol,
                                                                  is_annotated_symbol_of_interest)
        gen = symbols_object_generator(symbol_object)

        def lazy_result():
            try:
                return next(gen)
            except StopIteration:
                return None

        python_file = get_python_file_from_symbol_object(symbol_object)
        module_symbols = ModuleSymbols(inspect.getmodule(symbol_object), python_file, symbol_object.module,
                                       {symbol_object})

        sqlite_query_result_spy = SQLiteQueryResultSpy(len(symbol_object.nested_symbols) + 1, lazy_result)
        sqlite_cursor_spy = SQLiteCursorSpy(sqlite_query_result_spy)
        sqlite_repository = SQLiteRepository(str(), sqlite_cursor_spy)

        result = sql_repository_read_interaction(sqlite_repository).interact({module_symbols})
        assert result.status == PavoCristatusStatus.SUCCESS
        assert len(result.result) >= len(symbol_object.nested_symbols)
        assert sqlite_cursor_spy.execute_calls >= len(symbol_object.nested_symbols) + 2
