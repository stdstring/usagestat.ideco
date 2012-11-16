from __future__ import unicode_literals
from datetime import datetime, timedelta
from logging import Logger
from mox import Mox
from unittest.case import TestCase
import time
from stat_db_lib.sqlite_storage_impl import SqliteStorageImpl
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
import sqlite_db_manager

class TestSqliteStorageImpl(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSqliteStorageImpl, self).__init__(methodName)
        self._mox = None
        self._logger = None
        self._now = datetime.now()
        self._db_manager = sqlite_db_manager.SqliteDbManager('../stat_sender_db')
        self._query = 'select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID'

    def setUp(self):
        self._mox = Mox()
        self._logger = self._mox.CreateMock(Logger)
        self._db_manager.__enter__()

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_save_item(self):
        self._logger.info('save_item(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) exit')
        self._logger.info('save_item(some_source, category1, some portion of data) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        storage.save_item('some_source', 'category1', 'some portion of data')
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source', 'category1', 'some portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    def test_save_two_items(self):
        self._logger.info('save_item(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) exit')
        self._logger.info('save_item(some_source, category1, some portion of data) exit')
        self._logger.info('save_item(some_source, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) exit')
        self._logger.info('save_item(some_source, category2, yet one some portion of data) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        storage.save_item('some_source', 'category1', 'some portion of data')
        storage.save_item('some_source', 'category2', 'yet one some portion of data')
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source', 'category1', 'some portion of data'), (2, 'some_source', 'category2', 'yet one some portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    def test_save_two_items_for_different_sources(self):
        self._logger.info('save_item(some_source1, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source1, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source1, category1, some portion of data) exit')
        self._logger.info('save_item(some_source1, category1, some portion of data) exit')
        self._logger.info('save_item(some_source2, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source2, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source2, category2, yet one some portion of data) exit')
        self._logger.info('save_item(some_source2, category2, yet one some portion of data) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        storage.save_item('some_source1', 'category1', 'some portion of data')
        storage.save_item('some_source2', 'category2', 'yet one some portion of data')
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source1', 'category1', 'some portion of data'), (2, 'some_source2', 'category2', 'yet one some portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    def test_save_data(self):
        self._logger.info('save_data(some_source, data_list) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) exit')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) exit')
        self._logger.info('save_data(some_source, data_list) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        data = [('category1', 'some portion of data'), ('category2', 'yet one some portion of data')]
        storage.save_data('some_source', data)
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source', 'category1', 'some portion of data'), (2, 'some_source', 'category2', 'yet one some portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    def test_save_two_data_portions(self):
        self._logger.info('save_data(some_source, data_list) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, some portion of data) exit')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category2, yet one some portion of data) exit')
        self._logger.info('save_data(some_source, data_list) exit')
        self._logger.info('save_data(some_source, data_list) enter')
        self._logger.info('_save_item_impl(some_source, category1, other portion of data) enter')
        self._logger.info('_save_item_impl(some_source, category1, other portion of data) exit')
        self._logger.info('save_data(some_source, data_list) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        data = [('category1', 'some portion of data'), ('category2', 'yet one some portion of data')]
        storage.save_data('some_source', data)
        data = [('category1', 'other portion of data')]
        storage.save_data('some_source', data)
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source', 'category1', 'some portion of data'),
            (2, 'some_source', 'category2', 'yet one some portion of data'),
            (3, 'some_source', 'category1', 'other portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    def test_save_two_data_portions_for_different_sources(self):
        self._logger.info('save_data(some_source1, data_list) enter')
        self._logger.info('_save_item_impl(some_source1, category1, some portion of data) enter')
        self._logger.info('_save_item_impl(some_source1, category1, some portion of data) exit')
        self._logger.info('_save_item_impl(some_source1, category2, yet one some portion of data) enter')
        self._logger.info('_save_item_impl(some_source1, category2, yet one some portion of data) exit')
        self._logger.info('save_data(some_source1, data_list) exit')
        self._logger.info('save_data(some_source2, data_list) enter')
        self._logger.info('_save_item_impl(some_source2, category1, other portion of data) enter')
        self._logger.info('_save_item_impl(some_source2, category1, other portion of data) exit')
        self._logger.info('save_data(some_source2, data_list) exit')
        self._mox.ReplayAll()
        storage = SqliteStorageImpl(self._db_manager.connection_string, self._logger)
        data = [('category1', 'some portion of data'), ('category2', 'yet one some portion of data')]
        storage.save_data('some_source1', data)
        data = [('category1', 'other portion of data')]
        storage.save_data('some_source2', data)
        actual = self._db_manager.execute_query(self._query)
        expected = [(1, 'some_source1', 'category1', 'some portion of data'),
            (2, 'some_source1', 'category2', 'yet one some portion of data'),
            (3, 'some_source2', 'category1', 'other portion of data')]
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    # spec: [(int, str, str, str)], [(int, str, str, str, str)]
    def _check_data(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        index = 0
        while index < len(expected):
            self.assertEqual(expected[index][0], actual[index][0])
            self.assertEqual(expected[index][1], actual[index][1])
            self.assertEqual(expected[index][2], actual[index][2])
            self.assertEqual(expected[index][3], actual[index][4])
            time_str = time.strptime(actual[index][3], '%Y-%m-%d %H:%M:%S')
            actualDateTime = datetime(year=time_str.tm_yday, month=time_str.tm_mon, day=time_str.tm_mday, hour=time_str.tm_hour, minute=time_str.tm_min, second=time_str.tm_sec)
            self.assertTrue(actualDateTime-self._now < timedelta(seconds = 10))
            index += 1

__author__ = 'andrey.ushakov'
