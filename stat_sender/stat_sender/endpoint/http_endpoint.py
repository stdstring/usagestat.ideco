import httplib
from stat_sender.common.logger_helper import LoggerHelper
from stat_sender.endpoint.endpoint import Endpoint

class HttpEndpoint(Endpoint):

    def __init__(self, remote_host, logger, **kwargs):
        self._logger = logger
        #self._connection_factory = lambda: httplib.HTTPConnection(host=remote_host, port=8000)
        self._connection_factory = lambda: httplib.HTTPConnection(host='127.0.0.1', port=8000)

    # spec: str -> bool
    def send(self, data):
        self._logger.info('send(data) enter')
        conn = self._connection_factory()
        try:
            headers = {"Content-Type": "application/xml", "Accept": "text/plain"}
            conn.request('PUT', '/statserver/api/v1/collect/', data, headers)
            response = conn.getresponse()
            result = response.status == httplib.OK or response.status == httplib.NO_CONTENT
            str_result = LoggerHelper.bool_result_to_str(result)
            self._logger.info('send(data) exit with result {0:s}'.format(str_result))
            return result
        except BaseException as e:
            self._logger.exception('exception in send(data)')
            raise
        finally:
            conn.close()


__author__ = 'andrey.ushakov'
