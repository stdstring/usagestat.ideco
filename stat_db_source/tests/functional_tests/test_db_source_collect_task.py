from __future__ import unicode_literals
from datetime import datetime, timedelta
import logging
from unittest.case import TestCase
import psycopg2
from stat_db_funtest_utils import pg_db_manager, sqlite_db_manager
from stat_source_common.storage.sqlite_storage import SqliteStorage
from stat_db_source.db_source_collect_task import DbSourceCollectTask
from stat_db_source.task.collect_task import CollectTask
from stat_db_source.task.transform_process_task import TransformProcessTask

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
        #self._mox = None
        #self._main_logger = None

    def setUp(self):
        self._source_db_manager.__enter__()
        self._dest_db_manager.__enter__()
        self._now = datetime.now()
        #self._mox = Mox()
        #self._main_logger = self._mox.CreateMock(Logger)

    def tearDown(self):
        self._dest_db_manager.__exit__(None, None, None)
        self._source_db_manager.__exit__(None, None, None)

    def test(self):
        self._prepare_source_data()
        logger = logging.getLogger('test_db_source_collect_task')
        collect_task_list = [CollectTask(['select data_part1, data_part2, data_part3 from main_data_storage'],
            TransformProcessTask(lambda row: 'users_cat.{0:s}'.format(row[0]), lambda row: data_transformer(row)))]
        source_connection_factory = lambda: psycopg2.connect(self._source_db_manager.connection_string)
        dest_storage = SqliteStorage(self._dest_db_manager.connection_string)
        collect_task = DbSourceCollectTask(self._source_id, collect_task_list, source_connection_factory, dest_storage, logger)
        collect_task.execute()
        expected = [('users_cat.cat1', 'data1'),
            ('users_cat.cat2', 'data3'),
            ('users_cat.cat1', 'data4'),
            ('users_cat.cat1', 'data6'),
            ('users_cat.cat2', 'data8'),
            ('users_cat.cat3', '')]
        actual = self._dest_db_manager.execute_query('select ID, SOURCE, CATEGORY, TIMEMARKER, DATA from STAT_DATA')
        self._check_data(self._source_id, expected, actual)

    def _prepare_source_data(self):
        insert_query = 'insert into main_data_storage(user_id, data_part1, data_part2, data_part3) values(%s, %s, %s, %s)'
        user1 = '11111111-1111-1111-1111-111111111111'
        user2 = '22222222-2222-2222-2222-222222222222'
        user3 = '33333333-3333-3333-3333-333333333333'
        insert_data = [(user1, 'cat1', 'data1', 'data2'),
            (user1, 'cat2', None, 'data3'),
            (user2, 'cat1', 'data4', 'data5'),
            (user3, 'cat1', 'data6', 'data7'),
            (user3, 'cat2', None, 'data8'),
            (user3, 'cat3', None, None)]
        self._source_db_manager.execute_nonquery(insert_query, insert_data)

    # spec: [(str, str)], [(int, str, str, str, str)]
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
            self.assertEqual(expected_row[0], actual_row[2])
            # timemarker
            actual_now = datetime.strptime(actual_row[3], '%Y-%m-%d %H:%M:%S')
            self.assertTrue(actual_now - self._now < timedelta(seconds=10))
            # data
            self.assertEqual(expected_row[1], actual_row[4])
            index += 1

def data_transformer(row):
    if row[1] is not None:
        return row[1]
    if row[2] is not None:
        return row[2]
    return ''


__author__ = 'andrey.ushakov'
