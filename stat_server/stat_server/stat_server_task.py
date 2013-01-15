from __future__ import unicode_literals
from entity.stat_data_packet import StatDataPacket
from xml_serialization.xml_deserializer import XmlDeserializer

class StatServerTask(object):

    # spec: Storage, Logger -> StatServerTask
    def __init__(self, storage, logger):
        self._storage = storage
        self._logger = logger

    # spec: File -> None
    def process_request(self, body):
        body = self._transform_request_body(body)
        try:
            self._logger.info('process_request({0:s}) enter'.format(body))
            stat_data_packet = XmlDeserializer().deserialize(StatDataPacket, body)
            self._storage.save_data(stat_data_packet)
            self._logger.info('process_request({0:s}) exit'.format(body))
        except BaseException:
            self._logger.exception('exception in process_request({0:s})'.format(body))
            raise

    # spec: File -> str
    def _transform_request_body(self, file_body):
        self._logger.info('_transform_request_body(body) enter')
        try:
            result = unicode(file_body.read())
        except:
            self._logger.exception('exception in _transform_request_body(body)')
            raise
        self._logger.info('_transform_request_body(body) exit')
        return result

__author__ = 'andrey.ushakov'
