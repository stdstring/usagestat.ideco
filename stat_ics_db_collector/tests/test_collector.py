from __future__ import unicode_literals
import os
import stat
import shutil
from unittest.case import TestCase
import kinterbasdb
from stat_db_funtest_utils import sqlite_db_manager
from stat_ics_db_collector import settings, collector_entry_point

# TODO (aushakov) : move 2 stat_db_funtest_utils
class BadFirebirdDbManager:

    def __init__(self, source_location, dest_location, conn_str):
        self._source_location = source_location
        self._dest_location = dest_location
        self._conn_str = conn_str

    def __enter__(self):
        shutil.copy(self._source_location, self._dest_location)
        mode = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
        os.chmod(self._dest_location, mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.unlink(self._dest_location)
        return True

    def execute_query(self, query, params=None):
        conn = kinterbasdb.connect(**self._conn_str)
        try:
            cursor = conn.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

    def execute_non_query(self, query, params=None):
        conn = kinterbasdb.connect(**self._conn_str)
        try:
            cursor = conn.cursor()
            if params is None:
                cursor.execute(query)
            else:
                cursor.executemany(query, params)
            conn.commit()
        finally:
            conn.close()

class TestCollector(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestCollector, self).__init__(methodName)
        # source db
        settings.ICS_DB_CONN_STR = {'host': str('localhost'),
                                    'database': str('/tmp/ics_main.gdb'),
                                    'user': str('SYSDBA'),
                                    'password': str('masterkey')}
        source_location = os.path.abspath('tests/ics_main.gdb')
        self._source_db_manager = BadFirebirdDbManager(source_location, '/tmp/ics_main.gdb', settings.ICS_DB_CONN_STR)
        # dest db
        self._dest_db_manager = sqlite_db_manager.SqliteDbManager('../stat_sender_db')
        settings.DEST_DB_CONN_STR = self._dest_db_manager.connection_string
        settings.LOG_CONF['handlers'] = {'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'default'}}
        settings.LOG_CONF['loggers'] = {'stat_ics_conf_collector.entry_point': {'handlers': ['console'], 'level': 'INFO', 'propagate': True}}

    def setUp(self):
        self._source_db_manager.__enter__()
        self._dest_db_manager.__enter__()

    def tearDown(self):
        self._dest_db_manager.__exit__(None, None, None)
        self._source_db_manager.__exit__(None, None, None)

    def test_on_ics_db_with_test_data(self):
        base_expected_data = [('users.EndUserCount', 9),
            ('users.EndUserWithAgentAuthCount', 4),
            ('ad.ADSync', 'enabled'),
            ('ad.EndUserCount', 2)]
        lic_data = list(base_expected_data)
        lic_data.append(('license.Type', 'Trial'))
        self._test_common_body(lambda: self._prepare_data(None), lic_data)
        lic_data = list(base_expected_data)
        lic_data.append(('license.Type', 'Standard Named'))
        self._test_common_body(lambda: self._prepare_data(4), lic_data)
        lic_data = list(base_expected_data)
        lic_data.append(('license.Type', 'Enterprise Named'))
        self._test_common_body(lambda: self._prepare_data(5), lic_data)
        lic_data = list(base_expected_data)
        lic_data.append(('license.Type', 'Standard Concurrent'))
        self._test_common_body(lambda: self._prepare_data(6), lic_data)
        lic_data = list(base_expected_data)
        lic_data.append(('license.Type', 'Enterprise Concurrent'))
        self._test_common_body(lambda: self._prepare_data(7), lic_data)

    def test_on_ics_db_with_test_data_and_wrong_license(self):
        self._prepare_data(666)
        result = collector_entry_point.execute()
        self.assertFalse(result)

    def _test_common_body(self, prepare_fun, expected_data):
        prepare_fun()
        result = collector_entry_point.execute()
        self.assertTrue(result)
        actual = self._dest_db_manager.execute_query('SELECT * FROM STAT_DATA')
        self._check_data('ics.db', expected_data, actual)
        self._dest_db_manager.execute_nonquery('DELETE FROM STAT_DATA')


    def _prepare_data(self, reg_ver=None):
        self._source_db_manager.execute_non_query('DELETE FROM REG')
        # ID, REG_VER
        reg_data = [(1, reg_ver)]
        insert_reg_query = 'INSERT INTO REG(ID, REG_VER) VALUES(?, ?)'
        self._source_db_manager.execute_non_query(insert_reg_query, reg_data)
        self._source_db_manager.execute_non_query('DELETE FROM USERS')
        # ID, PARID, EMAIL, LOGIN, ENABLED, DELETED, END_USER, SERVER, AUTH_TYPE, AD_IS
        user_data = [(1, None, 'root@gmail.com', 'root', 1, 0, 0, 0, None, 0),
            (2, 1, 'subroot@gmail.com', 'subroot', 1, 0, 0, 0, None, 0),
            (3, 1, 'subroot_ad@gmail.com', 'subroot_ad', 1, 0, 0, 0, None, 1),
            (400, 2, 'ivanoff66@gmail.com', 'ivanoff66', 1, 0, 1, 0, 1, 0),
            (401, 2, 'petroff77@gmail.com', 'petroff66', 0, 0, 1, 0, 1, 0),
            (402, 2, 'sidoroff66@gmail.com', 'sidoroff88', 1, 1, 1, 0, 1, 0),
            (403, 2, 'kozlov74@gmail.com', 'kozlov74', 1, 0, 1, 0, 2, 0),
            (404, 2, 'petuhov76@gmail.com', 'petuhov76', 0, 0, 1, 0, 2, 0),
            (405, 2, 'bobrov81@gmail.com', 'bobrov81', 1, 1, 1, 0, 2, 0),
            (406, 2, 'berezko83@gmail.com', 'berezko83', 1, 0, 1, 0, 3, 0),
            (407, 2, 'osinko84@gmail.com', 'osinko84', 0, 0, 1, 0, 3, 0),
            (408, 2, 'dub85@gmail.com', 'dub85', 1, 1, 1, 0, 3, 0),
            (410, 2, '', 'web-server', 1, 0, 0, 1, 1, 0),
            (411, 2, '', 'ftp-server', 0, 0, 0, 1, 1, 0),
            (412, 2, '', 'jabber-server', 1, 1, 0, 1, 1, 0),
            (500, 3, 'ctulhu666@gmail.com', 'ctulhu666', 1, 0, 1, 0, 1, 1),
            (501, 3, 'shambler99@gmail.com', 'shambler99', 0, 0, 1, 0, 1, 1),
            (502, 3, 'kiberdemon 777@gmail.com', 'kiberdemon 777', 1, 1, 1, 0, 1, 1),
            (504, 3, 'kakodemon13@gmail.com', 'kakodemon13', 1, 0, 1, 0, 1, 0)]
        insert_user_query = 'INSERT INTO USERS(ID, PARID, EMAIL, LOGIN, ENABLED, DELETED, END_USER, SERVER, AUTH_TYPE, AD_IS) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        self._source_db_manager.execute_non_query(insert_user_query, user_data)

    # TODO (aushakov) : move 2 stat_db_funtest_utils
    # spec: str, [(str, str)], [(int, str, str, str, str)] -> None
    def _check_data(self, source_id, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for expected_row in expected:
            actual_row = self._get_actual_row(expected_row, actual)
            self.assertIsNotNone(actual_row)
            self.assertEqual(source_id, actual_row[1])

    # TODO (aushakov) : move 2 stat_db_funtest_utils
    # spec: str, (str, str), [(int, str, str, str, str)] -> (int, str, str, str, str)
    def _get_actual_row(self, expected_row, actual_rows):
        expected_category = expected_row[0]
        expected_data = expected_row[1]
        find_result = filter(lambda (id, source_id, category, timemarker, data): category == expected_category and data == expected_data, actual_rows)
        if len(find_result) == 1:
            return find_result[0]
        raise KeyError("row with category = '{0:s}', data = '{1!s}' not found".format(expected_row[0], expected_row[1]))

__author__ = 'andrey.ushakov'
