import inspect
import os
import sys

import pytest

from pavo_cristatus.project_loader import symbol_collector
from pavo_cristatus.project_loader.normalized_symbol import NormalizedSymbol
from pavo_cristatus.project_loader.utilities import is_non_annotated_symbol_of_interest

unit_test_path = os.path.split(__file__)[0]
project_root_path = os.path.normpath(os.path.join(unit_test_path, "..", "..")).replace("\\", "\\\\")


def callable_to_normalize(): pass


class ClassToNormalize: pass

class ClassToNormalize2:
    def x(self): pass

def callable_to_normalize_with_nested_callable():
    def nested_callable(): pass

def callable_to_normalize_with_conflicting_nested_callables():
    def nested_callable(x, y, z): pass
    def nested_callable(): pass

symbols_under_test = [callable_to_normalize, ClassToNormalize]

# these are only supported by python 3.9 (all of the following symbols will cause syntax errors)
if sys.version_info >= (3, 9):
    from pavo_cristatus.tests.project_loader_tests.lambda_decorated_symbols import lambda_decorated_callable_to_normalize, LambdaDecoratedClassToNormalize

    symbols_under_test.extend([lambda_decorated_callable_to_normalize, LambdaDecoratedClassToNormalize])


@pytest.mark.parametrize("symbol", symbols_under_test)
def test_normalized_symbol_works_with_no_parent_symbol(symbol):
    source = inspect.getsource(symbol)
    normalized_symbol = NormalizedSymbol(symbol, None, None)
    assert normalized_symbol.source == source
    assert normalized_symbol.original_symbol == symbol

@pytest.mark.parametrize("symbol,parent_symbol", [(ClassToNormalize2.x, ClassToNormalize2)])
def test_normalize_symbol_works_with_parent_symbol(symbol,parent_symbol):
    source = inspect.getsource(symbol)
    normalized_parent = NormalizedSymbol(parent_symbol, None, None)
    normalized_symbol = NormalizedSymbol(symbol, normalized_parent, symbol.__name__)
    assert normalized_symbol.normalized_source.rstrip() == source.strip()
    assert normalized_symbol.original_symbol == symbol


# normalized symbol can normalize this case:
# need to handle the case where we overwrite symbols in namespace
# example:
# def x():
#       class a: pass
#       def a(): pass
# we should resolve function a
@pytest.mark.parametrize("parent_symbol,nested_source",[(callable_to_normalize_with_nested_callable, "def nested_callable(): pass\n"),
                                                        (callable_to_normalize_with_conflicting_nested_callables, "def nested_callable(): pass\n")])
def test_normalized_symbol_works_with_nested_symbols(parent_symbol, nested_source):
    normalized_parent = NormalizedSymbol(parent_symbol, None, None)

    parent_symbol_object = symbol_collector.convert_to_symbol_object(project_root_path,
                                                                     normalized_parent,
                                                                     is_non_annotated_symbol_of_interest)

    nested_symbol_object = next(iter(parent_symbol_object.nested_symbols), None)
    assert nested_symbol_object is not None
    assert nested_symbol_object.normalized_symbol.normalized_source == nested_source

def test_normalized_symbol_raises_exception_if_normalized_parent_is_provided_without_normalized_child_name():
    try:
        NormalizedSymbol(ClassToNormalize2.x, ClassToNormalize2, None)
    except ValueError:
        pass
    else:
        pytest.fail("Value Error was expected")

# TODO: single line symbol raises error


