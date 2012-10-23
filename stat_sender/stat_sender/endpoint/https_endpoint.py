from __future__ import unicode_literals
import httplib
from stat_sender.endpoint.http_endpoint import HttpEndpoint

class HttpsEndpoint(HttpEndpoint):

    def __init__(self, remote_host, logger, **kwargs):
        super(HttpsEndpoint, self).__init__(remote_host, logger, kwargs = kwargs)
        key_file = kwargs['key_file']
        cert_file = kwargs['cert_file']
        self._connection_factory = lambda: httplib.HTTPSConnection(host=remote_host, key_file=key_file, cert_file=cert_file)

__author__ = 'andrey.ushakov'
