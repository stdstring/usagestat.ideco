from __future__ import unicode_literals
from stat_source_common.entity.data_item import DataItem
from stat_source_common.storage import sqlite_storage

class TestOtherSource(object):

    def __init__(self, db_file_path, logger):
        self._logger = logger
        storage_logger = self._logger.getChild('sqlite_storage')
        self._storage = sqlite_storage.SqliteStorage(db_file_path, storage_logger)

    def collect_stat_data(self):
        stat_data = [DataItem('bad_packet_count', 10),
            DataItem('good_packet_count', 13),
            DataItem('false_positive_antivirus_count', 4)]
        self._storage.save_data(self._source, stat_data)

    _source = 'other_source'

__author__ = 'andrey.ushakov'