from __future__ import unicode_literals
from _sqlite3 import connect
import logging
from storage import Storage

class SqliteStorageImpl(Storage):

    def __init__(self, db_file, logger = logging.getLogger('stat_sender.sqlite_storage_impl')):
        self._db_file = db_file
        self._logger = logger

    # spec: None -> [(int, str, str, str, str)]
    def get_data(self):
        connection = connect(self._db_file)
        self._logger.info('SqliteStorageImpl.get_data() enter')
        try:
            cursor = connection.cursor()
            query_str = 'select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID'
            cursor.execute(query_str)
            result = cursor.fetchall()
            self._logger.info('SqliteStorageImpl.get_data() exit')
            return result
        except Exception:
            self._logger.exception('exception in SqliteStorageImpl.get_data()')
            raise
        finally:
            connection.close()

    # spec: (int, int) -> None
    def clear(self, id_clear_range):
        connection = connect(self._db_file)
        self._logger.info('SqliteStorageImpl.clear(%(id_range)s) enter' % {'id_range':id_clear_range})
        try:
            cursor = connection.cursor()
            query_str = 'delete from STAT_DATA where id between ? and ?'
            cursor.execute(query_str, id_clear_range)
            connection.commit()
            self._logger.info('SqliteStorageImpl.clear(%(id_range)s) exit' % {'id_range':id_clear_range})
        except Exception:
            self._logger.exception('exception in SqliteStorageImpl.clear(%(id_range)s)' % {'id_range':id_clear_range})
            raise
        finally:
            connection.close()

    _db_file = None
    _logger = None

__author__ = 'andrey.ushakov'
