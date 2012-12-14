from __future__ import unicode_literals
import httplib
import urlparse
from stat_sender.endpoint.http_endpoint import HttpEndpoint

class HttpEndpointFactory(object):

    # spec: str, Logger -> HttpEndpoint
    def create(self, remote_host, logger, **kwargs):
        parse_result = urlparse.urlparse(remote_host)
        if parse_result.scheme != 'http' and parse_result.scheme != '':
            raise ValueError()
        hostname = parse_result.hostname
        port = parse_result.port
        path = parse_result.path
        connection_factory = lambda: httplib.HTTPConnection(host=hostname, port=port)
        return HttpEndpoint(connection_factory, path, logger)

__author__ = 'andrey.ushakov'
