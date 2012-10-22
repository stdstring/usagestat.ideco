from __future__ import unicode_literals
import logging
import psycopg2
from stat_server.storage.storage import Storage

class PgStorageImpl(Storage):
    def __init__(self, connection_string, logger = logging.getLogger('stat_server.pg_storage_impl')):
        self._connection_string = connection_string
        self._logger = logger

    # spec: str, str, str, (str | None), (int | None) -> PgStorageImpl
    @staticmethod
    def create(database, user, pwd, host = None, port = None, logger = logging.getLogger('stat_server.pg_storage_impl')):
        if database is None:
            database = 'stat_db'
        storage = ['dbname={0:s}'.format(database), 'user={0:s}'.format(user), 'password={0:s}'.format(pwd)]
        if host is not None:
            storage.append('host={0:s}'.format(host))
        if host is not None:
            storage.append('port={0:d}'.format(port))
        connection_string = ' '.join(storage)
        return PgStorageImpl(connection_string, logger)

    # spec: [StatDataEntity] -> None
    def save_data(self, data):
        self._log_info('save_data(data) enter')
        connection = psycopg2.connect(self._connection_string)
        try:
            cursor = connection.cursor()
            for item in data:
                self._save_item(cursor, item)
            connection.commit()
            self._log_info('save_data(data) exit')
        except BaseException:
            self._log_exception('exception in save_data(data)')
            raise
        finally:
            connection.close()

    # spec: Cursor, StatDataEntity -> None
    def _save_item(self, cursor, item):
        try:
            self._log_info('save_item(cursor, {0!s}) enter'.format(item))
            query = 'insert into stat_storage(source, category, timemarker, data) values(%s, %s, %s, %s)'
            cursor.execute(query, (item.source, item.category, item.timemarker, item.data))
            self._log_info('save_item(cursor, %(item)s) exit' % {'item': item})
        except BaseException:
            self._log_info('exception in save_item(cursor, {0:s})'.format(item))
            raise

    # spec: str -> None
    def _log_info(self, message):
        if self._logger is not None:
            self._logger.info(message)

    # spec: str -> None
    def _log_exception(self, message):
        if self._logger is not None:
            self._logger.exception(message)

__author__ = 'andrey.ushakov'
