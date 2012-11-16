from __future__ import unicode_literals
import unittest
from tests.functional_tests.storage.test_pg_storage_impl import TestPgStorageImpl

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPgStorageImpl))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
