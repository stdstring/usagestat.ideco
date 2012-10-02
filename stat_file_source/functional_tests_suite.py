from __future__ import unicode_literals
import unittest
from tests.functional_tests.test_file_source_collect_task import TestFileSourceCollectTask

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileSourceCollectTask))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andret.ushakov'
