from __future__ import unicode_literals
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_lib/stat_db_lib'))
import sqlite_storage_impl

class TestOtherSource(object):

    def __init__(self, db_file_path, logger):
        self._logger = logger
        storage_logger = self._logger.getChild('sqlite_storage_impl')
        self._storage = sqlite_storage_impl.SqliteStorageImpl(db_file_path, storage_logger)

    def collect_stat_data(self):
        stat_data = [('bad_packet_count', str(10)),
            ('good_packet_count', str(13)),
            ('false_positive_antivirus_count', str(4))]
        self._storage.save_data(self._source, stat_data)

    _source = 'other_source'

__author__ = 'andrey.ushakov'