from __future__ import unicode_literals
from collections import OrderedDict
from unittest.case import TestCase
from stat_file_source.common.state import State
from stat_file_source.handler.simple_key_value_handler import SimpleKeyValueHandler

class TestSimpleKeyValueHandler(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestSimpleKeyValueHandler, self).__init__(methodName)
        self._handler = SimpleKeyValueHandler.create_with_known_key_list('=', ['key13', 'key666'], lambda key, state: key)

    def test_handle_known_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 'IDDQD')]))), self._handler.process('key13=IDDQD', state))

    def test_handle_known_key_twice(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 'IDDQD')]))), result)
        result = self._handler.process('key13=IDKFA', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 'IDKFA')]))), result)

    def test_handle_known_keys(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 'IDDQD')]))), result)
        result = self._handler.process('key666=IDKFA', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 'IDDQD'), ('key666', 'IDKFA')]))), result)

    def test_handle_unknown_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key999=IDDQD', state))

    def test_handle_bad_data(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key666:IDDQD', state))

    def test_state_immutability(self):
        old_state = State(None, None, OrderedDict([('key13', 'some_data')]))
        result = self._handler.process('key13=IDDQD', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)
        self.assertFalse(new_state.items is old_state.items)

__author__ = 'andrey.ushakov'
