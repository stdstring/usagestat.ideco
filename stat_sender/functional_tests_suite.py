from __future__ import unicode_literals
import unittest
from tests.functional_tests.storage.test_sqlite_storage_impl import TestSqliteStorageImpl
from tests.functional_tests.test_settings import TestSettings

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSqliteStorageImpl))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSettings))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
