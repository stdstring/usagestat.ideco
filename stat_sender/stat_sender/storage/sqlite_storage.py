from __future__ import unicode_literals
from _sqlite3 import connect
from storage import Storage

class SqliteStorage(Storage):

    # spec: str, Logger -> SqliteStorage
    def __init__(self, db_file, logger):
        self._db_file = db_file
        self._logger = logger

    # spec: None -> [(int, str, str, str, str)]
    def get_data(self):
        connection = connect(self._db_file)
        self._logger.info('get_data() enter')
        try:
            cursor = connection.cursor()
            query_str = 'select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID'
            cursor.execute(query_str)
            result = cursor.fetchall()
            self._logger.info('get_data() exit')
            return result
        except BaseException:
            self._logger.exception('exception in get_data()')
            raise
        finally:
            connection.close()

    # spec: (int, int) -> None
    def clear(self, id_clear_range):
        connection = connect(self._db_file)
        self._logger.info('clear({0!s}) enter'.format(id_clear_range))
        try:
            cursor = connection.cursor()
            query_str = 'delete from STAT_DATA where id between ? and ?'
            cursor.execute(query_str, id_clear_range)
            connection.commit()
            self._logger.info('clear({0!s}) exit'.format(id_clear_range))
        except BaseException:
            self._logger.exception('exception in clear({0!s})'.format(id_clear_range))
            raise
        finally:
            connection.close()

__author__ = 'andrey.ushakov'
