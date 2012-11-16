from __future__ import unicode_literals
from datetime import datetime
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_sender.storage.sqlite_storage import SqliteStorage
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
import sqlite_db_manager

class TestSqliteStorage(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSqliteStorage, self).__init__(methodName)
        self._mox = None
        self._logger = None
        self._db_manager = sqlite_db_manager.SqliteDbManager('../stat_sender_db')
        self._now = datetime.now()
        self._str_now = str(self._now)

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
        source_data = [('SRC1', 'CAT1', str(self._now), 'some data'), ('SRC2', 'CAT2', self._str_now, 'some another data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(SOURCE, CATEGORY, TIMEMARKER, DATA) values(?, ?, ?, ?)', source_data)
        storage = SqliteStorage(self._db_manager.connection_string, self._logger)
        actual_data = storage.get_data()
        expected_data = [(1, 'SRC1', 'CAT1', self._str_now, 'some data'), (2, 'SRC2', 'CAT2', self._str_now, 'some another data')]
        self.assertEquals(expected_data, actual_data)
        self._mox.VerifyAll()

    def test_clear(self):
        self._logger.info('clear((2, 3)) enter')
        self._logger.info('clear((2, 3)) exit')
        self._mox.ReplayAll()
        source_data = [('SRC1', 'CAT1', self._str_now, 'some data'),
            ('SRC2', 'CAT2', self._str_now, 'some other data'),
            ('SRC2', 'CAT3', self._str_now, 'some another data'),
            ('SRC3', 'CAT4', self._str_now, 'yet some other data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(SOURCE, CATEGORY, TIMEMARKER, DATA) values(?, ?, ?, ?)', source_data)
        storage = SqliteStorage(self._db_manager.connection_string, self._logger)
        storage.clear((2, 3))
        actual_data = self._db_manager.execute_query('SELECT ID, SOURCE, CATEGORY, TIMEMARKER, DATA FROM STAT_DATA ORDER BY ID')
        expected_data = [(1, 'SRC1', 'CAT1', self._str_now, 'some data'), (4, 'SRC3', 'CAT4', self._str_now, 'yet some other data')]
        self.assertEquals(expected_data, actual_data)
        self._mox.VerifyAll()

__author__ = 'andrey.ushakov'