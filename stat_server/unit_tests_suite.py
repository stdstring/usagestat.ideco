from __future__ import unicode_literals
import unittest
from stat_server_tests.unit_tests.entity.test_stat_data_item import TestStatDataItem
from stat_server_tests.unit_tests.entity.test_stat_data_packet import TestStatDataPacket
from stat_server_tests.unit_tests.test_stat_server_task import TestStatServerTask
from stat_server_tests.unit_tests.xml_serialization.test_xml_deserialization_helper import TestXmlDeserializationHelper
from stat_server_tests.unit_tests.xml_serialization.test_xml_deserializer import TestXmlDeserializer

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXmlDeserializer))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestXmlDeserializationHelper))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatServerTask))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatDataItem))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatDataPacket))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
