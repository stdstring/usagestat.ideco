import httplib
import urlparse
from stat_sender.common import logger_helper
from stat_sender.endpoint.endpoint import Endpoint

class HttpEndpoint(Endpoint):

    # spec: str, Logger, {...} -> HttpEndpoint
    def __init__(self, remote_host, logger, **kwargs):
        self._logger = logger
        parse_result = urlparse.urlparse(remote_host)
        if parse_result.scheme != 'http':
            raise ValueError()
        hostname = parse_result.hostname
        port = parse_result.port
        self._path = parse_result.path
        self._connection_factory = lambda: httplib.HTTPConnection(host=hostname, port=port)

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
