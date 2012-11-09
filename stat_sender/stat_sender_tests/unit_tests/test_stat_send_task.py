from __future__ import unicode_literals
from datetime import datetime
from logging import Logger
from mox import Mox
import unittest
from unittest.case import TestCase
import uuid
from stat_sender.data_processor.data2xml_processor import Data2XmlProcessor
from stat_sender.data_processor.raw2data_processor import Raw2DataProcessor
from stat_sender.endpoint.endpoint import Endpoint
from stat_sender.stat_send_task import StatSendTask
from stat_sender.storage.storage import Storage
from stat_sender.user_identity.user_identity_provider import UserIdentityProvider

class TestStatSendTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestStatSendTask, self).__init__(methodName)
        self._now = datetime.now().replace(microsecond=0)
        self._str_now = '{0:%Y-%m-%d %H:%M:%S}'.format(self._now)
        self._mox = None
        self._storage = None
        self._endpoint = None
        self._user_identity_provider = None
        self._logger = None
        self._child_logger = None
        self._send_attempt_count = 2
        self._user_id = uuid.UUID('{11111111-2222-3333-4444-555555555555}')

    def setUp(self):
        self._mox = Mox()
        self._storage = self._mox.CreateMock(Storage)
        self._endpoint = self._mox.CreateMock(Endpoint)
        self._user_identity_provider = self._mox.CreateMock(UserIdentityProvider)
        self._logger = self._mox.CreateMock(Logger)
        self._child_logger = self._mox.CreateMock(Logger)

    def test_normal_life_cycle(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndReturn([(13, 's1', 'c1', self._datetime_2_str(self._now), 'data1')])
        self._user_identity_provider.get_user_identity().AndReturn(self._user_id)
        dest_data = '<data_packet user_id="' + str(self._user_id) + '"><data_item><source>s1</source><category>c1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item></data_packet>'
        self._logger.getChild('unreliable_task_executer').AndReturn(self._child_logger)
        self._child_logger.info('execute() enter')
        self._child_logger.info('execute(): iteration number 1')
        self._endpoint.send(dest_data).AndReturn(True)
        self._child_logger.info('execute() exit with result successfully')
        self._storage.clear((13, 13))
        self._logger.info('execute() exit with result successfully')
        self._test_common_action(True)

    def test_empty_data(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndReturn([])
        self._logger.info('execute() exit with result successfully')
        self._test_common_action(True)

    def test_exception_when_get_data(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndRaise(Exception())
        self._logger.exception('exception in execute()')
        self._test_common_action(False)

    def test_unsuccessful_send(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndReturn([(13, 's1', 'c1', self._datetime_2_str(self._now), 'data1')])
        self._user_identity_provider.get_user_identity().AndReturn(self._user_id)
        dest_data = '<data_packet user_id="' + str(self._user_id) + '"><data_item><source>s1</source><category>c1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item></data_packet>'
        self._logger.getChild('unreliable_task_executer').AndReturn(self._child_logger)
        self._child_logger.info('execute() enter')
        self._child_logger.info('execute(): iteration number 1')
        self._endpoint.send(dest_data).AndReturn(False)
        self._child_logger.info('execute(): iteration number 2')
        self._endpoint.send(dest_data).AndReturn(False)
        self._child_logger.info('execute() exit with result fails')
        self._logger.info('execute() exit with result fails')
        self._test_common_action(False)

    def test_exception_when_clear(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndReturn([(13, 's1', 'c1', self._datetime_2_str(self._now), 'data1')])
        self._user_identity_provider.get_user_identity().AndReturn(self._user_id)
        dest_data = '<data_packet user_id="' + str(self._user_id) + '"><data_item><source>s1</source><category>c1</category><timemarker>' + self._str_now + '</timemarker><data>data1</data></data_item></data_packet>'
        self._logger.getChild('unreliable_task_executer').AndReturn(self._child_logger)
        self._child_logger.info('execute() enter')
        self._child_logger.info('execute(): iteration number 1')
        self._endpoint.send(dest_data).AndReturn(True)
        self._child_logger.info('execute() exit with result successfully')
        self._storage.clear((13, 13)).AndRaise(Exception())
        self._logger.exception('exception in execute()')
        self._test_common_action(False)

    def test_exception_when_get_user_identity(self):
        self._logger.info('execute() enter')
        self._storage.get_data().AndReturn([(13, 's1', 'c1', self._datetime_2_str(self._now), 'data1')])
        self._user_identity_provider.get_user_identity().AndRaise(Exception())
        self._logger.exception('exception in execute()')
        self._test_common_action(False)

    def _test_common_action(self, expected_result):
        self._mox.ReplayAll()
        task = StatSendTask(self._storage, self._user_identity_provider, [Raw2DataProcessor(), Data2XmlProcessor()], self._endpoint, self._send_attempt_count, self._logger)
        actual_result = task.execute()
        self.assertEquals(expected_result, actual_result)
        self._mox.VerifyAll()

    def _datetime_2_str(self, source):
        return source.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
