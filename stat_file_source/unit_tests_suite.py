from __future__ import unicode_literals
import unittest
from tests.unit_tests.common.test_dict_helper import TestDictHelper

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDictHelper))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
