from __future__ import unicode_literals
from datetime import datetime, timedelta
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_file_source.file_source_collect_task import FileSourceCollectTask
from stat_file_source.filter.comment_filter import CommentFilter
from stat_file_source.filter.spaces_filter import SpacesFilter
from stat_file_source.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from stat_file_source.handler.simple_key_value_handler import SimpleKeyValueHandler
from stat_file_source.handler.standard_config_section_handler import StandardConfigSectionHandler
from stat_file_source.handler.transform_key_value_handler import TransformKeyValueHandler
from stat_file_source.utils.standard_key_transformer import StandardKeyTransformer
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
import sqlite_db_manager
sys.path.append(os.path.abspath('../stat_source_common/stat_source_common/entity'))
import data_item

# spec: str -> str
def transform_user_fun(source_value):
    delimiter_index = source_value.find(',')
    if delimiter_index == -1:
        return source_value
    else:
        user = source_value[0:delimiter_index]
        pwd = '*' * (len(source_value) - delimiter_index - 1)
        return '{user:s},{pwd:s}'.format(user=user, pwd=pwd)


class TestFileSourceCollectTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestFileSourceCollectTask, self).__init__(methodName)
        self._mox = None
        self._main_logger = None
        self._storage_logger = None
        self._collect_task = None
        self._db_manager = sqlite_db_manager.SqliteDbManager('../stat_sender_db')

    def setUp(self):
        self._mox = Mox()
        self._main_logger = self._mox.CreateMock(Logger)
        self._storage_logger = self._mox.CreateMock(Logger)
        source_filename = os.path.abspath('tests/functional_tests/test.conf')
        self._db_manager.__enter__()
        filters = [CommentFilter('#'), SpacesFilter()]
        standard_key_transformer = StandardKeyTransformer()
        ip_key_transformer = lambda key, state: '{category:s}.ip'.format(category=state.state_id)
        handlers = [StandardConfigSectionHandler(),
                    SimpleKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'services', standard_key_transformer),
                    TransformKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'users', standard_key_transformer, transform_user_fun),
                    AggregateKeyValueHandler.create_with_known_key_list('=', ['ip0', 'ip1', 'ip2', 'ip3', 'ip4'], ip_key_transformer, lambda old_value, item: old_value + 1, 0)]
        self._collect_task = FileSourceCollectTask('some_source', filters, handlers, source_filename, self._db_manager.db_filename, self._main_logger)

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_execute(self):
        data_list = [data_item.DataItem('wins.ip', 1),
                     data_item.DataItem('services.http', '80'),
                     data_item.DataItem('gate.ip', 3),
                     data_item.DataItem('users.user', 'ivanov,*******'),
                     data_item.DataItem('users.user', 'petrov,***'),
                     data_item.DataItem('users.user', 'sydorov,*********'),
                     data_item.DataItem('users.user', 'kozlov,*********'),
                     data_item.DataItem('dns.ip', 2),
                     data_item.DataItem('services.ftp', '21')]
        self._main_logger.getChild('sqlite_storage').AndReturn(self._storage_logger)
        self._main_logger.info('execute() enter')
        self._main_logger.info('_read_file_content() enter')
        self._main_logger.info('_read_file_content() exit')
        self._main_logger.info('_write_data(data_dict) enter')
        self._storage_logger.info('save_data(some_source, data_list) enter')
        for data in data_list:
            self._storage_logger.info('_save_item_impl(some_source, {0!s}) enter'.format(data))
            self._storage_logger.info('_save_item_impl(some_source, {0!s}) exit'.format(data))
        self._storage_logger.info('save_data(some_source, data_list) exit')
        self._main_logger.info('_write_data(data_dict) exit with result successfully')
        self._main_logger.info('execute() exit with result successfully')
        self._mox.ReplayAll()
        now = datetime.now()
        result = self._collect_task.execute()
        self.assertTrue(result)
        actual = self._db_manager.execute_query('select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID')
        expected = [('gate.ip', 3),
            ('dns.ip', 2),
            ('wins.ip', 1),
            ('users.user', 'ivanov,*******'),
            ('users.user', 'petrov,***'),
            ('users.user', 'sydorov,*********'),
            ('users.user', 'kozlov,*********'),
            ('services.http', '80'),
            ('services.ftp', '21')]
        self._check_data(now, 'some_source', expected, actual)
        self._mox.VerifyAll()

    # spec: datetime, str, [(str, str)], [(int, str, str, str, str)] -> None
    def _check_data(self, now, source_id, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for expected_item in expected:
            actual_items = filter(lambda item: item[1] == source_id and item[2] == expected_item[0] and item[4] == expected_item[1], actual)
            self.assertEqual(1, len(actual_items))
            actual_item = actual_items[0]
            actual_time = self._str_2_time(actual_item[3])
            self.assertTrue(actual_time - now < timedelta(seconds = 10))

    # spec: str -> datetime
    def _str_2_time(self, source_str):
        return datetime.strptime(source_str, '%Y-%m-%d %H:%M:%S')

__author__ = 'andrey.ushakov'
