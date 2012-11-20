from __future__ import unicode_literals
from _sqlite3 import connect
import storage

class SqliteStorage(storage.Storage):

    def __init__(self, db_file_path, logger = None):
        self._db_file_path = db_file_path
        self._logger = logger

    # spec: str, [DataItem] -> bool
    def save_data(self, source_id, data_item_list):
        self._log_info('save_data({0:s}, data_list) enter'.format(source_id))
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            for data_item in data_item_list:
                self._save_item_impl(cursor, source_id, data_item)
            connection.commit()
            self._log_info('save_data({0:s}, data_list) exit'.format(source_id))
            return True
        except Exception:
            self._log_exception('Exception in save_data({0:s}, data_list)'.format(source_id))
            return False
        finally:
            connection.close()

    # spec: str, DataItem -> bool
    def save_item(self, source_id, data_item):
        self._log_info('save_item({source:s}, {data_item!s}) enter'.format(source=source_id, data_item=data_item))
        connection = connect(self._db_file_path)
        try:
            cursor = connection.cursor()
            self._save_item_impl(cursor, source_id, data_item)
            connection.commit()
            self._log_info('save_item({source:s}, {data_item!s}) exit'.format(source=source_id, data_item=data_item))
            return True
        except Exception:
            self._log_exception('Exception in save_item({source:s}, {data_item!s})'.format(source=source_id, data_item=data_item))
            return False
        finally:
            connection.close()

    # spec: Sqlite3Cursor, str, DataItem -> None
    def _save_item_impl(self, cursor, source_id, data_item):
        try:
            self._log_info('_save_item_impl({source:s}, {data_item!s}) enter'.format(source=source_id, data_item=data_item))
            query = "insert into STAT_DATA(ID, SOURCE, CATEGORY, TIMEMARKER, DATA) values(NULL, ?, ?, datetime('now', 'localtime'), ?)"
            cursor.execute(query, (source_id, data_item.category, data_item.data))
            self._log_info('_save_item_impl({source:s}, {data_item!s}) exit'.format(source=source_id, data_item=data_item))
        except Exception:
            self._log_exception('Exception in _save_item_impl({source:s}, {data_item!s})'.format(source=source_id, data_item=data_item))
            raise

    # spec: str -> None
    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info(message)

    # spec: str -> None
    def _log_exception(self, message):
        if self._logger is not None:
            self._logger.exception(message)

    _db_file_path = None
    _logger = None

__author__ = 'andrey.ushakov'
