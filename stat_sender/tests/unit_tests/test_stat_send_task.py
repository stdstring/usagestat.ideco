from __future__ import unicode_literals
from datetime import datetime
from mox import Mox
import unittest
from unittest.case import TestCase
from src.data_processor.data2xml_processor import Data2XmlProcessor
from src.data_processor.raw2data_processor import Raw2DataProcessor
from src.endpoint.endpoint import EndPoint
from src.stat_send_task import StatSendTask
from src.storage.storage import Storage

class TestStatSendTask(TestCase):

    def setUp(self):
        self._mox = Mox()
        self._storage = self._mox.CreateMock(Storage)
        self._endpoint = self._mox.CreateMock(EndPoint)

    def test_normal_life_cycle(self):
        now = datetime.now().replace(microsecond=0)
        self._storage.get_data().AndReturn([(13, 'c1', now, 'data1')])
        dest_data = '<stat_data><c1><c1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></c1_item></c1></stat_data>'
        self._endpoint.send(dest_data).AndReturn(True)
        self._storage.clear((13, 13))
        self._test_common_action(True)

    def test_empty_data(self):
        self._storage.get_data().AndReturn([])
        self._test_common_action(True)

    def test_exception_when_get_data(self):
        self._storage.get_data().AndRaise(Exception())
        self._test_common_action(False)

    def test_unsuccessful_send(self):
        now = datetime.now().replace(microsecond=0)
        self._storage.get_data().AndReturn([(13, 'c1', now, 'data1')])
        dest_data = '<stat_data><c1><c1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></c1_item></c1></stat_data>'
        self._endpoint.send(dest_data).AndRaise(Exception())
        self._endpoint.send(dest_data).AndReturn(False)
        self._test_common_action(False)

    def test_exception_when_clear(self):
        now = datetime.now().replace(microsecond=0)
        self._storage.get_data().AndReturn([(13, 'c1', now, 'data1')])
        dest_data = '<stat_data><c1><c1_item><timemarker>' + str(now) + '</timemarker><data>data1</data></c1_item></c1></stat_data>'
        self._endpoint.send(dest_data).AndReturn(True)
        self._storage.clear((13, 13)).AndRaise(Exception())
        self._test_common_action(False)

    def _test_common_action(self, expected_result):
        self._mox.ReplayAll()
        task = StatSendTask(self._storage, [Raw2DataProcessor(), Data2XmlProcessor()], self._endpoint, self._send_attempt_count)
        actual_result = task.execute()
        self.assertEquals(expected_result, actual_result)
        self._mox.VerifyAll()

    _mox = None
    _storage = None
    _endpoint = None
    _send_attempt_count = 2

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'
