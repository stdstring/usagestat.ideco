import httplib
import logging
from src.common.logger_helper import LoggerHelper
from src.endpoint.endpoint import Endpoint

class HttpEndpoint(Endpoint):

    def __init__(self, remote_host, logger=logging.getLogger('stat_sender.http_endpoint'), **kwargs):
        self._logger = logger
        self._connection_factory = lambda: httplib.HTTPConnection(host=remote_host)

    # spec: str -> bool
    def send(self, data):
        self._logger.info('send(data) enter')
        conn = self._connection_factory()
        try:
            headers = {"Content-type": "text/xml", "Accept": "text/plain"}
            conn.request('POST', '', data, headers)
            response = conn.getresponse()
            str_result = LoggerHelper.bool_result_to_str(response.status == httplib.OK)
            self._logger.info('send(data) exit with result {0:s}'.format(str_result))
            return response.status == httplib.OK
        except Exception:
            self._logger.exception('exception in send(data)')
            raise
        finally:
            conn.close()


__author__ = 'andrey.ushakov'
