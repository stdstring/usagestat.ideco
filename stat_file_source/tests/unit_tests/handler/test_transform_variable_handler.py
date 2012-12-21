from __future__ import unicode_literals
from collections import OrderedDict
from unittest.case import TestCase
from stat_file_source.handler.transform_variable_handler import TransformVariableHandler
from stat_file_source.common.state import State

class TestTransformVariableHandler(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestTransformVariableHandler, self).__init__(methodName)
        transform_fun = lambda data: int(data)
        self._handler = TransformVariableHandler.create_with_known_key_list('=', ['key13', 'key666'], lambda key, state: key, transform_fun, 0)

    def test_handle_known_key_with_value(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 666)]))), self._handler.process('key13=666', state))

    def test_handle_known_key_without_value(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 0)]))), self._handler.process('key13', state))

    def test_handle_known_key_multiple_times(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=666', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 666)]))), result)
        result = self._handler.process('key13', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 0)]))), result)
        result = self._handler.process('key13=999', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 999)]))), result)

    def test_handle_known_keys(self):
        state = State(None, None, OrderedDict())
        result = self._handler.process('key13=666', state)
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 666)]))), result)
        result = self._handler.process('key666', result[1])
        self.assertEqual((True, State(None, None, OrderedDict([('key13', 666), ('key666', 0)]))), result)

    def test_handle_unknown_key(self):
        state = State(None, None, OrderedDict())
        self.assertEqual((False, state), self._handler.process('key999=777', state))
        self.assertEqual((False, state), self._handler.process('key999', state))

    def test_state_immutability_processing_key_value(self):
        old_state = State(None, None, OrderedDict([('key13=999', 'some_data')]))
        result = self._handler.process('key13=888', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)
        self.assertFalse(new_state.items is old_state.items)

    def test_state_immutability_processing_single_key(self):
        old_state = State(None, None, OrderedDict([('key13', 'some_data')]))
        result = self._handler.process('key13=888', old_state)
        new_state = result[1]
        self.assertTrue(result[0])
        self.assertFalse(new_state is None)
        self.assertFalse(new_state is old_state)
        self.assertFalse(new_state.items is old_state.items)

__author__ = 'andrey.ushakov'
