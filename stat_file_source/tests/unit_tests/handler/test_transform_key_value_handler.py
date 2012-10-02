from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.common.state import State
from stat_file_source.handler.transform_key_value_handler import TransformKeyValueHandler

class TestTransformKeyValueHandler(TestCase):

    def test_handle_known_key(self):
        state = State(None, None, {})
        self.assertEqual((True, State(None, None, {'key13': ['__IDDQD__']})), self._handler.process('key13=IDDQD', state))

    def test_handle_known_key_twice(self):
        state = State(None, None, {})
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, {'key13': ['__IDDQD__']})), result)
        result = self._handler.process('key13=IDKFA', result[1])
        self.assertEqual((True, State(None, None, {'key13': ['__IDDQD__', '__IDKFA__']})), result)

    def test_handle_known_keys(self):
        state = State(None, None, {})
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, {'key13': ['__IDDQD__']})), result)
        result = self._handler.process('key666=IDKFA', result[1])
        self.assertEqual((True, State(None, None, {'key13': ['__IDDQD__'], 'key666': ['__IDKFA__']})), result)

    def test_handle_unknown_key(self):
        state = State(None, None, {})
        self.assertEqual((False, state), self._handler.process('key999=IDDQD', state))

    def test_handle_bad_data(self):
        state = State(None, None, {})
        self.assertEqual((False, state), self._handler.process('key666:IDDQD', state))

    def test_state_immutability(self):
        old_state = State(None, None, {'key13': ['__some_data__']})
        result = self._handler.process('key13=IDDQD', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)
        self.assertFalse(new_state.items is old_state.items)

    _handler = TransformKeyValueHandler.create_with_known_key_list('=', ['key13', 'key666'], lambda key, state: key, lambda value: '__' + str(value) + '__')

__author__ = 'andrey.ushakov'
