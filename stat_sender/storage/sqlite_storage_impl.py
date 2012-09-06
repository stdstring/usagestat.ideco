from __future__ import unicode_literals
from _sqlite3 import connect
from storage.storage import Storage

class SqliteStorageImpl(Storage):

    def __init__(self, db_filename):
        self._db_filename = db_filename

    # spec: None -> [(int, str, datetime, str)]
    def get_data(self):
        connection = connect(self._db_filename)
        try:
            cursor = connection.cursor()
            query_str = 'select ID, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID'
            cursor.execute(query_str)
            return cursor.fetchall()
        finally:
            connection.close()

    # spec: (int, int) -> None
    def clear(self, id_clear_range):
        connection = connect(self._db_filename)
        try:
            cursor = connection.cursor()
            query_str = 'delete from STAT_DATA where id between ? and ?'
            cursor.execute(query_str, id_clear_range)
            connection.commit()
        finally:
            connection.close()

    _db_filename = None

__author__ = 'andrey.ushakov'
