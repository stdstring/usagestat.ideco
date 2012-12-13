from __future__ import unicode_literals
from tornado.web import RequestHandler

class CollectHandler(RequestHandler):

    #noinspection PyMethodOverriding
    # spec Storage, (str -> object), Logger -> None
    def initialize(self, storage, deserializer, logger):
        self._storage = storage
        self._deserializer = deserializer
        self._logger = logger
    #inspection PyMethodOverriding

    def post(self, *args, **kwargs):
        self._logger.info('post(*args, **kwargs) enter')
        try:
            body = self.request.body
            self._logger.info('post(): body = "{0:s}"'.format(body))
            (source_id, data_list) = self._deserializer(body)
            self._storage.save_data(source_id, data_list)
        except BaseException:
            self._logger.info('exception in post(*args, **kwargs)')
            raise
        self._logger.info('post(*args, **kwargs) exit')

__author__ = 'andrey.ushakov'
