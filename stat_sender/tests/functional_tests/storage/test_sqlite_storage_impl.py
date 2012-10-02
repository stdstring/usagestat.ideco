from __future__ import unicode_literals
from datetime import datetime
from unittest.case import TestCase
from src.storage.sqlite_storage_impl import SqliteStorageImpl
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
from db_manager import DBManager

class TestSqliteStorageImpl(TestCase):

    def setUp(self):
        self._db_manager.__enter__()

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_db_metadata(self):
        actual_metadata = self._db_manager.execute_query("select name, sql from SQLITE_MASTER where type = 'table'")
        expected_metadata = [('STAT_DATA', 'CREATE TABLE STAT_DATA(ID INTEGER PRIMARY KEY, CATEGORY TEXT, TIMEMARKER TEXT, DATA BLOB)')]
        self.assertEquals(expected_metadata, actual_metadata)

    def test_get_data(self):
        now = datetime.now()
        source_data = [('CAT1', str(now), 'some data'), ('CAT2', str(now), 'some another data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(CATEGORY, TIMEMARKER, DATA) values(?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._db_manager.get_db_file())
        actual_data = storage.get_data()
        expected_data = [(1, 'CAT1', str(now), 'some data'), (2, 'CAT2', str(now), 'some another data')]
        self.assertEquals(expected_data, actual_data)

    def test_clear(self):
        now = datetime.now()
        source_data = [('CAT1', str(now), 'some data'), ('CAT2', str(now), 'some other data'), ('CAT3', str(now), 'some another data'), ('CAT4', str(now), 'yet some other data')]
        self._db_manager.execute_nonquery('insert into STAT_DATA(CATEGORY, TIMEMARKER, DATA) values(?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._db_manager.get_db_file())
        storage.clear((2, 3))
        actual_data = self._db_manager.execute_query('SELECT ID, CATEGORY, TIMEMARKER, DATA FROM STAT_DATA ORDER BY ID')
        expected_data = [(1, 'CAT1', str(now), 'some data'), (4, 'CAT4', str(now), 'yet some other data')]
        self.assertEquals(expected_data, actual_data)

    _db_manager = DBManager('../stat_sender_db')

__author__ = 'andrey.ushakov'