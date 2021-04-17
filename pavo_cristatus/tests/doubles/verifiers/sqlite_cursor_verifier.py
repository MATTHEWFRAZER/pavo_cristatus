from picidae import true

from pavo_cristatus.repositories import SQLiteRepository
from pavo_cristatus.tests.doubles.spies.sqlite_cursor_spy import SQLiteCursorSpy
from pavo_cristatus.tests.doubles.spies.sqlite_query_result_spy import SQLiteQueryResultSpy


class SQLiteCursorVerifier(object):
    def __init__(self, operation_accessor, post_operation_accessor, attribute_verifier):
        self.operation_accessor = operation_accessor
        self.attribute_verifier = attribute_verifier
        self.post_operation_accessor = post_operation_accessor

    def verify(self, data_items, expected_value):
        sqlite_query_result_spy = SQLiteQueryResultSpy(expected_value, true)
        sqlite_cursor_spy = SQLiteCursorSpy(sqlite_query_result_spy)
        sqlite_repository = SQLiteRepository(sqlite_cursor_spy)
        for data in data_items:
            result = self.operation_accessor(sqlite_repository)(data)
            assert self.post_operation_accessor(result)


        # TODO: assert sqlite_query_result_spy.number_of_elements == -1
        self.attribute_verifier.verify(sqlite_cursor_spy)