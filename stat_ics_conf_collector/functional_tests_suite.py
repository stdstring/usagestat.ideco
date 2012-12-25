from __future__ import unicode_literals
import unittest
from tests.test_collector import TestCollector

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCollector))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
