from __future__ import unicode_literals
from collections import OrderedDict
from unittest.case import TestCase
from stat_file_source.handler.single_key_handler import SingleKeyHandler
from stat_file_source.common.state import State

class TestSingleKeyHandler(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSingleKeyHandler, self).__init__(methodName)
        key_transformer = lambda key, value, state: key
        self._handler = SingleKeyHandler.create_with_known_key_list('=', ['key13', 'key666'], key_transformer, '0')

    def test_handle_known_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((True, State(None, None, OrderedDict([('key13', '0')]))), self._handler.process('key13', state))

    def test_handle_known_key_twice(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', '0')]))), result)
        result = self._handler.process('key13', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', '0')]))), result)

    def test_handle_known_keys(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', '0')]))), result)
        result = self._handler.process('key666', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', '0'), ('key666', '0')]))), result)

    def test_handle_unknown_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key999', state))

    def test_handle_key_value_data(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key666=IDDQD', state))

    def test_state_immutability(self):
        old_state = State(None, None, OrderedDict([('key13', 'some_data')]))
        result = self._handler.process('key13', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)
        self.assertFalse(new_state.items is old_state.items)

__author__ = 'andrey.ushakov'
