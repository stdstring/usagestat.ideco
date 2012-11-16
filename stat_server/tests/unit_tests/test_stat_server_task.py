from __future__ import unicode_literals
from logging import Logger
from mox import Mox
from unittest.case import TestCase
import uuid
from stat_server.common.datetime_converters import str_2_time
from stat_server.entity.stat_data_item import StatDataItem
from stat_server.entity.stat_data_packet import StatDataPacket
from stat_server.stat_server_task import StatServerTask
from stat_server.storage.storage import Storage

class TestStatServerTask(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestStatServerTask, self).__init__(methodName)
        self._mox = None
        self._storage = None
        self._logger = None
        self._good_xml_packet = '<data_packet user_id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                                '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                                '<data_item><source>source2</source><category>cat2</category><timemarker>2013-01-01 11:11:11</timemarker><data>IDKFA</data></data_item>' +\
                                '</data_packet>'
        data_items = [StatDataItem('source1', 'cat1', str_2_time('2012-12-21 23:59:59'), 'IDDQD'),
                      StatDataItem('source2', 'cat2', str_2_time('2013-01-01 11:11:11'), 'IDKFA')]
        self._good_data_packet = StatDataPacket(uuid.UUID('83cf01c6-2284-11e2-9494-08002703af71'), data_items)

    def setUp(self):
        self._mox = Mox()
        self._storage = self._mox.CreateMock(Storage)
        self._logger = self._mox.CreateMock(Logger)

    def test_normal_life_cycle(self):
        self._logger.info('process_request({0:s}) enter'.format(self._good_xml_packet))
        self._storage.save_data(self._good_data_packet)
        self._logger.info('process_request({0:s}) exit'.format(self._good_xml_packet))
        self._test_common_body(self._good_xml_packet)

    def test_exception_in_deserialization(self):
        bad_xml_packet = '<data_packet id="83cf01c6-2284-11e2-9494-08002703af71">' +\
                         '<data_item><source>source1</source><category>cat1</category><timemarker>2012-12-21 23:59:59</timemarker><data>IDDQD</data></data_item>' +\
                         '<data_item><source>source2</source><category>cat2</category><timemarker>2013-01-01 11:11:11</timemarker><data>IDKFA</data></data_item>' +\
                         '</data_packet>'
        self._logger.info('process_request({0:s}) enter'.format(bad_xml_packet))
        self._logger.exception('exception in process_request({0:s})'.format(bad_xml_packet))
        self._test_common_body_with_exception(bad_xml_packet, KeyError)

    def test_exception_when_save(self):
        self._logger.info('process_request({0:s}) enter'.format(self._good_xml_packet))
        self._storage.save_data(self._good_data_packet).AndRaise(Exception())
        self._logger.exception('exception in process_request({0:s})'.format(self._good_xml_packet))
        self._test_common_body_with_exception(self._good_xml_packet, Exception)

    def _test_common_body(self, request_body):
        self._mox.ReplayAll()
        task = StatServerTask(self._storage, self._logger)
        task.process_request(request_body)
        self._mox.VerifyAll()

    def _test_common_body_with_exception(self, request_body, expected_exception):
        self._mox.ReplayAll()
        task = StatServerTask(self._storage, self._logger)
        self.assertRaises(expected_exception, lambda: task.process_request(request_body))
        self._mox.VerifyAll()

__author__ = 'andrey_ushakov'
