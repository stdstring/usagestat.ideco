from __future__ import unicode_literals
from _sqlite3 import connect
import storage

class SqliteStorageImpl(storage.Storage):

    def __init__(self, db_file_path, logger = None):
        self._db_file_path = db_file_path
        self._logger = logger

    # spec: [(str, str)] -> bool
    def save_data(self, data_list):
        self._log_info('SqliteStorageImpl.save_data(data_list) enter')
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            for data_pair in data_list:
                self._save_item_impl(cursor, data_pair[0], data_pair[1])
            connection.commit()
            self._log_info('SqliteStorageImpl.save_data(data_list) exit')
            return True
        except Exception:
            self._log_exception('exception in SqliteStorageImpl.save_data(data_list)')
            return False
        finally:
            connection.close()

    # spec: str, str -> bool
    def save_item(self, category, data):
        self._log_info('SqliteStorageImpl.save_item(%(category)s,%(data)s) enter' % {'category': category, 'data': data})
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            self._save_item_impl(cursor, category, data)
            connection.commit()
            self._log_info('SqliteStorageImpl.save_item(%(category)s,%(data)s) exit' % {'category': category, 'data': data})
            return True
        except Exception:
            self._log_exception('exception in SqliteStorageImpl.save_item(%(category)s,%(data)s)' % {'category': category, 'data': data})
            return False
        finally:
            connection.close()

    # spec: Sqlite3Cursor, str, str -> None
    def _save_item_impl(self, cursor, category, data):
        try:
            self._log_info('Start saving the item (%(category)s,%(data)s) enter' % {'category': category, 'data': data})
            query = "insert into STAT_DATA(ID, CATEGORY, TIMEMARKER, DATA) values(NULL, ?, datetime('now', 'localtime'), ?)"
            cursor.execute(query, (category, data))
            self._log_info('Finish saving the item (%(category)s,%(data)s) enter' % {'category': category, 'data': data})
        except Exception:
            self._log_exception('Exception when saving the item (%(category)s,%(data)s)' % {'category': category, 'data': data})
            raise

    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info(message)

    def _log_exception(self, message):
        if self._logger is not None:
            self._logger.exception(message)

    _db_file_path = None
    _logger = None

__author__ = 'andrey.ushakov'
