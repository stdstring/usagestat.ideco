from __future__ import unicode_literals
from collections import OrderedDict
from unittest.case import TestCase
from stat_file_source.common.state import State
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler

class TestAggregateKeyValueHandler(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestAggregateKeyValueHandler, self).__init__(methodName)
        key_transformer = lambda key, value, state: key
        aggregate_fun = lambda old_value, item: old_value + 1
        self._handler = AggregateKeyValueHandler.create_with_known_key_list('=', ['key13', 'key666'], key_transformer, aggregate_fun, 0)

    def test_handle_known_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 1)]))), self._handler.process('key13=IDDQD', state))

    def test_handle_known_key_twice(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 1)]))), result)
        result = self._handler.process('key13=IDKFA', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 2)]))), result)

    def test_handle_known_keys(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=IDDQD', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 1)]))), result)
        result = self._handler.process('key666=IDKFA', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 1), ('key666', 1)]))), result)

    def test_handle_unknown_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key999=IDDQD', state))

    def test_handle_bad_data(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key666:IDDQD', state))

    def test_state_immutability(self):
        old_state = State(None, None, OrderedDict([('key13', 3)]))
        result = self._handler.process('key13=IDDQD', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)

    def test_handle_aggegate_by_one_key(self):
        key_transformer = lambda key, value, state: 'ip'
        aggregate_fun = lambda old_value, item: old_value + 1
        handler = AggregateKeyValueHandler.create_with_known_key_list('=', ['ip0', 'ip1', 'ip2', 'ip3', 'ip4'], key_transformer, aggregate_fun, 0)
        state = State(None, None, {})
        result = handler.process('ip0=192.168.0.1', state)
        self.assertEqual((True, State(None, None, OrderedDict({'ip': 1}))), result)
        result = handler.process('ip1=192.168.1.1', result[1])
        self.assertEqual((True, State(None, None, OrderedDict({'ip': 2}))), result)
        result = handler.process('ip2=192.168.5.1', result[1])
        self.assertEqual((True, State(None, None, OrderedDict({'ip': 3}))), result)
        result = handler.process('ip9=192.168.5.5', result[1])
        self.assertEqual((False, State(None, None, OrderedDict({'ip': 3}))), result)

__author__ = 'andrey.ushakov'
