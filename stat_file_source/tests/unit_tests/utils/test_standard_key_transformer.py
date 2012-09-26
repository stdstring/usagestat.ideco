from __future__ import unicode_literals
from unittest.case import TestCase
from src.common.state import State
from src.utils.standard_key_transformer import StandardKeyTransformer

class TestStandardKeyTransformer(TestCase):

    def test_transform_with_state_id(self):
        self.assertEqual('category.key', self._transformer('key', State('category', 'category', {'key666': ['data']})))

    def test_transform_without_state_id(self):
        self.assertEqual('key', self._transformer('key', State(None, None, {'key666': ['data']})))

    _transformer = StandardKeyTransformer()

__author__ = 'andrey.ushakov'
