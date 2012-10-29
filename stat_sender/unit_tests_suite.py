from __future__ import unicode_literals
import unittest
from stat_sender_tests.unit_tests.common.test_logger_helper import TestLoggerHelper
from stat_sender_tests.unit_tests.common.test_unreliable_task_executer import TestUnreliableTaskExecuter
from stat_sender_tests.unit_tests.data_processor.test_data2xml_processor import TestData2XmlProcessor
from stat_sender_tests.unit_tests.data_processor.test_raw2data_processor import TestRaw2DataProcessor
from stat_sender_tests.unit_tests.test_stat_send_task import TestStatSendTask

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUnreliableTaskExecuter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestData2XmlProcessor))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestRaw2DataProcessor))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStatSendTask))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestLoggerHelper))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
