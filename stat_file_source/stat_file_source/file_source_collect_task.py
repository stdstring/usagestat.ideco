from __future__ import unicode_literals
import logging
from stat_file_source.file_source_collect_task_impl import FileSourceCollectTaskImpl
from stat_file_source.file_source_collector import FileSourceCollector
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_lib/stat_db_lib'))
from sqlite_storage_impl import SqliteStorageImpl

def read_file_content(source_filename):
    source = open(source_filename, 'r')
    try:
        return source.readlines()
    finally:
        source.close()

class FileSourceCollectTask(object):

    # spec: str, [Filter], [Handler], str, str, Logger -> FileSourceCollectTask
    def __init__(self, source_id, filters, handlers, source_filename, db_dest_filename, logger = logging.getLogger('stat_file_source.file_source_collect_task')):
        self._source_id = source_id
        self._collector = FileSourceCollector(filters, handlers)
        self._source_filename = source_filename
        self._db_dest_filename = db_dest_filename
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        storage = SqliteStorageImpl(self._db_dest_filename, self._logger.getChild('sqlite_storage_impl'))
        return FileSourceCollectTaskImpl(self._source_id, self._collector, lambda: read_file_content(self._source_filename), storage, self._logger).execute()

    _source_id = None
    _collector = None
    _source_filename = None
    _db_dest_filename = None
    _logger = None

__author__ = 'andrey.ushakov'
