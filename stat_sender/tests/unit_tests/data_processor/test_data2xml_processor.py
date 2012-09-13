from __future__ import unicode_literals
from datetime import datetime
import unittest
from unittest.case import TestCase
from src.common.stat_data import StatDataItem, StatData
from src.data_processor.data2xml_processor import Data2XmlProcessor

class TestData2XmlProcessor(TestCase):

    def test_single_data_item_process(self):
        processor = Data2XmlProcessor()
        now = datetime.now().replace(microsecond=0)
        source_items = [StatDataItem(13, 'category1', now, 'data1')]
        actual = processor.process(StatData((13, 13), source_items))
        expected = '<stat_data><category1><category1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></category1_item></category1></stat_data>'
        self.assertEquals(expected, actual)

    def test_several_category_data_item_process(self):
        processor = Data2XmlProcessor()
        now = datetime.now().replace(microsecond=0)
        source_items = [StatDataItem(13, 'category1', now, 'data1'), StatDataItem(14, 'category2', now, 'data2')]
        actual = processor.process(StatData((13, 14), source_items))
        expected = '<stat_data>' +\
                   '<category1><category1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></category1_item></category1>' +\
                   '<category2><category2_item><timemarker>' + str(now) + '</timemarker><data>data2</data></category2_item></category2>' +\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    def test_same_category_data_item_process(self):
        processor = Data2XmlProcessor()
        now = datetime.now().replace(microsecond=0)
        source_items = [StatDataItem(13, 'category1', now, 'data1'), StatDataItem(14, 'category1', now, 'data2')]
        actual = processor.process(StatData((13, 14), source_items))
        expected = '<stat_data>' +\
                   '<category1>' +\
                   '<category1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></category1_item>' +\
                   '<category1_item><timemarker>' + str(now) + '</timemarker><data>data2</data></category1_item>' +\
                   '</category1>' +\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    def test_complex_data_item_process(self):
        processor = Data2XmlProcessor()
        now = datetime.now().replace(microsecond=0)
        source_items = [StatDataItem(13, 'category1', now, 'data1'), StatDataItem(14, 'category2', now, 'data2'), StatDataItem(15, 'category1', now, 'data3')]
        actual = processor.process(StatData((13, 15), source_items))
        expected = '<stat_data>' +\
                   '<category1>' +\
                   '<category1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></category1_item>' +\
                   '<category1_item><timemarker>' + str(now) + '</timemarker><data>data3</data></category1_item>' +\
                   '</category1>' +\
                   '<category2><category2_item><timemarker>' + str(now) + '</timemarker><data>data2</data></category2_item></category2>' +\
                   '</stat_data>'
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
