from __future__ import unicode_literals
from unittest.case import TestCase
import uuid
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem
from stat_server.entity.stat_data_packet import StatDataPacket

class TestStatDataPacket(TestCase):

    def test_str_for_single_item(self):
        items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')]
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), items)
        expected = 'StatDataPacket(user_id="83cf01c6-2284-11e2-9494-08002703af71", ' \
                   'items=[StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD")])'
        self.assertEqual(expected, str(source))

    def test_repr_for_single_item(self):
        items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')]
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), items)
        expected = 'StatDataPacket(user_id="83cf01c6-2284-11e2-9494-08002703af71", '\
                   'items=[StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD")])'
        self.assertEqual(expected, repr(source))

    def test_str_for_several_items(self):
        items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                 StatDataItem('source2', 'cat2', str_2_time('2013-01-01 11:11:11'), 'IDKFA')]
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), items)
        expected = 'StatDataPacket(user_id="83cf01c6-2284-11e2-9494-08002703af71", '\
                   'items=[StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD"),' \
                   'StatDataItem(source="source2", category="cat2", timemarker="2013-01-01 11:11:11", data="IDKFA")])'
        self.assertEqual(expected, str(source))

    def test_repr_for_several_items(self):
        items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                 StatDataItem('source2', 'cat2', str_2_time('2013-01-01 11:11:11'), 'IDKFA')]
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), items)
        expected = 'StatDataPacket(user_id="83cf01c6-2284-11e2-9494-08002703af71", '\
                   'items=[StatDataItem(source="source1", category="cat1", timemarker="2012-12-21 23:59:59", data="IDDQD"),'\
                   'StatDataItem(source="source2", category="cat2", timemarker="2013-01-01 11:11:11", data="IDKFA")])'
        self.assertEqual(expected, repr(source))

__author__ = 'andrey.ushakov'
