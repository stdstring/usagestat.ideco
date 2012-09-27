from __future__ import unicode_literals
from datetime import datetime, timedelta
from unittest.case import TestCase
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
import time
from src.sqlite_storage_impl import SqliteStorageImpl

sys.path.append(os.path.abspath('../stat_sender_db/functional_test_utils'))
from db_manager import DBManager

class TestSqliteStorageImpl(TestCase):

    def setUp(self):
        self._db_manager.__enter__()

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_save_data(self):
        now = datetime.now()
        print now
        storage = SqliteStorageImpl(self._db_manager.get_db_file(), None)
        storage.save('category1', 'some portion of data')
        storage.save('category2', 'yet one some portion of data')
        actual = self._db_manager.execute_query('select ID, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID')
        expected = [(1, 'category1', 'some portion of data'), (2, 'category2', 'yet one some portion of data')]
        self._check_data(now, expected, actual)

    # datetime, [(int, str, str)], [(int, str, str, str)]
    def _check_data(self, now, expected, actual):
        self.assertEqual(len(expected), len(actual))
        index = 0
        while index < len(expected):
            self.assertEqual(expected[index][0], actual[index][0])
            self.assertEqual(expected[index][1], actual[index][1])
            self.assertEqual(expected[index][2], actual[index][3])
            time_str = time.strptime(actual[index][2], '%Y-%m-%d %H:%M:%S')
            actualDateTime = datetime(year=time_str.tm_yday, month=time_str.tm_mon, day=time_str.tm_mday, hour=time_str.tm_hour, minute=time_str.tm_min, second=time_str.tm_sec)
            self.assertTrue(actualDateTime-now < timedelta(seconds = 10))
            index += 1

    _db_manager = DBManager('../stat_sender_db')

__author__ = 'andrey.ushakov'
