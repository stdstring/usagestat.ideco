from __future__ import unicode_literals
from unittest.case import TestCase
import uuid
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem
from stat_server.entity.stat_data_packet import StatDataPacket
from stat_server.xml_serialization.xml_deserializer import XmlDeserializer
from stat_server_tests.common.stat_data_packet_checker import check_stat_data_packet

class TestXmlDeserializer(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestXmlDeserializer, self).__init__(methodName)
        self._deserializer = XmlDeserializer()

    def test_simple_object(self):
        source = '<simple_object><id>666</id><data>IDDQD</data></simple_object>'
        expected = TestXmlDeserializer.SimpleObject(666, 'IDDQD')
        actual = self._deserializer.deserialize(TestXmlDeserializer.SimpleObject, source)
        self._check_simple_object(expected, actual)

    def test_bad_simple_object_source(self):
        source = '<simple_object id="666"><data>IDDQD</data></simple_object>'
        self.assertRaises(TypeError, lambda: self._deserializer.deserialize(TestXmlDeserializer.SimpleObject, source))

    def test_data_packet_with_single_item(self):
        source = '<data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                 '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                 '</data_packet>'
        expected = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'),
            [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        actual = self._deserializer.deserialize(StatDataPacket, source)
        check_stat_data_packet(self, expected, actual)

    def test_data_packet_with_several_item(self):
        source = '<data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                 '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                 '<data_item><source>source2</source><category>cat2</category><timemarker>2013-01-01 11:11:11</timemarker><data>IDKFA</data></data_item>' +\
                 '</data_packet>'
        expected = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'),
            [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
             StatDataItem('source2', 'cat2', str_2_time('2013-01-01 11:11:11'), 'IDKFA')])
        actual = self._deserializer.deserialize(StatDataPacket, source)
        check_stat_data_packet(self, expected, actual)

    class SimpleObject(object):

        def __init__(self, id=None, data=None):
            self._id = id
            self._data = data

        @property
        def id(self):
            return self._id

        @id.setter
        def id(self, value):
            self._id = value

        @property
        def data(self):
            return self._data

        @data.setter
        def data(self, value):
            self._data = value

        @staticmethod
        def create(internal_repr):
            body = internal_repr['simple_object']
            id = int(body['id'][''])
            data = body['data']['']
            return TestXmlDeserializer.SimpleObject(id, data)

    def _check_simple_object(self, expected, actual):
        self.assertIsNotNone(actual)
        self.assertEqual(expected.id, actual.id)
        self.assertEqual(expected.data, actual.data)

__author__ = 'andrey.ushakov'
