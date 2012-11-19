from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
import uuid
from psycopg2._psycopg import DataError, IntegrityError
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem
from stat_server.entity.stat_data_packet import StatDataPacket
from stat_server.storage.pg_storage_impl import PgStorageImpl
# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
import pg_db_manager

class TestPgStorageImpl(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestPgStorageImpl, self).__init__(methodName)
        self._db_manager = pg_db_manager.PgDbManager('postgres', '31415926')
        self._query = 'select id, user_id, source, category, timemarker, data from stat_storage order by id asc'
        self._mox = None
        self._logger = None

    def setUp(self):
        self._db_manager.__enter__()
        self._mox = Mox()
        self._logger = self._mox.CreateMock(Logger)

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_save_single_item_data(self):
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'),
            [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        expected = [('83cf01c6-2284-11e2-9494-08002703af71', 'source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')]
        self._set_logger_when_normal('83cf01c6-2284-11e2-9494-08002703af71', source.items)
        self._test_common_body([source], expected)

    def test_save_several_items_data(self):
        items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                 StatDataItem('source2', 'cat2', str_2_time('2013-01-01 11:12:13'), 'IDKFA')]
        source = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), items)
        expected = [('83cf01c6-2284-11e2-9494-08002703af71', 'source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                    ('83cf01c6-2284-11e2-9494-08002703af71', 'source2', 'cat2', str_2_time('2013-01-01 11:12:13'), 'IDKFA')]
        self._set_logger_when_normal('83cf01c6-2284-11e2-9494-08002703af71', source.items)
        self._test_common_body([source], expected)

    def test_save_data_from_different_users(self):
        source1 = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'),
            [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        source2 = StatDataPacket(uuid.UUID('a5ab1a21-0731-4eff-9206-26de85f81970'),
            [StatDataItem('source1', 'cat1', str_2_time('2013-01-01 11:12:13'), 'IDKFA')])
        expected = [('83cf01c6-2284-11e2-9494-08002703af71', 'source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                    ('a5ab1a21-0731-4eff-9206-26de85f81970', 'source1', 'cat1', str_2_time('2013-01-01 11:12:13'), 'IDKFA')]
        self._set_logger_when_normal('83cf01c6-2284-11e2-9494-08002703af71', source1.items)
        self._set_logger_when_normal('a5ab1a21-0731-4eff-9206-26de85f81970', source2.items)
        self._test_common_body([source1, source2], expected)

    def test_bad_user_id(self):
        source = StatDataPacket('xxx-yyy-zzz', [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        self._set_logger_when_exception('xxx-yyy-zzz', source.items[0])
        self._test_common_body_with_exception(source, DataError)

    def test_none_user_id(self):
        source = StatDataPacket(None, [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        self._set_logger_when_exception(None, source.items[0])
        self._test_common_body_with_exception(source, DataError)

    def test_none_source(self):
        source = StatDataPacket('83cf01c6-2284-11e2-9494-08002703af71',
            [StatDataItem(None, 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        self._set_logger_when_exception('83cf01c6-2284-11e2-9494-08002703af71', source.items[0])
        self._test_common_body_with_exception(source, IntegrityError)

    def test_none_category(self):
        source = StatDataPacket('83cf01c6-2284-11e2-9494-08002703af71',
            [StatDataItem('source1', None, str_2_time('2012-12-21 23:59:59'), 'IDDQD')])
        self._set_logger_when_exception('83cf01c6-2284-11e2-9494-08002703af71', source.items[0])
        self._test_common_body_with_exception(source, IntegrityError)

    def test_none_timemarker(self):
        source = StatDataPacket('83cf01c6-2284-11e2-9494-08002703af71',
                [StatDataItem('source1', 'cat1', None, 'IDDQD')])
        self._logger.info('save_data(data) enter')
        self._logger.exception('exception in save_data(data)')
        self._test_common_body_with_exception(source, ValueError)

    def test_none_data(self):
        source = StatDataPacket('83cf01c6-2284-11e2-9494-08002703af71',
            [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), None)])
        self._set_logger_when_exception('83cf01c6-2284-11e2-9494-08002703af71', source.items[0])
        self._test_common_body_with_exception(source, IntegrityError)

    # spec: [StatDataPacket], [(str, str, str, datetime, str)] -> None
    def _test_common_body(self, source_list, expected):
        self._mox.ReplayAll()
        storage = PgStorageImpl(self._db_manager.connection_string, self._logger)
        for source in source_list:
            storage.save_data(source)
        actual = self._db_manager.execute_query(self._query)
        self._check_data(expected, actual)
        self._mox.VerifyAll()

    # spec: [StatDataPacket], class -> None
    def _test_common_body_with_exception(self, source, expected_exception):
        self._mox.ReplayAll()
        storage = PgStorageImpl(self._db_manager.connection_string, self._logger)
        self.assertRaises(expected_exception, lambda: storage.save_data(source))
        self._mox.VerifyAll()

    # spec: str, StatDataItem -> None
    def _set_logger_when_normal(self, user_id, items):
        self._logger.info('save_data(data) enter')
        for item in items:
            self._logger.info('save_item(cursor, {user_id:s}, {item!s}) enter'.format(user_id=user_id, item=item))
            self._logger.info('save_item(cursor, {user_id:s}, {item!s}) exit'.format(user_id=user_id, item=item))
        self._logger.info('save_data(data) exit')

    # spec: str, StatDataItem -> None
    def _set_logger_when_exception(self, user_id, item):
        self._logger.info('save_data(data) enter')
        self._logger.info('save_item(cursor, {user_id:s}, {item!s}) enter'.format(user_id=user_id, item=item))
        self._logger.exception('exception in save_item(cursor, {user_id:s}, {item!s})'.format(user_id=user_id, item=item))
        self._logger.exception('exception in save_data(data)')

    # spec: [(str, str, str, datetime, str), (long, str, str, str, datetime, str)]
    def _check_data(self, expected, actual):
        self.assertEqual(len(expected), len(actual))
        index = 0
        while index < len(expected):
            expected_row = expected[index]
            actual_row = actual[index]
            # id
            self.assertIsNotNone(actual_row[0])
            # user_id
            self.assertEqual(expected_row[0], actual_row[1])
            # source
            self.assertEqual(expected_row[1], actual_row[2])
            # category
            self.assertEqual(expected_row[2], actual_row[3])
            # timemarker
            self.assertEqual(expected_row[3], actual_row[4])
            # data
            self.assertEqual(expected_row[4], actual_row[5])
            index += 1

__author__ = 'andrey.ushakov'
