from __future__ import unicode_literals
import os
from unittest.case import TestCase
from stat_db_funtest_utils import sqlite_db_manager
from stat_ics_conf_collector import settings, collector_entry_point

class TestCollector(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCollector, self).__init__(methodName)
        self._db_manager = sqlite_db_manager.SqliteDbManager('../stat_sender_db')
        settings.DEST_DB_CONN_STR = self._db_manager.connection_string

    def setUp(self):
        self._db_manager.__enter__()

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_on_real_ics_conf(self):
        ics_conf_source = os.path.abspath('tests/ics.conf')
        # without CLAM4WEB_ENABLED, CLAM4MAIL_ENABLED, BA_ON, DLP_ICQ_ENABLED, FTP_ENABLED, WINS_ENABLED
        expected = [('net_type.Ethernet', 2),
            ('net_type.OpenVPN', 1),
            ('net_type.', 2),
            ('antivirus.KAV.WEB', 'disabled'),
            ('antivirus.KAV.MAIL', 'disabled'),
            ('antivirus.ClamAV.WEB', 'disabled'),
            ('antivirus.ClamAV.MAIL', 'disabled'),
            ('firewall.BA', 'disabled'),
            ('dlp.WEB', 'disabled'),
            ('dlp.MAIL', 'disabled'),
            ('dlp.ICQ', 'disabled'),
            ('mail.POSTFIX', 'enabled'),
            ('mail.POP3', 'enabled'),
            ('mail.IMAP', 'enabled'),
            ('mail.FETCHMAIL', 'disabled'),
            ('mail.WEBMAIL.External', 'enabled'),
            ('mail.WEBMAIL.Local', 'enabled'),
            ('antispam.KSP.MAIL', 'enabled'),
            ('antispam.DSPAM', 'disabled'),
            ('server.WEB', 'enabled'),
            ('server.FTP', 'disabled'),
            ('server.JABBER', 'disabled'),
            ('server.PPTP', 'enabled'),
            ('server.DHCP', 'disabled'),
            ('server.WINS', 'disabled'),
            ('server.SNMP', 'enabled'),
            ('server.DNS', 'enabled')]
        self._test_common_body(ics_conf_source, expected)

    def _test_common_body(self, ics_conf, expected):
        settings.ICS_CONF_SOURCE = ics_conf
        collect_result = collector_entry_point.execute()
        self.assertTrue(collect_result)
        actual = self._db_manager.execute_query('SELECT * FROM STAT_DATA')
        self._check_data('ics.conf', expected, actual)
        self._db_manager.execute_nonquery('DELETE FROM STAT_DATA')

    # spec: str, [(str, str)], [(int, str, str, str, str)] -> None
    def _check_data(self, source_id, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for expected_row in expected:
            actual_row = self._get_actual_row(expected_row, actual)
            self.assertIsNotNone(actual_row)
            self.assertEqual(source_id, actual_row[1])

    # spec: str, (str, str), [(int, str, str, str, str)] -> (int, str, str, str, str)
    def _get_actual_row(self, expected_row, actual_rows):
        expected_category = expected_row[0]
        expected_data = expected_row[1]
        find_result = filter(lambda (id, source_id, category, timemarker, data): category == expected_category and data == expected_data, actual_rows)
        if len(find_result) == 1:
            return find_result[0]
        raise KeyError("row with category = '{0:s}', data = '{1!s}' not found".format(expected_row[0], expected_row[1]))

__author__ = 'andrey.ushakov'