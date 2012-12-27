from __future__ import unicode_literals
import io
from stat_source_common.storage import sqlite_storage
import file_source_collect_task_impl
import file_source_collector

# spec: str, str -> [str]
def read_file_content(source_filename, encoding):
    source = io.open(source_filename, 'rb')
    try:
        data = source.read()
        decoded_data = data.decode(encoding)
        return decoded_data.splitlines()
    finally:
        source.close()

class FileSourceCollectTask(object):

    # spec: str, [Filter], [Handler], OrderedDict, str, str, str, Logger -> FileSourceCollectTask
    def __init__(self, source_id, filters, handlers, initial_state, source_filename, source_encoding, db_dest_filename, logger):
        self._source_id = source_id
        self._collector = file_source_collector.FileSourceCollector(filters, handlers, initial_state)
        self._source_filename = source_filename
        self._source_encoding = source_encoding
        self._db_dest_filename = db_dest_filename
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        storage = sqlite_storage.SqliteStorage(self._db_dest_filename, self._logger.getChild('sqlite_storage'))
        source_provider = lambda: read_file_content(self._source_filename, self._source_encoding)
        task_impl = file_source_collect_task_impl.FileSourceCollectTaskImpl(self._source_id, self._collector, source_provider, storage, self._logger)
        return task_impl.execute()

__author__ = 'andrey.ushakov'
