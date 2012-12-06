from __future__ import unicode_literals
import unittest
from tests.unit_tests.storage.test_data_collector import TestDataCollector
from tests.unit_tests.task.test_simple_process_task import TestSimpleProcessTask
from tests.unit_tests.task.test_transform_process_task import TestTransformProcessTask
from tests.unit_tests.test_db_source_collect_task import TestDbSourceCollectTask
from tests.unit_tests.test_db_source_collector import TestDbSourceCollector

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataCollector))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimpleProcessTask))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTransformProcessTask))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDbSourceCollector))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDbSourceCollectTask))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
