from __future__ import unicode_literals
from unittest.case import TestCase
from stat_source_common.entity.data_item import DataItem
from stat_db_source.task.transform_process_task import TransformProcessTask

class TestTransformProcessTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestTransformProcessTask, self).__init__(methodName)
        category_transformer = lambda row: 'category.{0!s}'.format(row[0])
        data_transformer = lambda row: '{0!s}:{1!s}'.format(row[1], row[2])
        self._process_task = TransformProcessTask(category_transformer, data_transformer)

    def test_process_empty_list(self):
        self.assertEqual([], self._process_task.process([]))

    def test_process_list_with_correct_tuples(self):
        expected = [DataItem('category.cat1', 'data1:subdata1'),
                    DataItem('category.cat2', 'data2:subdata2'),
                    DataItem('category.cat1', 'data3:subdata3'),
                    DataItem('category.cat3', 'data4:subdata4')]
        source = [[('cat1', 'data1', 'subdata1'), ('cat2', 'data2', 'subdata2')], [('cat1', 'data3', 'subdata3')], [('cat3', 'data4', 'subdata4')]]
        self.assertEqual(expected, self._process_task.process(source))

    def test_process_list_with_incorrect_tuples(self):
        source = [[('cat1', 'data1')]]
        self.assertRaises(IndexError, lambda: self._process_task.process(source))

__author__ = 'andrey.ushakov'
