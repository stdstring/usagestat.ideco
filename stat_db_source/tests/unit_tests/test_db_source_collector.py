from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_source_common.entity.data_item import DataItem
from stat_source_common.storage.storage import Storage
from stat_db_source.db_source_collector import DbSourceCollector
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.simple_process_task import SimpleProcessTask
from stat_db_source.task.transform_process_task import TransformProcessTask
from tests.common.collector_expectations import set_collect_data_expectations, set_process_data_expectations
from tests.common.custom_test_exception import CustomTestException

class TestDbSourceCollector(TestCase):
    def __init__(self, methodName='runTest'):
        super(TestDbSourceCollector, self).__init__(methodName)
        self._mox = None
        self._source_connection = None
        self._source_cursor = None
        self._dest_storage = None
        self._logger = None
        self._data_collector_logger = None
        self._collect_task_logger = None
        self._source_id = 'test_db_source'
        self._collect_task_list = None
        self._collector = None

    def setUp(self):
        self._mox = Mox()
        self._source_connection = self._mox.CreateMockAnything()
        self._source_cursor = self._mox.CreateMockAnything()
        self._dest_storage = self._mox.CreateMock(Storage)
        self._logger = self._mox.CreateMock(Logger)
        self._data_collector_logger = self._mox.CreateMock(Logger)
        self._collect_task_logger = self._mox.CreateMock(Logger)
        self._dest_storage_logger = self._mox.CreateMock(Logger)
        category_transformer = lambda row: 'category.{0!s}'.format(row[0])
        data_transformer = lambda row: '{0!s}:{1!s}'.format(row[1], row[2])
        self._collect_task_list = [CollectTask(['q1', 'q2'], SimpleProcessTask()),
                                   CollectTask(['q3'], TransformProcessTask(category_transformer, data_transformer))]
        self._collector = DbSourceCollector(self._source_id,
            self._collect_task_list,
            lambda: self._source_connection,
            lambda logger: self._dest_storage,
            self._logger)

    def test_normal_collect(self):
        self._logger.info('collect() enter')
        self._logger.getChild('data_collector').AndReturn(self._data_collector_logger)
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._source_connection.cursor().AndReturn(self._source_cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q1', 'q2'],
            [[('cat1', 'data1'), ('cat2', 'data2')], [('cat1', 'data3')]])
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q3'],
            [[('cat1', 'data1', 'subdata1'), ('cat2', 'data2', 'subdata2'), ('cat1', 'data3', 'subdata3')]])
        self._source_connection.close()
        self._data_collector_logger.info(u'collect_data(collect_task_list) exit')
        self._logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._logger.getChild('dest_storage').AndReturn(self._dest_storage_logger)
        save_items_list = [[DataItem(category='cat1', data='data1'), DataItem(category='cat2', data='data2'), DataItem(category='cat1', data='data3')],
            [DataItem(category='category.cat1', data='data1:subdata1'), DataItem(category='category.cat2', data='data2:subdata2'), DataItem(category='category.cat1', data='data3:subdata3')]]
        set_process_data_expectations(self._collect_task_logger, self._dest_storage, self._source_id, save_items_list)
        self._logger.info('collect() exit')
        self._mox.ReplayAll()
        self._collector.collect()
        self._mox.VerifyAll()

    def test_exception_when_collect(self):
        self._logger.info('collect() enter')
        self._logger.getChild('data_collector').AndReturn(self._data_collector_logger)
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._source_connection.cursor().AndReturn(self._source_cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._collect_task_logger.info('collect_data(query_executer) enter')
        self._collect_task_logger.info('_collect_data_item(q1) enter')
        self._source_cursor.execute('q1').AndRaise(CustomTestException())
        self._collect_task_logger.exception('exception in _collect_data_item(q1)')
        self._collect_task_logger.exception('exception in collect_data(query_executer)')
        self._source_connection.close()
        self._data_collector_logger.exception('exception in collect_data(collect_task_list)')
        self._logger.exception('exception in collect()')
        self._mox.ReplayAll()
        self.assertRaises(CustomTestException, lambda: self._collector.collect())
        self._mox.VerifyAll()

    def test_exception_when_process(self):
        self._logger.info('collect() enter')
        self._logger.getChild('data_collector').AndReturn(self._data_collector_logger)
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._source_connection.cursor().AndReturn(self._source_cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q1', 'q2'],
            [[('cat1',), ('cat2',)], [('cat1',)]])
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q3'],
            [[('cat1', 'data1', 'subdata1'), ('cat2', 'data2', 'subdata2'), ('cat1', 'data3', 'subdata3')]])
        self._source_connection.close()
        self._data_collector_logger.info(u'collect_data(collect_task_list) exit')
        self._logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._logger.getChild('dest_storage').AndReturn(self._dest_storage_logger)
        self._collect_task_logger.info('process_data() enter')
        self._collect_task_logger.exception('exception in process_data()')
        self._logger.exception(u'exception in collect()')
        self._mox.ReplayAll()
        self.assertRaises(IndexError, lambda: self._collector.collect())
        self._mox.VerifyAll()

    def test_exception_when_save(self):
        self._logger.info('collect() enter')
        self._logger.getChild('data_collector').AndReturn(self._data_collector_logger)
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._source_connection.cursor().AndReturn(self._source_cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q1', 'q2'],
            [[('cat1', 'data1'), ('cat2', 'data2')], [('cat1', 'data3')]])
        set_collect_data_expectations(self._collect_task_logger,
            self._source_cursor,
            ['q3'],
            [[('cat1', 'data1', 'subdata1'), ('cat2', 'data2', 'subdata2'), ('cat1', 'data3', 'subdata3')]])
        self._source_connection.close()
        self._data_collector_logger.info(u'collect_data(collect_task_list) exit')
        self._logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._logger.getChild('dest_storage').AndReturn(self._dest_storage_logger)
        self._collect_task_logger.info('process_data() enter')
        self._collect_task_logger.info('process_data() exit')
        save_data = [DataItem(category='cat1', data='data1'), DataItem(category='cat2', data='data2'), DataItem(category='cat1', data='data3')]
        self._dest_storage.save_data(self._source_id, save_data).AndRaise(CustomTestException())
        self._logger.exception(u'exception in collect()')
        self._mox.ReplayAll()
        self.assertRaises(CustomTestException, lambda: self._collector.collect())
        self._mox.VerifyAll()

__author__ = 'andrey.ushakov'
