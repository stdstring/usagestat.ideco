from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.common.state import State
from stat_file_source.handler.standard_config_section_handler import StandardConfigSectionHandler

class TestStandardConfigSectionHandler(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestStandardConfigSectionHandler, self).__init__(methodName)
        self._handler = StandardConfigSectionHandler()

    def test_handle_section(self):
        state = State(None, None, {})
        self.assertEqual((True, State('some section', 'some section', {})), self._handler.process('[some section]', state))

    def test_handle_additional_open_brackets(self):
        state = State(None, None, {})
        self.assertEqual((True, State('[s[o[m[e[ section', '[s[o[m[e[ section', {})), self._handler.process('[[s[o[m[e[ section]', state))

    def test_handle_additional_close_brackets(self):
        state = State(None, None, {})
        self.assertEqual((True, State('some ]s]e]c]t]i]o]n]', 'some ]s]e]c]t]i]o]n]', {})), self._handler.process('[some ]s]e]c]t]i]o]n]]', state))

    def test_handle_different_sections(self):
        state = State(None, None, {})
        result = self._handler.process('[some section]', state)
        self.assertEqual((True, State('some section', 'some section', {})), result)
        result = self._handler.process('[some other section]', result[1])
        self.assertEqual((True, State('some other section', 'some other section', {})), result)

    def test_handle_bad_data(self):
        state = State(None, None, {})
        self.assertEqual((False, state), self._handler.process('some arbitrary data', state))

__author__ = 'andrey.ushakov'
