from __future__ import unicode_literals
from unittest.case import TestCase
from src.common.state import State
from src.handler.aggregate_key_value_handler import AggregateKeyValueHandler

class TestAggregateKeyValueHandler(TestCase):

    def test_handle_known_key(self):
        state = State(None, None, {})
        self.assertEqual((True, State(None, None, {'key13': 1})), self._handler.process('key13=IDDQD', state))

    def test_handle_known_key_twice(self):
        state = State(None, None, {})
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, {'key13': 1})), result)
        result = self._handler.process('key13=IDKFA', result[1])
        self.assertEqual((True, State(None, None, {'key13': 2})), result)

    def test_handle_known_keys(self):
        state = State(None, None, {})
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, {'key13': 1})), result)
        result = self._handler.process('key666=IDKFA', result[1])
        self.assertEqual((True, State(None, None, {'key13': 1, 'key666': 1})), result)

    def test_handle_unknown_key(self):
        state = State(None, None, {})
        self.assertEqual((False, state), self._handler.process('key999=IDDQD', state))

    def test_handle_bad_data(self):
        state = State(None, None, {})
        self.assertEqual((False, state), self._handler.process('key666:IDDQD', state))

    def test_state_immutability(self):
        old_state = State(None, None, {'key13': 3})
        result = self._handler.process('key13=IDDQD', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)

    _handler = AggregateKeyValueHandler('=', ['key13', 'key666'], lambda key, state: key, lambda old_value, item: old_value + 1, 0)

__author__ = 'andrey.ushakov'
