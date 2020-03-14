class SQLiteQueryResultSpy(object):
    def __init__(self, row_count, lazy_result):
        self.row_count = row_count
        self.number_of_elements = row_count
        self.lazy_result = lazy_result

    @property
    def rowcount(self):
        return self.row_count

    def fetchone(self):
        self.number_of_elements -= 1
        if self.number_of_elements < 0:
            return None
        return self.lazy_result()