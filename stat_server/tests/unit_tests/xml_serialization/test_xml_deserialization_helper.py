from __future__ import unicode_literals
from unittest.case import TestCase
from stat_server.xml_serialization.xml_deserializer import XmlDeserializationHelper

class TestXmlDeserializationHelper(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestXmlDeserializationHelper, self).__init__(methodName)
        self._deserialization_helper = XmlDeserializationHelper()

    def test_simple_source_without_attrs(self):
        source = '<outer><id>666</id><data>IDDQD</data><inner><user_id>xxx-yyy-zzz</user_id><user_data>IDKFA</user_data></inner></outer>'
        expected = {'outer': {'id': {'': '666'}, 'data': {'': 'IDDQD'}, 'inner': {'user_id': {'': 'xxx-yyy-zzz'}, 'user_data': {'': 'IDKFA'}}}}
        actual = self._deserialization_helper.deserialize(source)
        self.assertEqual(expected, actual)

    def test_simple_source_with_attrs(self):
        source = '<outer id="666"><data>IDDQD</data><inner user_id = "xxx-yyy-zzz"><user_data>IDKFA</user_data></inner></outer>'
        expected = {'outer': {'id': '666', 'data': {'': 'IDDQD'}, 'inner': {'user_id': 'xxx-yyy-zzz', 'user_data': {'': 'IDKFA'}}}}
        actual = self._deserialization_helper.deserialize(source)
        self.assertEqual(expected, actual)

    def test_source_with_objects(self):
        source = '<objects><object id="1"><data>IDDQD</data></object><object id="2"><data>IDKFA</data></object></objects>'
        expected = {'objects': {'object': [{'id': '1', 'data': {'': 'IDDQD'}}, {'id': '2', 'data': {'': 'IDKFA'}}]}}
        actual = self._deserialization_helper.deserialize(source)
        self.assertEqual(expected, actual)

    def test_real_case_with_single_item(self):
        source = '<data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                 '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                 '</data_packet>'
        expected = {'data_packet': {'user_id': '83cf01c6-2284-11e2-9494-08002703af71', 'data_item': {'source': {'': 'source1'}, 'category': {'': 'cat1'}, 'timemarker': {'': '2012-12-21 23:59:59'}, 'data': {'': 'IDDQD'}}}}
        actual = self._deserialization_helper.deserialize(source)
        self.assertEqual(expected, actual)

    def test_real_case_with_several_items(self):
        source = '<data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                 '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                 '<data_item><source>source2</source><category>cat2</category><timemarker>2013-01-01 11:11:11</timemarker><data>IDKFA</data></data_item>' +\
                 '</data_packet>'
        expected = {'data_packet': {'user_id': '83cf01c6-2284-11e2-9494-08002703af71', 'data_item': [{'source': {'': 'source1'}, 'category': {'': 'cat1'}, 'timemarker': {'': '2012-12-21 23:59:59'}, 'data': {'': 'IDDQD'}}, {'source': {'': 'source2'}, 'category': {'': 'cat2'}, 'timemarker': {'': '2013-01-01 11:11:11'}, 'data': {'': 'IDKFA'}}]}}
        actual = self._deserialization_helper.deserialize(source)
        self.assertEqual(expected, actual)

__author__ = 'andrey.ushakov'
