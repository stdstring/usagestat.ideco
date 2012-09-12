from __future__ import unicode_literals
from datetime import datetime, timedelta
import unittest
from unittest.case import TestCase
from common.stat_data import StatDataItem, StatData
from data_processor.raw2data_processor import Raw2DataProcessor

class TestRaw2DataProcessor(TestCase):

    def test_processing(self):
        processor = Raw2DataProcessor()
        now = datetime.now()
        source = [(10, 'cat1', now-timedelta(minutes=59), 'sone_data'),
            (11, 'cat2', now-timedelta(hours=57), 'sone_data2'),
            (12, 'cat1', now-timedelta(minutes=46), 'sone_data3')]
        expected_items = [StatDataItem(10, 'cat1', now-timedelta(minutes=59), 'sone_data'),
                          StatDataItem(11, 'cat2', now-timedelta(hours=57), 'sone_data2'),
                          StatDataItem(12, 'cat1', now-timedelta(minutes=46), 'sone_data3')]
        actual = processor.process(source)
        self.assertIsInstance(actual, StatData)
        self.assertEquals((10, 12), actual.id_range)
        self.assertEquals(expected_items, actual.stat_data_items)

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
