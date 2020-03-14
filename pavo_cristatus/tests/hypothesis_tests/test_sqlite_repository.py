from decorator import decorator
from hypothesis import given
from hypothesis.strategies import text, sets, builds, binary
from picidae import echo, to_bool, lazily_compose_given_functions, access_attribute, true, expand_parameter_list_by_x

from pavo_cristatus.repositories.data_item import DataItem
from pavo_cristatus.tests.doubles.verifiers.attribute_verifier import AttributeVerifier
from pavo_cristatus.tests.doubles.verifiers.sqlite_cursor_verifier import SQLiteCursorVerifier
from pavo_cristatus.utilities import is_symbol_callable

data_item = builds(DataItem, text(), binary()).filter(lazily_compose_given_functions(access_attribute("id"), to_bool))

def does_data_items_contain_unique_ids(data_items):
    return len({data_item.id for data_item in data_items}) == len(data_items)

given_data_items = given(sets(data_item).filter(does_data_items_contain_unique_ids))

@decorator
def decorate_all_test_methods(decorator_to_apply, cls):
    for key, value in cls.__dict__.items():
        if key.startswith("test_") and is_symbol_callable(value):
            setattr(cls, key, decorator_to_apply(value))
    return cls

@decorate_all_test_methods(given_data_items)
class TestSQLiteRepository:

    def test_write_data_item(self, data_items):
        attribute_verifier = AttributeVerifier(access_attribute("execute_calls"), 2 + len(data_items))
        verifier = SQLiteCursorVerifier(access_attribute("write_data_item"), echo, attribute_verifier)
        verifier.verify(data_items, len(data_items))

    def test_delete_data_item(self, data_items):
        attribute_verifier = AttributeVerifier(access_attribute("execute_calls"), 2 + len(data_items))
        verifier = SQLiteCursorVerifier(access_attribute("delete_data_item"), echo, attribute_verifier)
        verifier.verify(data_items, len(data_items))

    # TODO: read_all_data_items_needs to be tested differently
    #def test_read_all_data_items(self, data_items):
    #    attribute_verifier = AttributeVerifier(access_attribute("execute_calls"), 3)
    #    verifier = SQLiteCursorVerifier(access_attribute("read_all_data_items"), echo, attribute_verifier)
    #    verifier.verify(data_items, len(data_items))