from __future__ import unicode_literals
from datetime import datetime
import unittest
from unittest.case import TestCase
import uuid
from stat_sender.common.stat_data import StatDataItem, StatData
from stat_sender.data_processor.data2xml_processor import Data2XmlProcessor

class TestData2XmlProcessor(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestData2XmlProcessor, self).__init__(methodName)
        self._now = datetime.now().replace(microsecond=0)
        self._str_now = '{0:%Y-%m-%d %H:%M:%S}'.format(self._now)
        self._processor = Data2XmlProcessor()
        self._user_id = uuid.UUID('{11111111-2222-3333-4444-555555555555}')
        self._additional_params = {'user_id': self._user_id}

    def test_process_single_data_item(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1')]
        actual = self._processor.process(StatData((13, 13), source_items), **self._additional_params)
        expected = '<data_packet user_id="' + str(self._user_id) + '"><data_item><source>some_source</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item></data_packet>'
        self.assertEquals(expected, actual)

    def test_process_several_data_items(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source', 'category2', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items), **self._additional_params)
        expected = '<data_packet user_id="' + str(self._user_id) + '">' + \
                   '<data_item><source>some_source</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item>' +\
                   '<data_item><source>some_source</source><category>category2</category><timemarker>' + self._str_now + '</timemarker><data>data2</data></data_item>' +\
                   '</data_packet>'
        self.assertEquals(expected, actual)

    def test_process_same_category_data_items(self):
        source_items = [StatDataItem(13, 'some_source', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source', 'category1', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items), **self._additional_params)
        expected = '<data_packet user_id="' + str(self._user_id) + '">' +\
                   '<data_item><source>some_source</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item>' +\
                   '<data_item><source>some_source</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data2</data></data_item>' +\
                   '</data_packet>'
        self.assertEquals(expected, actual)

    def test_process_several_sources(self):
        source_items = [StatDataItem(13, 'some_source1', 'category1', self._now, 'data1'), StatDataItem(14, 'some_source2', 'category1', self._now, 'data2')]
        actual = self._processor.process(StatData((13, 14), source_items), **self._additional_params)
        expected = '<data_packet user_id="' + str(self._user_id) + '">' +\
                   '<data_item><source>some_source1</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item>' +\
                   '<data_item><source>some_source2</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data2</data></data_item>' +\
                   '</data_packet>'
        self.assertEquals(expected, actual)

    def test_process_complex_data_items(self):
        source_items = [StatDataItem(13, 'some_source1', 'category1', self._now, 'data1'),
                        StatDataItem(14, 'some_source1','category2', self._now, 'data2'),
                        StatDataItem(15, 'some_source1','category1', self._now, 'data3'),
                        StatDataItem(16, 'some_source2','category2', self._now, 'data4'),
                        StatDataItem(17, 'some_source2','category1', self._now, 'data5'),
                        StatDataItem(18, 'some_source2','category2', self._now, 'data6')]
        actual = self._processor.process(StatData((13, 18), source_items), **self._additional_params)
        expected = '<data_packet user_id="' + str(self._user_id) + '">' +\
                   '<data_item><source>some_source1</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item>' +\
                   '<data_item><source>some_source1</source><category>category2</category><timemarker>' + self._str_now + '</timemarker><data>data2</data></data_item>' +\
                   '<data_item><source>some_source1</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data3</data></data_item>' +\
                   '<data_item><source>some_source2</source><category>category2</category><timemarker>' + self._str_now + '</timemarker><data>data4</data></data_item>' +\
                   '<data_item><source>some_source2</source><category>category1</category><timemarker>' + self._str_now + '</timemarker><data>data5</data></data_item>' +\
                   '<data_item><source>some_source2</source><category>category2</category><timemarker>' + self._str_now + '</timemarker><data>data6</data></data_item>' +\
                   '</data_packet>'
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
