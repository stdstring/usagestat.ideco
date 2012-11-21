from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_source_common.entity.data_item import DataItem
from stat_source_common.storage.sqlite_storage import SqliteStorage
from tests.common.data_portion import DataPortion

class TestSqliteStorage(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSqliteStorage, self).__init__(methodName)
        self._mox = None
        self._connection = None
        self._cursor = None
        self._logger = None
        self._query_str = "insert into STAT_DATA(ID, SOURCE, CATEGORY, TIMEMARKER, DATA) values(NULL, ?, ?, datetime('now', 'localtime'), ?)"

    def setUp(self):
        self._mox = Mox()
        self._connection = self._mox.CreateMockAnything()
        self._cursor = self._mox.CreateMockAnything()
        self._logger = self._mox.CreateMock(Logger)

    def test_save_single_item(self):
        data_portion_list = [DataPortion('source1', DataItem('category1', 'some data'))]
        self._test_save_items_common_body(data_portion_list)

    def test_save_several_items(self):
        data_portion_list = [DataPortion('source1', DataItem('category1', 'some data')), DataPortion('source2', DataItem('category2', 'some other data'))]
        self._test_save_items_common_body(data_portion_list)

    def test_save_single_data(self):
        data_item_list = [DataItem('category1', 'some data'), DataItem('category2', 'some other data')]
        data_portion_list = [DataPortion('source1', data_item_list)]
        self._test_save_data_common_body(data_portion_list)

    def test_save_several_data(self):
        data_item_list1 = [DataItem('category1', 'some data'), DataItem('category2', 'some other data')]
        data_item_list2 = [DataItem('category1', 'yet one some data'), DataItem('category666', 'yet one some other data')]
        data_portion_list = [DataPortion('source1', data_item_list1), DataPortion('source2', data_item_list2)]
        self._test_save_data_common_body(data_portion_list)

    def test_save_item_with_exception(self):
        data_portion = DataPortion('source1', DataItem('category1', 'some data'))
        self._logger.info("save_item({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_portion.data))
        self._connection.cursor().AndReturn(self._cursor)
        self._logger.info("_save_item_impl({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_portion.data))
        self._cursor.execute(self._query_str, (data_portion.source_id, data_portion.data.category, data_portion.data.data)).AndRaise(Exception())
        self._logger.exception("exception in _save_item_impl({source:s}, {data_item!s})".format(source=data_portion.source_id, data_item=data_portion.data))
        self._connection.close()
        self._logger.exception("exception in save_item({source:s}, {data_item!s})".format(source=data_portion.source_id, data_item=data_portion.data))
        self._mox.ReplayAll()
        storage = SqliteStorage(lambda: self._connection, self._logger)
        storage.save_item(data_portion.source_id, data_portion.data)
        self._mox.VerifyAll()

    def test_save_data_with_exception(self):
        data_item = DataItem('category1', 'some data')
        data_portion = DataPortion('source1', [data_item])
        self._logger.info('save_data({0:s}, data_list) enter'.format(data_portion.source_id))
        self._connection.cursor().AndReturn(self._cursor)
        self._logger.info("_save_item_impl({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_item))
        self._cursor.execute(self._query_str, (data_portion.source_id, data_item.category, data_item.data)).AndRaise(Exception())
        self._logger.exception("exception in _save_item_impl({source:s}, {data_item!s})".format(source=data_portion.source_id, data_item=data_item))
        self._connection.close()
        self._logger.exception('exception in save_data({0:s}, data_list)'.format(data_portion.source_id))
        self._mox.ReplayAll()
        storage = SqliteStorage(lambda: self._connection, self._logger)
        storage.save_data(data_portion.source_id, data_portion.data)
        self._mox.VerifyAll()

    # spec: [DataPortion] -> None
    def _test_save_items_common_body(self, data_portion_list):
        for data_portion in data_portion_list:
            self._logger.info("save_item({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_portion.data))
            self._connection.cursor().AndReturn(self._cursor)
            self._logger.info("_save_item_impl({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_portion.data))
            self._cursor.execute(self._query_str, (data_portion.source_id, data_portion.data.category, data_portion.data.data))
            self._logger.info("_save_item_impl({source:s}, {data_item!s}) exit".format(source=data_portion.source_id, data_item=data_portion.data))
            self._connection.commit()
            self._logger.info("save_item({source:s}, {data_item!s}) exit".format(source=data_portion.source_id, data_item=data_portion.data))
            self._connection.close()
        self._mox.ReplayAll()
        storage = SqliteStorage(lambda: self._connection, self._logger)
        for data_portion in data_portion_list:
            result = storage.save_item(data_portion.source_id, data_portion.data)
            self.assertTrue(result)
        self._mox.VerifyAll()

    # spec: [DataPortion] -> None
    def _test_save_data_common_body(self, data_portion_list):
        for data_portion in data_portion_list:
            self._logger.info('save_data({0:s}, data_list) enter'.format(data_portion.source_id))
            self._connection.cursor().AndReturn(self._cursor)
            for data_item in data_portion.data:
                self._logger.info("_save_item_impl({source:s}, {data_item!s}) enter".format(source=data_portion.source_id, data_item=data_item))
                self._cursor.execute(self._query_str, (data_portion.source_id, data_item.category, data_item.data))
                self._logger.info("_save_item_impl({source:s}, {data_item!s}) exit".format(source=data_portion.source_id, data_item=data_item))
            self._connection.commit()
            self._logger.info('save_data({0:s}, data_list) exit'.format(data_portion.source_id))
            self._connection.close()
        self._mox.ReplayAll()
        storage = SqliteStorage(lambda: self._connection, self._logger)
        for data_portion in data_portion_list:
            result = storage.save_data(data_portion.source_id, data_portion.data)
            self.assertTrue(result)
        self._mox.VerifyAll()

__author__ = 'andrey.ushakov'
