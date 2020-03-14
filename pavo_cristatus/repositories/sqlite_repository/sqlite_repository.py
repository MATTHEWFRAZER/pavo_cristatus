import logging
import os

from pavo_cristatus.repositories.data_item import DataItem

logger = logging.getLogger(__name__)

class SQLiteRepository(object):
    """
    repository for using sql backing db
    """

    def __init__(self, database_path, database_connection):
        self.database_connection = database_connection
        self.cursor = self.database_connection.cursor()
        # TODO: do this in SQL
        if not os.path.exists(database_path):
            self.cursor.execute("CREATE TABLE DATA_ITEMS (id TEXT PRIMARY KEY, data BLOB);")
            self.cursor.execute("CREATE [UNIQUE] INDEX id_index ON DATA_ITEMS(id);")

    def __del__(self):
        self.database_connection.close()

    def read_data_item(self, data_id):
        data_items = self.cursor.execute("SELECT (id, data) FROM DATA_ITEMS WHERE id = {0};".format(data_id))
        result = data_items.fetchone()
        if result:
            id, data = result
            return DataItem(id, data)
        return None

    def write_data_item(self, data_item):
        result = self.cursor.execute("INSERT OR REPLACE INTO DATA_ITEMS (id, data) VALUES ({0}, {1});".format(data_item.id, data_item.data))
        self.database_connection.commit()
        return result.rowcount > 0

    def delete_data_item(self, data_item):
        result = self.cursor.execute("DELETE FROM DATA_ITEMS WHERE id = {0};".format(data_item.id))
        self.database_connection.commit()
        return result.rowcount > 0