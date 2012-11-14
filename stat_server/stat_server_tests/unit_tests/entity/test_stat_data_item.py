from __future__ import unicode_literals
from unittest.case import TestCase
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem

class TestStatDataItem(TestCase):

    def test_str(self):
        source = StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')
        expected = 'StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD")'
        self.assertEqual(expected, str(source))

    def test_repr(self):
        source = StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')
        expected = 'StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD")'
        self.assertEqual(expected, repr(source))

__author__ = 'andrey.ushakov'
