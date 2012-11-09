from __future__ import unicode_literals
from stat_server.entity.stat_data_packet import StatDataPacket
from stat_server.xml_serialization.xml_deserializer import XmlDeserializer

class StatServerTask(object):

    # spec: Storage, Logger -> StatServerTask
    def __init__(self, storage, logger):
        self._storage = storage
        self._logger = logger

    # spec: str -> None
    def process_request(self, body):
        try:
            self._logger.info('process_request({0:s}) enter'.format(body))
            stat_data_packet = XmlDeserializer().deserialize(StatDataPacket, body)
            self._storage.save_data(stat_data_packet)
            self._logger.info('process_request({0:s}) exit'.format(body))
        except BaseException:
            self._logger.exception('exception in process_request({0:s})'.format(body))
            raise

__author__ = 'andrey.ushakov'
