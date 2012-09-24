from __future__ import unicode_literals
import unittest
from tests.unit_tests.common.test_dict_helper import TestDictHelper
from tests.unit_tests.filter.test_comment_filter import TestCommentFilter
from tests.unit_tests.filter.test_spaces_filter import TestSpacesFilter

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDictHelper))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommentFilter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSpacesFilter))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
