from __future__ import unicode_literals
from httplib import HTTPSConnection, OK
from endpoint import EndPoint

class EndPointImpl(EndPoint):

    def __init__(self, remote_host, key_file, cert_file):
        self._remote_host = remote_host
        self._key_file = key_file
        self._cert_file = cert_file

    # spec: str -> bool
    def send(self, data):
        conn = HTTPSConnection(host=self._remote_host, key_file=self._key_file, cert_file=self._cert_file)
        try:
            headers = {"Content-type": "text/xml", "Accept": "text/plain"}
            conn.request('POST', '', data, headers)
            response = conn.getresponse()
            return response.status == OK
        finally:
            conn.close()

    _remote_host = None
    _key_file = None
    _cert_file = None

__author__ = 'andrey.ushakov'
