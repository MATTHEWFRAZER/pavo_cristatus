import inspect
import os
import pickle
import base64
from sys import version_info

import pytest

from pavo_cristatus.interactions.pavo_cristatus_status import PavoCristatusStatus
from pavo_cristatus.interactions.repository_interaction import sql_repository_write_interaction, sql_repository_read_interaction
from pavo_cristatus.module_symbols.module_symbols import ModuleSymbols
from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.project_loader.utilities import is_annotated_symbol_of_interest
from pavo_cristatus.repositories import SQLiteRepository
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_callables import \
    ModuleFakeClassWithCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes_with_nested_annotated_callables import \
    ModuleFakeClassWithClassesWithNestedAnnotatedCallables
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_classes import \
    ModuleFakeClassWithClasses
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_inherited_annotated_callables import \
    ModuleFakeClassWithInheritedAnnotatedCallables
from pavo_cristatus.tests.doubles.spies.sqlite_cursor_spy import SQLiteCursorSpy
from pavo_cristatus.tests.doubles.spies.sqlite_query_result_spy import SQLiteQueryResultSpy
from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_mixed_annotated_symbols import \
    ModuleFakeClassWithMixedAnnotatedSymbols
from pavo_cristatus.tests.module_symbols_tests.test_non_annotated_module_symbols import ModuleFakeClassWithNestedAnnotatedFunction
from pavo_cristatus.tests.utilities import get_module_qualname_from_source, get_python_file_from_symbol_object
from pavo_cristatus.utilities import create_data_item_id

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")

symbols_under_test = [ModuleFakeClassWithCallables.non_symbol_of_interest,
                      ModuleFakeClassWithClasses.NonSymbolOfInterest,
                      ModuleFakeClassWithInheritedAnnotatedCallables.SymbolOfInterest,
                      ModuleFakeClassWithInheritedAnnotatedCallables.NonSymbolOfInterest,
                      ModuleFakeClassWithClassesWithNestedAnnotatedCallables.NonSymbolOfInterest,
                      ModuleFakeClassWithClassesWithNestedAnnotatedCallables.SymbolOfInterest,
                      ModuleFakeClassWithNestedAnnotatedFunction.non_symbol_of_interest,
                      ModuleFakeClassWithMixedAnnotatedSymbols.symbol_of_interest]

# these are only supported by python 3.9 (all of the following symbols will cause syntax errors)
if version_info >= (3, 9):
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_classes import \
        ModuleFakeClassWithNestedLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_classes import \
        ModuleFakeClassWithLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_callables import \
        ModuleFakeClassWithMultiplyLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_multiply_lambda_decorated_classes import \
        ModuleFakeClassWithMultiplyLambdaDecoratedClasses
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_nested_lambda_decorated_callables import \
        ModuleFakeClassWithNestedLambdaDecoratedCallables
    from pavo_cristatus.tests.doubles.module_fakes.annotated.module_fake_class_with_lambda_decorated_callables import \
        ModuleFakeClassWithLambdaDecoratedCallables

    symbols_under_test.extend([ModuleFakeClassWithNestedLambdaDecoratedClasses.symbol_of_interest,
                               ModuleFakeClassWithLambdaDecoratedClasses.SymbolOfInterest,
                               ModuleFakeClassWithMultiplyLambdaDecoratedCallables.symbol_of_interest,
                               ModuleFakeClassWithMultiplyLambdaDecoratedClasses.SymbolOfInterest,
                               ModuleFakeClassWithNestedLambdaDecoratedCallables.symbol_of_interest,
                               ModuleFakeClassWithLambdaDecoratedCallables.symbol_of_interest])


class DummyPickled(object): pass

def symbols_object_generator(symbol_object):
    base64_data = base64.b64encode(pickle.dumps(DummyPickled()))
    data_item_data = str(base64_data, "utf-8")
    yield create_data_item_id(get_module_qualname_from_source(symbol_object.normalized_symbol.source, project_root_path), symbol_object.qualname), data_item_data
    for nested_symbol in symbol_object.nested_symbols:
        base64_data = base64.b64encode(pickle.dumps(DummyPickled()))
        data_item_data = str(base64_data, "utf-8")
        yield create_data_item_id(get_module_qualname_from_source(nested_symbol.normalized_symbol.source, project_root_path), symbol_object.qualname), data_item_data

class TestRepositoryInteraction:

    @pytest.mark.parametrize("symbol", symbols_under_test)
    def test_write_interaction(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, NormalizedSymbol(symbol, None, None),
                                                                  is_annotated_symbol_of_interest)

        python_file = get_python_file_from_symbol_object(symbol_object)

        module_symbols = ModuleSymbols(inspect.getmodule(symbol_object), python_file, symbol_object.module, {symbol_object})

        sqlite_query_result_spy = SQLiteQueryResultSpy(1, lambda: {module_symbols})
        sqlite_cursor_spy = SQLiteCursorSpy(sqlite_query_result_spy)
        sqlite_repository = SQLiteRepository(sqlite_cursor_spy)
        assert sql_repository_write_interaction(sqlite_repository).interact({module_symbols}).status == PavoCristatusStatus.SUCCESS
        assert sqlite_cursor_spy.execute_calls == len(symbol_object.nested_symbols) + 3

    @pytest.mark.parametrize("symbol", symbols_under_test)
    def test_read_interaction(self, symbol):
        symbol_object = symbol_collector.convert_to_symbol_object(project_root_path, NormalizedSymbol(symbol, None, None),
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
        sqlite_repository = SQLiteRepository(sqlite_cursor_spy)

        result = sql_repository_read_interaction(sqlite_repository).interact({module_symbols})
        assert result.status == PavoCristatusStatus.SUCCESS
        assert len(result.result) >= len(symbol_object.nested_symbols)
        assert sqlite_cursor_spy.execute_calls >= len(symbol_object.nested_symbols) + 2
