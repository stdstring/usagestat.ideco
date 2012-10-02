from __future__ import unicode_literals
from unittest.case import TestCase
from stat_file_source.common.logger_helper import LoggerHelper

class TestLoggerHelper(TestCase):

    def test_bool_value(self):
        self.assertEqual('successfully', LoggerHelper.bool_result_to_str(True))
        self.assertEqual('fails', LoggerHelper.bool_result_to_str(False))

    def test_other_value(self):
        self.assertEqual('successfully', LoggerHelper.bool_result_to_str(['Item']))
        self.assertEqual('fails', LoggerHelper.bool_result_to_str([]))

__author__ = 'andrey.ushakov'
