from __future__ import unicode_literals
from datetime import datetime
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from src.storage.sqlite_storage_impl import SqliteStorageImpl
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
from db_manager import DBManager

class TestSqliteStorageImpl(TestCase):

    def setUp(self):
        self._mox = Mox()
        self._logger = self._mox.CreateMock(Logger)
        self._db_manager.__enter__()

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_db_metadata(self):
        actual_metadata = self._db_manager.execute_query("select name, sql from SQLITE_MASTER where type = 'table'")
        expected_metadata = [('STAT_DATA', 'CREATE TABLE STAT_DATA(ID INTEGER PRIMARY KEY, SOURCE TEXT not null, CATEGORY TEXT not null, TIMEMARKER TEXT not null, DATA BLOB not null)')]
        self.assertEquals(expected_metadata, actual_metadata)

    def test_get_data(self):
        self._logger.info('get_data() enter')
        self._logger.info('get_data() exit')
        self._mox.ReplayAll()
        source_data = [('SRC1', 'CAT1', str(self._now), 'some data'), ('SRC2', 'CAT2', str(self._now), 'some another data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(SOURCE, CATEGORY, TIMEMARKER, DATA) values(?, ?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._db_manager.get_db_file(), self._logger)
        actual_data = storage.get_data()
        expected_data = [(1, 'SRC1', 'CAT1', str(self._now), 'some data'), (2, 'SRC2', 'CAT2', str(self._now), 'some another data')]
        self.assertEquals(expected_data, actual_data)
        self._mox.VerifyAll()

    def test_clear(self):
        self._logger.info('clear((2, 3)) enter')
        self._logger.info('clear((2, 3)) exit')
        self._mox.ReplayAll()
        source_data = [('SRC1', 'CAT1', str(self._now), 'some data'),
            ('SRC2', 'CAT2', str(self._now), 'some other data'),
            ('SRC2', 'CAT3', str(self._now), 'some another data'),
            ('SRC3', 'CAT4', str(self._now), 'yet some other data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(SOURCE, CATEGORY, TIMEMARKER, DATA) values(?, ?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._db_manager.get_db_file(), self._logger)
        storage.clear((2, 3))
        actual_data = self._db_manager.execute_query('SELECT ID, SOURCE, CATEGORY, TIMEMARKER, DATA FROM STAT_DATA ORDER BY ID')
        expected_data = [(1, 'SRC1', 'CAT1', str(self._now), 'some data'), (4, 'SRC3', 'CAT4', str(self._now), 'yet some other data')]
        self.assertEquals(expected_data, actual_data)
        self._mox.VerifyAll()

    _mox = None
    _logger = None
    _db_manager = DBManager('../stat_sender_db')
    _now = datetime.now()

__author__ = 'andrey.ushakov'