from __future__ import unicode_literals
from tornado.web import RequestHandler
from stat_server.handler.collect_handler_impl import CollectHandlerImpl

class CollectHandler(RequestHandler):

    #noinspection PyMethodOverriding
    # spec: Storage, (str -> StatDataPacket), Logger -> None
    def initialize(self, storage, deserializer, logger):
        self._collect_handler_impl = CollectHandlerImpl(storage, deserializer, logger)
        self._logger = logger
    #inspection PyMethodOverriding

    def post(self, *args, **kwargs):
        self._logger.info('post(*args, **kwargs) enter')
        self._collect_handler_impl.collect(self.request.body)
        self._logger.info('post(*args, **kwargs) exit')

__author__ = 'andrey.ushakov'
