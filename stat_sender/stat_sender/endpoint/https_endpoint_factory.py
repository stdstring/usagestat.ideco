from __future__ import unicode_literals
import httplib
import urlparse
from stat_sender.endpoint.http_endpoint import HttpEndpoint

class HttpsEndpointFactory(object):

    # spec: str, Logger -> HttpEndpoint
    def create(self, remote_host, logger, **kwargs):
        parse_result = urlparse.urlparse(remote_host)
        if parse_result.scheme != 'https' and parse_result.scheme != '':
            raise ValueError()
        hostname = parse_result.hostname
        port = parse_result.port
        path = parse_result.path
        key_file = kwargs['key_file']
        cert_file = kwargs['cert_file']
        connection_factory = lambda: httplib.HTTPSConnection(host=hostname, port=port, key_file=key_file, cert_file=cert_file)
        return HttpEndpoint(connection_factory, path, logger)

__author__ = 'std_string'
