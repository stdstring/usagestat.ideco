from __future__ import unicode_literals
from datetime import datetime, timedelta
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_db_funtest_utils import sqlite_db_manager
from stat_source_common.entity.data_item import DataItem
from stat_source_common.storage.sqlite_storage import SqliteStorage
from tests.common.data_portion import DataPortion

class TestSqliteStorage(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSqliteStorage, self).__init__(methodName)
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
        data_portion_list = [DataPortion('some_source', DataItem('category1', 'some portion of data'))]
        expected = [(1, 'some_source', 'category1', 'some portion of data')]
        self._test_save_item_common_body(data_portion_list, expected)

    def test_save_two_items(self):
        data_portion_list = [DataPortion('some_source', DataItem('category1', 'some portion of data')),
                             DataPortion('some_source', DataItem('category2', 'yet one some portion of data'))]
        expected = [(1, 'some_source', 'category1', 'some portion of data'), (2, 'some_source', 'category2', 'yet one some portion of data')]
        self._test_save_item_common_body(data_portion_list, expected)

    def test_save_two_items_for_different_sources(self):
        data_portion_list = [DataPortion('some_source1', DataItem('category1', 'some portion of data')),
                             DataPortion('some_source2', DataItem('category2', 'yet one some portion of data'))]
        expected = [(1, 'some_source1', 'category1', 'some portion of data'), (2, 'some_source2', 'category2', 'yet one some portion of data')]
        self._test_save_item_common_body(data_portion_list, expected)

    def test_save_data(self):
        data_portion_list = [DataPortion('some_source', [DataItem('category1', 'some portion of data'), DataItem('category2', 'yet one some portion of data')])]
        expected = [(1, 'some_source', 'category1', 'some portion of data'), (2, 'some_source', 'category2', 'yet one some portion of data')]
        self._test_save_data_common_body(data_portion_list, expected)

    def test_save_two_data_portions(self):
        data_portion_list = [DataPortion('some_source', [DataItem('category1', 'some portion of data'), DataItem('category2', 'yet one some portion of data')]),
                             DataPortion('some_source', [DataItem('category1', 'other portion of data')])]
        expected = [(1, 'some_source', 'category1', 'some portion of data'),
            (2, 'some_source', 'category2', 'yet one some portion of data'),
            (3, 'some_source', 'category1', 'other portion of data')]
        self._test_save_data_common_body(data_portion_list, expected)

    def test_save_two_data_portions_for_different_sources(self):
        data_portion_list = [DataPortion('some_source1', [DataItem('category1', 'some portion of data'), DataItem('category2', 'yet one some portion of data')]),
                             DataPortion('some_source2', [DataItem('category1', 'other portion of data')])]
        expected = [(1, 'some_source1', 'category1', 'some portion of data'),
            (2, 'some_source1', 'category2', 'yet one some portion of data'),
            (3, 'some_source2', 'category1', 'other portion of data')]
        self._test_save_data_common_body(data_portion_list, expected)

    # spec: [DataPortion], [(int, str, str, str)] -> None
    def _test_save_item_common_body(self, data_portion_list, expected):
        for data_portion in data_portion_list:
            self._logger.info('save_item({source:s}, {data_item!s}) enter'.format(source=data_portion.source_id, data_item=data_portion.data))
            self._logger.info('_save_item_impl({source:s}, {data_item!s}) enter'.format(source=data_portion.source_id, data_item=data_portion.data))
            self._logger.info('_save_item_impl({source:s}, {data_item!s}) exit'.format(source=data_portion.source_id, data_item=data_portion.data))
            self._logger.info('save_item({source:s}, {data_item!s}) exit'.format(source=data_portion.source_id, data_item=data_portion.data))
        self._mox.ReplayAll()
        storage = SqliteStorage(self._db_manager.connection_string, self._logger)
        for data_portion in data_portion_list:
            storage.save_item(data_portion.source_id, data_portion.data)
        actual = self._db_manager.execute_query(self._query)
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    # spec: [DataPortion], [(int, str, str, str)] -> None
    def _test_save_data_common_body(self, data_portion_list, expected):
        for data_portion in data_portion_list:
            self._logger.info('save_data({source:s}, data_list) enter'.format(source=data_portion.source_id))
            for data_item in data_portion.data:
                self._logger.info('_save_item_impl({source:s}, {data_item!s}) enter'.format(source=data_portion.source_id, data_item=data_item))
                self._logger.info('_save_item_impl({source:s}, {data_item!s}) exit'.format(source=data_portion.source_id, data_item=data_item))
            self._logger.info('save_data({source:s}, data_list) exit'.format(source=data_portion.source_id))
        self._mox.ReplayAll()
        storage = SqliteStorage(self._db_manager.connection_string, self._logger)
        for data_portion in data_portion_list:
            storage.save_data(data_portion.source_id, data_portion.data)
        actual = self._db_manager.execute_query(self._query)
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
            actualDateTime = datetime.strptime(actual[index][3], '%Y-%m-%d %H:%M:%S')
            self.assertTrue(actualDateTime-self._now < timedelta(seconds = 10))
            index += 1

__author__ = 'andrey.ushakov'
