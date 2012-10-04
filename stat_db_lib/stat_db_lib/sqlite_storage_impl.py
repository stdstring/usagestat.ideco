from __future__ import unicode_literals
from _sqlite3 import connect
import storage

class SqliteStorageImpl(storage.Storage):

    def __init__(self, db_file_path, logger = None):
        self._db_file_path = db_file_path
        self._logger = logger

    # spec: str, [(str, str)] -> bool
    def save_data(self, source_id, data_list):
        self._log_info('save_data(%(source)s, data_list) enter' % {'source': source_id})
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            for data_pair in data_list:
                self._save_item_impl(cursor, source_id, data_pair[0], data_pair[1])
            connection.commit()
            self._log_info('save_data(%(source)s, data_list) exit' % {'source': source_id})
            return True
        except Exception:
            self._log_exception('Exception in save_data(%(source)s, data_list)' % {'source': source_id})
            return False
        finally:
            connection.close()

    # spec: str, str, str -> bool
    def save_item(self, source_id, category, data):
        self._log_info('save_item(%(source)s, %(category)s, %(data)s) enter' % {'source': source_id, 'category': category, 'data': data})
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            self._save_item_impl(cursor, source_id, category, data)
            connection.commit()
            self._log_info('save_item(%(source)s, %(category)s, %(data)s) exit' % {'source': source_id, 'category': category, 'data': data})
            return True
        except Exception:
            self._log_exception('Exception in save_item(%(source)s, %(category)s, %(data)s)' % {'source': source_id, 'category': category, 'data': data})
            return False
        finally:
            connection.close()

    # spec: Sqlite3Cursor, str, str, str -> None
    def _save_item_impl(self, cursor, source_id, category, data):
        try:
            self._log_info('_save_item_impl(%(source)s, %(category)s, %(data)s) enter' % {'source': source_id, 'category': category, 'data': data})
            query = "insert into STAT_DATA(ID, SOURCE, CATEGORY, TIMEMARKER, DATA) values(NULL, ?, ?, datetime('now', 'localtime'), ?)"
            cursor.execute(query, (source_id, category, data))
            self._log_info('_save_item_impl(%(source)s, %(category)s, %(data)s) exit' % {'source': source_id, 'category': category, 'data': data})
        except Exception:
            self._log_exception('Exception in _save_item_impl(%(source)s, %(category)s, %(data)s)' % {'source': source_id, 'category': category, 'data': data})
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
