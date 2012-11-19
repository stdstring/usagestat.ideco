from __future__ import unicode_literals
from datetime import datetime, timedelta
import unittest
from unittest.case import TestCase
from stat_sender.common.stat_data import StatDataItem, StatData
from stat_sender.data_processor.raw2data_processor import Raw2DataProcessor
from tests.common.datetime_converters import datetime_2_str

class TestRaw2DataProcessor(TestCase):

    def test_processing(self):
        processor = Raw2DataProcessor()
        now = datetime.now()
        source = [(10, 'some_source1', 'cat1', datetime_2_str(now-timedelta(minutes=59)), 'some_data'),
            (11, 'some_source2', 'cat2', datetime_2_str(now-timedelta(hours=57)), 'some_data2'),
            (12, 'some_source1', 'cat1', datetime_2_str(now-timedelta(minutes=46)), 'some_data3')]
        expected_items = [StatDataItem(10, 'some_source1', 'cat1', (now-timedelta(minutes=59)).replace(microsecond=0), 'some_data'),
                          StatDataItem(11, 'some_source2', 'cat2', (now-timedelta(hours=57)).replace(microsecond=0), 'some_data2'),
                          StatDataItem(12, 'some_source1', 'cat1', (now-timedelta(minutes=46)).replace(microsecond=0), 'some_data3')]
        actual = processor.process(source)
        self.assertIsInstance(actual, StatData)
        self.assertEquals((10, 12), actual.id_range)
        self.assertEquals(expected_items, actual.stat_data_items)

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
