from __future__ import unicode_literals
from httplib import HTTPSConnection, OK
import logging
from endpoint import EndPoint

class EndPointImpl(EndPoint):

    def __init__(self, remote_host, key_file, cert_file, logger = logging.getLogger('stat_sender.endpoint_impl')):
        self._remote_host = remote_host
        self._key_file = key_file
        self._cert_file = cert_file
        self._logger = logger

    # spec: str -> bool
    def send(self, data):
        self._logger.info('EndPointImpl.send(data) enter')
        conn = HTTPSConnection(host=self._remote_host, key_file=self._key_file, cert_file=self._cert_file)
        try:
            headers = {"Content-type": "text/xml", "Accept": "text/plain"}
            conn.request('POST', '', data, headers)
            response = conn.getresponse()
            str_result = self._execute_result_to_str(response.status)
            self._logger.info('EndPointImpl.send(data) exit with result %(result)s' % {'result':str_result})
            return response.status == OK
        except Exception:
            self._logger.exception('exception in EndPointImpl.send(data)')
            raise
        finally:
            conn.close()

    # spec: int -> str
    def _execute_result_to_str(self, execute_result):
        if execute_result == OK:
            return 'successfully'
        else:
            return 'fails'

    _remote_host = None
    _key_file = None
    _cert_file = None
    _logger = None

__author__ = 'andrey.ushakov'
