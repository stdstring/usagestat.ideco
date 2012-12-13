from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
from stat_source_common.storage import storage
from stat_file_source.file_source_collect_task_impl import FileSourceCollectTaskImpl
from stat_file_source.file_source_collector import FileSourceCollector
from tests.common.custom_test_exception import CustomTestException

class TestFileSourceCollectTaskImpl(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestFileSourceCollectTaskImpl, self).__init__(methodName)
        self._mox = None
        self._collector = None
        self._source_provider = None
        self._storage = None
        self._logger = None

    def setUp(self):
        self._mox = Mox()
        self._collector = self._mox.CreateMock(FileSourceCollector)
        self._source_provider = self._mox.CreateMockAnything()
        self._storage = self._mox.CreateMock(storage.Storage)
        self._logger = self._mox.CreateMock(Logger)

    def test_successful_execute(self):
        self._logger.info('execute() enter')
        self._logger.info('_read_file_content() enter')
        self._source_provider().AndReturn(['key1=value1', 'key2=value2'])
        self._logger.info('_read_file_content() exit')
        self._collector.collect(['key1=value1', 'key2=value2']).AndReturn({'key1': 'value1', 'key2': 'value2'})
        self._logger.info('_write_data(data_dict) enter')
        self._storage.save_data('test', [(u'key2', u'value2'), (u'key1', u'value1')])
        self._logger.info('_write_data(data_dict) exit')
        self._logger.info(u'execute() exit')
        self._test_common_body(True)

    def test_exception_in_source_provider(self):
        self._logger.info('execute() enter')
        self._logger.info('_read_file_content() enter')
        self._source_provider().AndRaise(Exception())
        self._logger.exception('exception in _read_file_content()')
        self._logger.exception('exception in execute()')
        self._test_common_body(False)

    def test_exception_in_collector(self):
        self._logger.info('execute() enter')
        self._logger.info('_read_file_content() enter')
        self._source_provider().AndReturn(['key1=value1', 'key2=value2'])
        self._logger.info('_read_file_content() exit')
        self._collector.collect(['key1=value1', 'key2=value2']).AndRaise(CustomTestException())
        self._logger.exception('exception in execute()')
        self._test_common_body(False)

    def test_exception_in_save_data(self):
        self._logger.info('execute() enter')
        self._logger.info('_read_file_content() enter')
        self._source_provider().AndReturn(['key1=value1', 'key2=value2'])
        self._logger.info('_read_file_content() exit')
        self._collector.collect(['key1=value1', 'key2=value2']).AndReturn({'key1': 'value1', 'key2': 'value2'})
        self._logger.info('_write_data(data_dict) enter')
        self._storage.save_data('test', [(u'key2', u'value2'), (u'key1', u'value1')]).AndRaise(CustomTestException())
        self._logger.exception('exception in execute()')
        self._test_common_body(False)

    def _test_common_body(self, expected_result):
        self._mox.ReplayAll()
        task_impl = FileSourceCollectTaskImpl('test', self._collector, self._source_provider, self._storage, self._logger)
        actual_result = task_impl.execute()
        self.assertEqual(expected_result, actual_result)
        self._mox.VerifyAll()

__author__ = 'andrey.ushakov'
