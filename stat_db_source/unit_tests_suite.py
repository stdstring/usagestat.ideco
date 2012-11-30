from __future__ import unicode_literals
import unittest
from tests.unit_tests.storage.test_data_collector import TestDataCollector

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDataCollector))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
