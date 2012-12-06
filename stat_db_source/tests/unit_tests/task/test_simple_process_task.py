from __future__ import unicode_literals
from unittest.case import TestCase
from stat_source_common.entity.data_item import DataItem
from stat_db_source.task.simple_process_task import SimpleProcessTask

class TestSimpleProcessTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSimpleProcessTask, self).__init__(methodName)
        self._process_task = SimpleProcessTask()

    def test_process_empty_list(self):
        self.assertEqual([], self._process_task.process([]))

    def test_process_list_with_pairs(self):
        expected = [DataItem('cat1', 'data1'), DataItem('cat2', 'data2'), DataItem('cat1', 'data3')]
        source = [[('cat1', 'data1'), ('cat2', 'data2')], [('cat1', 'data3')]]
        self.assertEqual(expected, self._process_task.process(source))

    def test_process_list_with_big_tuples(self):
        expected = [DataItem('cat1', 'data1'), DataItem('cat2', 'data2'), DataItem('cat1', 'data3')]
        source = [[('cat1', 'data1', 'other data 1'), ('cat2', 'data2', 'other data 2')], [('cat1', 'data3', 'other data 3')]]
        self.assertEqual(expected, self._process_task.process(source))

    def test_process_list_with_small_tuples(self):
        source = [[('cat1', ), ('cat2', )], [('cat1', )]]
        self.assertRaises(IndexError, lambda: self._process_task.process(source))

__author__ = 'andrey.ushakov'
