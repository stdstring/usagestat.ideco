from __future__ import unicode_literals
from unittest.case import TestCase
from stat_sender.common import logger_helper

class TestLoggerHelper(TestCase):

    def test_bool_value(self):
        self.assertEqual('successfully', logger_helper.bool_result_to_str(True))
        self.assertEqual('fails', logger_helper.bool_result_to_str(False))

    def test_other_value(self):
        self.assertEqual('successfully', logger_helper.bool_result_to_str(['Item']))
        self.assertEqual('fails', logger_helper.bool_result_to_str([]))

__author__ = 'andrey.ushakov'
