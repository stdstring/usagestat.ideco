from __future__ import unicode_literals
import unittest
from stat_sender_tests.functional_tests.storage.test_sqlite_storage import TestSqliteStorage
from stat_sender_tests.functional_tests.user_identity.test_user_identity_provider import TestUserIdentityProvider

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSqliteStorage))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUserIdentityProvider))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
