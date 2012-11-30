from __future__ import unicode_literals
from datetime import datetime, timedelta
import logging
from mox import Mox
from unittest.case import TestCase
import psycopg2
from stat_db_funtest_utils import pg_db_manager, sqlite_db_manager
from stat_source_common.entity import data_item
from stat_source_common.storage.sqlite_storage import SqliteStorage
from stat_db_source.db_source_collect_task import DbSourceCollectTask
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.simple_process_task import SimpleProcessTask
from stat_db_source.task.transform_process_task import TransformProcessTask
from tests.functional_tests.test_custom_process_task import TestCustomProcessTask

class TestDbSourceCollectTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestDbSourceCollectTask, self).__init__(methodName)
        self._source_db_manager = pg_db_manager.PgDbManager(username='postgres',
            pwd='31415926',
            dbname='stat_db_source_test',
            create_script='tests/functional_tests/test_db_metadata.sql',
            clear_script='tests/functional_tests/test_db_clear.sql')
        self._dest_db_manager = sqlite_db_manager.SqliteDbManager(db_create_script_path='../stat_sender_db')
        self._now = datetime.now()
        self._source_id = 'test_db_source'
        self._mox = None
        self._main_logger = None
        self._db_source_collector_logger = None
        self._data_collector_logger = None
        self._collect_task_logger = None
        self._dest_storage_logger = None

    def setUp(self):
        self._source_db_manager.__enter__()
        self._dest_db_manager.__enter__()
        self._now = datetime.now()
        self._mox = Mox()
        self._main_logger = self._mox.CreateMock(logging.Logger)
        self._db_source_collector_logger = self._mox.CreateMock(logging.Logger)
        self._data_collector_logger = self._mox.CreateMock(logging.Logger)
        self._collect_task_logger = self._mox.CreateMock(logging.Logger)
        self._dest_storage_logger = self._mox.CreateMock(logging.Logger)

    def tearDown(self):
        self._dest_db_manager.__exit__(None, None, None)
        self._source_db_manager.__exit__(None, None, None)

    def test_simple_process_task(self):
        query_list = ["select 'users_cat.' || data_part1, data_part2 from main_data_storage where data_part2 is not null",
                      "select 'users_cat.' || data_part1, data_part3 from main_data_storage where data_part2 is null and data_part3 is not null"]
        expected_data_list = [data_item.DataItem('users_cat.cat1', 'data1'),
                              data_item.DataItem('users_cat.cat1', 'data4'),
                              data_item.DataItem('users_cat.cat1', 'data6'),
                              data_item.DataItem('users_cat.cat2', 'data3'),
                              data_item.DataItem('users_cat.cat2', 'data8')]
        collect_task_list = [CollectTask(query_list, SimpleProcessTask())]
        self._test_common_body(query_list, expected_data_list, collect_task_list)

    def test_transform_process_task(self):
        query_list = ['select data_part1, data_part2, data_part3 from main_data_storage']
        expected_data_list = [data_item.DataItem('users_cat.cat1', 'data1'),
                              data_item.DataItem('users_cat.cat2', 'data3'),
                              data_item.DataItem('users_cat.cat1', 'data4'),
                              data_item.DataItem('users_cat.cat1', 'data6'),
                              data_item.DataItem('users_cat.cat2', 'data8'),
                              data_item.DataItem('users_cat.cat3', '')]
        collect_task_list = [CollectTask(query_list, TransformProcessTask(lambda row: 'users_cat.{0:s}'.format(row[0]), lambda row: data_transformer(row)))]
        self._test_common_body(query_list, expected_data_list, collect_task_list)

    def test_custom_process_task(self):
        query_list = ['select user_id, data_part1, data_part2, data_part3 from main_data_storage',
                      'select user_id, user_data from user_data_storage']
        expected_data_list = [data_item.DataItem('users_cat.adminko.cat1', '-data1-'),
                              data_item.DataItem('users_cat.adminko.cat2', '-data3-'),
                              data_item.DataItem('users_cat.simple_user.cat1', '-data6-'),
                              data_item.DataItem('users_cat.simple_user.cat2', '-data8-'),
                              data_item.DataItem('users_cat.simple_user.cat3', '-empty-')]
        collect_task_list = [CollectTask(query_list, TestCustomProcessTask())]
        self._test_common_body(query_list, expected_data_list, collect_task_list)

    # spec: [str], [DataItem], [CollectTask] -> None
    def _test_common_body(self, query_list, expected_data_list, collect_task_list):
        self._prepare_source_data()
        self._create_logger_expectations(query_list, expected_data_list)
        self._mox.ReplayAll()
        source_connection_factory = lambda: psycopg2.connect(self._source_db_manager.connection_string)
        dest_storage_factory = lambda logger: SqliteStorage(self._dest_db_manager.connection_string, logger)
        collect_task = DbSourceCollectTask(self._source_id, collect_task_list, source_connection_factory, dest_storage_factory, self._main_logger)
        result = collect_task.execute()
        self.assertTrue(result)
        actual = self._dest_db_manager.execute_query('select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA')
        self._check_data(self._source_id, expected_data_list, actual)
        self._mox.VerifyAll()

    # spec: None -> None
    def _prepare_source_data(self):
        user1 = '11111111-1111-1111-1111-111111111111'
        user2 = '22222222-2222-2222-2222-222222222222'
        user3 = '33333333-3333-3333-3333-333333333333'
        insert_user_data_query = 'insert into user_data_storage(user_id, user_data) values(%s, %s)'
        user_data = [(user1, 'adminko'), (user3, 'simple_user')]
        self._source_db_manager.execute_nonquery(insert_user_data_query, user_data)
        insert_main_data_query = 'insert into main_data_storage(user_id, data_part1, data_part2, data_part3) values(%s, %s, %s, %s)'
        main_data = [(user1, 'cat1', 'data1', 'data2'),
            (user1, 'cat2', None, 'data3'),
            (user2, 'cat1', 'data4', 'data5'),
            (user3, 'cat1', 'data6', 'data7'),
            (user3, 'cat2', None, 'data8'),
            (user3, 'cat3', None, None)]
        self._source_db_manager.execute_nonquery(insert_main_data_query, main_data)

    # spec: [str], [DataItem] -> None
    def _create_logger_expectations(self, query_list, expected_data_list):
        self._main_logger.info('execute() enter')
        self._main_logger.getChild('db_source_collector').AndReturn(self._db_source_collector_logger)
        self._db_source_collector_logger.info('collect() enter')
        self._db_source_collector_logger.getChild('data_collector').AndReturn(self._data_collector_logger)
        self._data_collector_logger.info('collect_data(collect_task_list) enter')
        self._data_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._collect_task_logger.info('collect_data(query_executer) enter')
        for query in query_list:
            self._collect_task_logger.info('_collect_data_item({query:s}) enter'.format(query=query))
            self._collect_task_logger.info('_collect_data_item({query:s}) exit'.format(query=query))
        self._collect_task_logger.info('collect_data(query_executer) exit')
        self._data_collector_logger.info('collect_data(collect_task_list) exit')
        self._db_source_collector_logger.getChild('collect_task').AndReturn(self._collect_task_logger)
        self._db_source_collector_logger.getChild('dest_storage').AndReturn(self._dest_storage_logger)
        self._collect_task_logger.info('process_data() enter')
        self._collect_task_logger.info('process_data() exit')
        self._dest_storage_logger.info('save_data(test_db_source, data_list) enter')
        for expected_data_item in expected_data_list:
            self._dest_storage_logger.info('_save_item_impl(test_db_source, {data_item!s}) enter'.format(data_item=expected_data_item))
            self._dest_storage_logger.info('_save_item_impl(test_db_source, {data_item!s}) exit'.format(data_item=expected_data_item))
        self._dest_storage_logger.info('save_data(test_db_source, data_list) exit')
        self._db_source_collector_logger.info('collect() exit')
        self._main_logger.info('execute() exit')

    # spec: [DataItem], [(int, str, str, str, str)]
    def _check_data(self, source_id, expected, actual):
        self.assertEqual(len(expected), len(actual))
        index = 0
        while index < len(expected):
            expected_row = expected[index]
            actual_row = actual[index]
            # id
            self.assertTrue(actual_row[0] > 0)
            # source_id
            self.assertEqual(source_id, actual_row[1])
            # category
            self.assertEqual(expected_row.category, actual_row[2])
            # timemarker
            actual_now = datetime.strptime(actual_row[3], '%Y-%m-%d %H:%M:%S')
            self.assertTrue(actual_now - self._now < timedelta(seconds=10))
            # data
            self.assertEqual(expected_row.data, actual_row[4])
            index += 1

def data_transformer(row):
    if row[1] is not None:
        return '' + row[1]
    if row[2] is not None:
        return '' + row[2]
    return ''


__author__ = 'andrey.ushakov'
