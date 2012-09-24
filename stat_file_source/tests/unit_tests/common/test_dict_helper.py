from __future__ import unicode_literals
from unittest.case import TestCase
from src.common.dict_helper import DictHelper

class TestDictHelper(TestCase):

    def test_get(self):
        source_dict = {'some_key': 'some_value'}
        self.assertEquals('some_value', DictHelper.get_or_create(source_dict, 'some_key', 'default_value'))
        self.assertDictEqual({'some_key': 'some_value'}, source_dict)

    def test_create(self):
        source_dict = {'some_key': 'some_value'}
        self.assertEquals('default_value', DictHelper.get_or_create(source_dict, 'other_key', 'default_value'))
        self.assertDictEqual({'some_key': 'some_value', 'other_key': 'default_value'}, source_dict)

__author__ = 'andrey.ushakov'
