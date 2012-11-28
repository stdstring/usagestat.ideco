from __future__ import unicode_literals
import unittest
from tests.functional_tests.test_db_source_collect_task import TestDbSourceCollectTask

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDbSourceCollectTask))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
