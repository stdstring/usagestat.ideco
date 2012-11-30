from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_db_source.storage.data_collector import DataCollector
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.simple_process_task import SimpleProcessTask

class TestDataCollector(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestDataCollector, self).__init__(methodName)
        self._mox = None
        self._connection = None
        self._cursor = None
        self._data_collector_logger = None
        self._collect_task_logger = None

    def setUp(self):
        self._mox = Mox()
        self._connection = self._mox.CreateMockAnything()
        self._cursor = self._mox.CreateMockAnything()
        self._collect_task_list = [CollectTask(['q1', 'q2'], SimpleProcessTask()),
                                   CollectTask(['q3'], SimpleProcessTask())]
        self._data_collector_logger = self._mox.CreateMock(Logger)
        self._collect_task_logger = self._mox.CreateMock(Logger)

    def test_collect_data(self):
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._connection.cursor().AndReturn(self._cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._collect_task_logger.info('collect_data(query_executer) enter')
        # q1
        self._collect_task_logger.info('_collect_data_item(q1) enter')
        self._cursor.execute('q1')
        self._cursor.fetchall().AndReturn([('c1.1', 'd1'), ('c1.2', 'd2')])
        self._collect_task_logger.info('_collect_data_item(q1) exit')
        # q2
        self._collect_task_logger.info('_collect_data_item(q2) enter')
        self._cursor.execute('q2')
        self._cursor.fetchall().AndReturn([('c2.1', 'd33')])
        self._collect_task_logger.info('_collect_data_item(q2) exit')
        self._collect_task_logger.info('collect_data(query_executer) exit')
        self._collect_task_logger.info('collect_data(query_executer) enter')
        # q3
        self._collect_task_logger.info('_collect_data_item(q3) enter')
        self._cursor.execute('q3')
        self._cursor.fetchall().AndReturn([('c3.1', 'd666'), ('c3.2', 'd999')])
        self._collect_task_logger.info('_collect_data_item(q3) exit')
        self._collect_task_logger.info('collect_data(query_executer) exit')
        self._connection.close()
        self._data_collector_logger.info('collect_data(collect_task_list) exit')
        self._mox.ReplayAll()
        data_collector = DataCollector(lambda: self._connection, self._data_collector_logger)
        data_collector.collect_data(self._collect_task_list)
        self._mox.VerifyAll()

    def test_collect_data_with_exception(self):
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._connection.cursor().AndReturn(self._cursor)
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._collect_task_logger.info('collect_data(query_executer) enter')
        # q1
        self._collect_task_logger.info('_collect_data_item(q1) enter')
        self._cursor.execute('q1')
        self._cursor.fetchall().AndReturn([('c1.1', 'd1'), ('c1.2', 'd2')])
        self._collect_task_logger.info('_collect_data_item(q1) exit')
        # q2
        self._collect_task_logger.info('_collect_data_item(q2) enter')
        self._cursor.execute('q2').AndRaise(Exception())
        self._collect_task_logger.exception('exception in _collect_data_item(q2)')
        self._collect_task_logger.exception('exception in collect_data(query_executer)')
        self._data_collector_logger.exception('exception in collect_data(collect_task_list)')
        self._connection.close()
        self._mox.ReplayAll()
        data_collector = DataCollector(lambda: self._connection, self._data_collector_logger)
        self.assertRaises(Exception, lambda :data_collector.collect_data(self._collect_task_list))
        self._mox.VerifyAll()

__author__ = 'andrey.ushakov'
