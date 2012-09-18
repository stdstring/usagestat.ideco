from __future__ import unicode_literals
import os
from unittest.case import TestCase
from src.settings import Settings

class TestSettings(TestCase):

    def setUp(self):
        self._default_conf_file = Settings._main_conf_file
        Settings._main_conf_file = self._test_conf_file

    def tearDown(self):
        Settings._main_conf_file = self._default_conf_file

    def test_settings(self):
        self.assertEquals('/home/some_user/stat_sender/usage_stat.db', Settings.get_db_file())
        self.assertEquals('https://stat_sender_server/collect', Settings.get_remote_host())
        self.assertEquals('/home/some_user/stat_sender/key_file.key', Settings.get_key_file())
        self.assertEquals('/home/some_user/stat_sender/cert_file.cert', Settings.get_cert_file())
        self.assertEquals(666, Settings.get_send_attempt_count())
        self.assertEquals('/home/some_user/stat_sender/log.conf', Settings.get_log_conf())

    _default_conf_file = None
    _test_conf_file = 'tests/functional_tests/test_stat_sender.conf'

__author__ = 'andrey.ushakov'
