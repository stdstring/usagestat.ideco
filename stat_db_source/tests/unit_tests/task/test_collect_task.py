from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_source_common.entity.data_item import DataItem
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.process_task import ProcessTask
from tests.common.custom_test_exception import CustomTestException

class TestCollectTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCollectTask, self).__init__(methodName)
        self._mox = None
        self._logger = None,
        self._query_executer = None
        self._process_task = None
        self._collect_task = None
        self._query_list = ['q1', 'q2']
        self._intermediate_data_list = [[('c1', 'd1', 'sd1'), ('c2', 'd2', 'sd2')], [('c1', 'd3', 'sd3')]]
        self._data_item_list = [DataItem('cat.c1', 'd1:sd1'), DataItem('cat.c2', 'd2:sd2'), DataItem('cat.c3', 'd3:sd3')]

    def setUp(self):
        self._mox = Mox()
        self._logger = self._mox.CreateMock(Logger)
        self._process_task = self._mox.CreateMock(ProcessTask)
        self._query_executer = self._mox.CreateMockAnything()
        self._collect_task = CollectTask(self._query_list, self._process_task)

    def test_normal_life_cycle(self):
        self._set_collect_data_expectations()
        self._set_process_data_expectations()
        self._mox.ReplayAll()
        self.assertFalse(self._collect_task.contains_data())
        self._collect_task.collect_data(self._query_executer, self._logger)
        self.assertTrue(self._collect_task.contains_data())
        self._collect_task.process_data(self._logger)
        self.assertFalse(self._collect_task.contains_data())
        self._mox.VerifyAll()

    def test_exception_when_collect_data(self):
        self._logger.info('collect_data(query_executer) enter')
        self._logger.info('_collect_data_item({0:s}) enter'.format(self._query_list[0]))
        self._query_executer(self._query_list[0]).AndReturn(self._intermediate_data_list[0])
        self._logger.info('_collect_data_item({0:s}) exit'.format(self._query_list[0]))
        self._logger.info('_collect_data_item({0:s}) enter'.format(self._query_list[1]))
        self._query_executer(self._query_list[1]).AndRaise(CustomTestException())
        self._logger.exception('exception in _collect_data_item({0:s})'.format(self._query_list[1]))
        self._logger.exception('exception in collect_data(query_executer)')
        self._mox.ReplayAll()
        self.assertFalse(self._collect_task.contains_data())
        self.assertRaises(CustomTestException, lambda: self._collect_task.collect_data(self._query_executer, self._logger))
        self.assertFalse(self._collect_task.contains_data())
        self._mox.VerifyAll()

    def test_exception_when_process_data(self):
        self._set_collect_data_expectations()
        self._logger.info('process_data() enter')
        self._process_task.process(self._intermediate_data_list).AndRaise(CustomTestException())
        self._logger.exception('exception in process_data()')
        self._mox.ReplayAll()
        self.assertFalse(self._collect_task.contains_data())
        self._collect_task.collect_data(self._query_executer, self._logger)
        self.assertTrue(self._collect_task.contains_data())
        self.assertRaises(CustomTestException, lambda: self._collect_task.process_data(self._logger))
        self.assertFalse(self._collect_task.contains_data())
        self._mox.VerifyAll()

    def _set_collect_data_expectations(self):
        self._logger.info('collect_data(query_executer) enter')
        index = 0
        while index < len(self._query_list):
            self._logger.info('_collect_data_item({0:s}) enter'.format(self._query_list[index]))
            self._query_executer(self._query_list[index]).AndReturn(self._intermediate_data_list[index])
            self._logger.info('_collect_data_item({0:s}) exit'.format(self._query_list[index]))
            index += 1
        self._logger.info('collect_data(query_executer) exit')

    def _set_process_data_expectations(self):
        self._logger.info('process_data() enter')
        self._process_task.process(self._intermediate_data_list).AndReturn(self._data_item_list)
        self._logger.info('process_data() exit')

__author__ = 'andrey.ushakov'
