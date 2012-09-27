from __future__ import unicode_literals
from _sqlite3 import connect
from src.storage import Storage

class SqliteStorageImpl(Storage):

    def __init__(self, db_file_path, logger):
        self._db_file_path = db_file_path
        self._logger = logger

    # spec: str, str -> bool
    def save(self, category, data):
        connection = connect(self._db_file_path)
        self._log_info('SqliteStorageImpl.save(%(category)s,%(data)s) enter' % {'category': category, 'data': data})
        try:
            cursor = connection.cursor()
            query = "insert into STAT_DATA(ID, CATEGORY, TIMEMARKER, DATA) values(NULL, ?, datetime('now', 'localtime'), ?)"
            cursor.execute(query, (category, data))
            connection.commit()
            self._log_info('SqliteStorageImpl.save(%(category)s,%(data)s) exit' % {'category': category, 'data': data})
            return True
        except Exception:
            self._log_exception('exception in SqliteStorageImpl.save(%(category)s,%(data)s)' % {'category': category, 'data': data})
            return False
        finally:
            connection.close()

    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info(message)

    def _log_exception(self, message):
        if self._logger is not None:
            self._logger.exception(message)

    _db_file_path = None
    _logger = None

__author__ = 'andrey.ushakov'
