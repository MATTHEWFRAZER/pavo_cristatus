class SQLiteCursorSpy(object):
    def __init__(self, query_result_spy):
        self.query_result_spy = query_result_spy
        self.execute_calls = 0

    def execute(self, x, *y):
        self.execute_calls += 1
        return self.query_result_spy

    def cursor(self):
        return self

    def commit(self):
        return

    def close(self):
        return