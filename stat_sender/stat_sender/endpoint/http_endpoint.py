import httplib
from stat_sender.common import logger_helper
from stat_sender.endpoint.endpoint import Endpoint

class HttpEndpoint(Endpoint):

    # spec (None -> HttpConnection), str, Logger -> HttpEndpoint
    def __init__(self, connection_factory, path, logger):
        self._connection_factory = connection_factory
        self._path = path
        self._logger = logger

    # spec: str -> bool
    def send(self, data):
        self._logger.info('send(data) enter')
        conn = self._connection_factory()
        try:
            headers = {"Content-Type": "application/xml", "Accept": "text/plain"}
            conn.request('POST', self._path, data, headers)
            response = conn.getresponse()
            result = response.status == httplib.OK
            str_result = logger_helper.bool_result_to_str(result)
            self._logger.info('send(data) exit with result {0:s}'.format(str_result))
            return result
        except BaseException:
            self._logger.exception('exception in send(data)')
            return False
        finally:
            conn.close()


__author__ = 'andrey.ushakov'
