from __future__ import unicode_literals
from datetime import datetime, timedelta
from unittest.case import TestCase
import time
from src.file_source_collect_task import FileSourceCollectTask
from src.filter.comment_filter import CommentFilter
from src.filter.spaces_filter import SpacesFilter
from src.handler.aggregate_key_value_handler import AggregateKeyValueHandler
from src.handler.simple_key_value_handler import SimpleKeyValueHandler
from src.handler.standard_config_section_handler import StandardConfigSectionHandler
from src.handler.transform_key_value_handler import TransformKeyValueHandler
from src.utils.standard_key_transformer import StandardKeyTransformer

# TODO (andrey.ushakov) : think because this is very dirty hack
import os
import sys
sys.path.append(os.path.abspath('../stat_db_funtest_utils'))
from db_manager import DBManager

# spec: str -> str
def transform_user_fun(source_value):
    delimiter_index = source_value.find(',')
    if delimiter_index == -1:
        return source_value
    else:
        user = source_value[0:delimiter_index]
        pwd = '*' * (len(source_value) - delimiter_index - 1)
        return '%(user)s,%(pwd)s' % {'user': user, 'pwd': pwd}


class TestFileSourceCollectTask(TestCase):

    def setUp(self):
        source_filename = os.path.abspath('tests/functional_tests/test.conf')
        self._db_manager.__enter__()
        filters = [CommentFilter('#'), SpacesFilter()]
        standard_key_transformer = StandardKeyTransformer()
        ip_key_transformer = lambda key, state: '%(category)s.ip' % {'category': state.state_id}
        handlers = [StandardConfigSectionHandler(),
                    SimpleKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'services', standard_key_transformer),
                    TransformKeyValueHandler.create_with_known_key_predicate('=', lambda key, state: state.state_id == 'users', standard_key_transformer, transform_user_fun),
                    AggregateKeyValueHandler.create_with_known_key_list('=', ['ip0', 'ip1', 'ip2', 'ip3', 'ip4'], ip_key_transformer, lambda old_value, item: old_value + 1, 0)]
        self._collect_task = FileSourceCollectTask(filters, handlers, source_filename, self._db_manager.get_db_file())

    def tearDown(self):
        self._db_manager.__exit__(None, None, None)

    def test_execute(self):
        now = datetime.now()
        result = self._collect_task.execute()
        self.assertTrue(result)
        actual = self._db_manager.execute_query('select ID, CATEGORY, TIMEMARKER, DATA from STAT_DATA order by ID')
        expected = [('gate.ip', 3),
            ('dns.ip', 2),
            ('wins.ip', 1),
            ('users.user', 'ivanov,*******'),
            ('users.user', 'petrov,***'),
            ('users.user', 'sydorov,*********'),
            ('users.user', 'kozlov,*********'),
            ('services.http', '80'),
            ('services.ftp', '21')]
        self._check_data(now, expected, actual)

    # spec: datetime, [(str, str)], [(int, str, str, str)] -> None
    def _check_data(self, now, expected, actual):
        self.assertEqual(len(expected), len(actual))
        for expected_item in expected:
            actual_items = filter(lambda item: item[1] == expected_item[0] and item[3] == expected_item[1], actual)
            self.assertEqual(1, len(actual_items))
            actual_item = actual_items[0]
            actual_time = self._str_2_time(actual_item[2])
            self.assertTrue(actual_time - now < timedelta(seconds = 10))

    # spec: str -> datetime
    def _str_2_time(self, source_str):
        time_str = time.strptime(source_str, '%Y-%m-%d %H:%M:%S')
        return datetime(year=time_str.tm_yday, month=time_str.tm_mon, day=time_str.tm_mday, hour=time_str.tm_hour, minute=time_str.tm_min, second=time_str.tm_sec)

    _collect_task = None
    _db_manager = DBManager('../stat_sender_db')

__author__ = 'andrey.ushakov'
