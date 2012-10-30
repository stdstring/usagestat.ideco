from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.common.state import State
from stat_file_source.utils.standard_key_transformer import StandardKeyTransformer

class TestStandardKeyTransformer(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestStandardKeyTransformer, self).__init__(methodName)
        self._transformer = StandardKeyTransformer()

    def test_transform_with_state_id(self):
        self.assertEqual('category.key', self._transformer('key', State('category', 'category', {'key666': ['data']})))

    def test_transform_without_state_id(self):
        self.assertEqual('key', self._transformer('key', State(None, None, {'key666': ['data']})))

__author__ = 'andrey.ushakov'
