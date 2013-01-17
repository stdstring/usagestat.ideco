from __future__ import unicode_literals

class CollectHandlerImpl:

    # spec: Storage, (str -> StatDataPacket), Logger -> CollectHandlerImpl
    def __init__(self, storage, deserializer, logger):
        self._storage = storage
        self._deserializer = deserializer
        self._logger = logger

    # spec: str -> None
    def collect(self, source_data):
        self._logger.info('collect({0:s}) enter'.format(source_data))
        try:
            data_packet = self._deserializer(source_data)
            self._storage.save_data(data_packet)
        except BaseException:
            self._logger.exception('exception in collect({0:s})'.format(source_data))
            raise
        self._logger.info('collect({0:s}) exit'.format(source_data))

__author__ = 'andrey.ushakov'
