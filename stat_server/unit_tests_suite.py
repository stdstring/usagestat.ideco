from __future__ import unicode_literals
import unittest
from tests.unit_tests.entity.test_stat_data_item import TestStatDataItem
from tests.unit_tests.entity.test_stat_data_packet import TestStatDataPacket
from tests.unit_tests.handler.test_collect_handler_impl import TestCollectHandlerImpl
from tests.unit_tests.xml_serialization.test_xml_deserialization_helper import TestXmlDeserializationHelper
from tests.unit_tests.xml_serialization.test_xml_deserializer import TestXmlDeserializer

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXmlDeserializer))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXmlDeserializationHelper))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCollectHandlerImpl))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatDataItem))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatDataPacket))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
