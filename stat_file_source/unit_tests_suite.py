from __future__ import unicode_literals
import unittest
from tests.unit_tests.filter.test_comment_filter import TestCommentFilter
from tests.unit_tests.filter.test_spaces_filter import TestSpacesFilter
from tests.unit_tests.handler.test_aggregate_key_value_handler import TestAggregateKeyValueHandler
from tests.unit_tests.handler.test_simple_key_list_handler import TestSimpleKeyListHandler
from tests.unit_tests.handler.test_simple_key_value_handler import TestSimpleKeyValueHandler
from tests.unit_tests.handler.test_simple_variable_handler import TestSimpleVariableHandler
from tests.unit_tests.handler.test_single_key_handler import TestSingleKeyHandler
from tests.unit_tests.handler.test_standard_config_section_handler import TestStandardConfigSectionHandler
from tests.unit_tests.handler.test_transform_key_list_handler import TestTransformKeyListHandler
from tests.unit_tests.handler.test_transform_key_value_handler import TestTransformKeyValueHandler
from tests.unit_tests.handler.test_transform_variable_handler import TestTransformVariableHandler
from tests.unit_tests.test_file_source_collect_task_impl import TestFileSourceCollectTaskImpl
from tests.unit_tests.test_file_source_collector import TestFileSourceCollector
from tests.unit_tests.utils.test_standard_key_transformer import TestStandardKeyTransformer

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCommentFilter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSpacesFilter))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAggregateKeyValueHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimpleKeyValueHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimpleKeyListHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStandardConfigSectionHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTransformKeyValueHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTransformKeyListHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSingleKeyHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSimpleVariableHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTransformVariableHandler))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestStandardKeyTransformer))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileSourceCollector))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileSourceCollectTaskImpl))
    return suite

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
