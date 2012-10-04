from __future__ import unicode_literals
from datetime import datetime
import unittest
from unittest.case import TestCase
from src.common.stat_data import StatDataItem, StatData
from src.data_processor.data2xml_processor import Data2XmlProcessor

class TestData2XmlProcessor(TestCase):

    def test_process_single_data_item(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1')]
        actual = self._processor.process(StatData((13, 13), source_items))
        expected = '<stat_data><some_source><category1><item><timemarker>' + str(self._now) + '</timemarker><data>data1</data></item></category1></some_source></stat_data>'
        self.assertEquals(expected, actual)

    def test_process_several_data_items(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source', 'category2', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items))
        expected = '<stat_data>' + \
                   '<some_source>' +\
                   '<category1><item><timemarker>' + str(self._now) + '</timemarker><data>data1</data></item></category1>' +\
                   '<category2><item><timemarker>' + str(self._now) + '</timemarker><data>data2</data></item></category2>' +\
                   '</some_source>'+\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    def test_process_same_category_data_items(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source', 'category1', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items))
        expected = '<stat_data>' +\
                   '<some_source>' +\
                   '<category1>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data1</data></item>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data2</data></item>' +\
                   '</category1>' +\
                   '</some_source>' +\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    def test_process_several_sources(self):
        source_items = [StatDataItem(13, 'some_source1', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source2', 'category1', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items))
        expected = '<stat_data>' +\
                   '<some_source1>' +\
                   '<category1><item><timemarker>' + str(self._now) + '</timemarker><data>data1</data></item></category1>' +\
                   '</some_source1>' +\
                   '<some_source2>' +\
                   '<category1><item><timemarker>' + str(self._now) + '</timemarker><data>data2</data></item></category1>' +\
                   '</some_source2>'+\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    def test_process_complex_data_items(self):
        source_items = [StatDataItem(13, 'some_source1', 'category1', self._now, 'data1'),
                        StatDataItem(14, 'some_source1','category2', self._now, 'data2'),
                        StatDataItem(15, 'some_source1','category1', self._now, 'data3'),
                        StatDataItem(16, 'some_source2','category2', self._now, 'data4'),
                        StatDataItem(17, 'some_source2','category1', self._now, 'data5'),
                        StatDataItem(18, 'some_source2','category2', self._now, 'data6')]
        actual = self._processor.process(StatData((13, 18), source_items))
        expected = '<stat_data>' +\
                   '<some_source1>' +\
                   '<category1>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data1</data></item>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data3</data></item>' +\
                   '</category1>' +\
                   '<category2><item><timemarker>' + str(self._now) + '</timemarker><data>data2</data></item></category2>' +\
                   '</some_source1>' +\
                   '<some_source2>' +\
                   '<category1><item><timemarker>' + str(self._now) + '</timemarker><data>data5</data></item></category1>' +\
                   '<category2>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data4</data></item>' +\
                   '<item><timemarker>' + str(self._now) + '</timemarker><data>data6</data></item>' +\
                   '</category2>' +\
                   '</some_source2>'+\
                   '</stat_data>'
        self.assertEquals(expected, actual)

    _processor = Data2XmlProcessor()
    _now = datetime.now().replace(microsecond=0)

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
