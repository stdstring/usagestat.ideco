from __future__ import unicode_literals
from src.endpoint.http_endpoint import HttpEndpoint
from src.endpoint.https_endpoint import HttpsEndpoint

# storage
DB_FILE = ''

# endpoint
USED_ENDPOINT = 'https'

ENDPOINTS_DEF = {'http':  {'endpoint_impl': HttpEndpoint,
                           'remote_host': '',
                           'params': {}},
                 'https': {'endpoint_impl': HttpsEndpoint,
                           'remote_host': '',
                           'params': {'key_file': '', 'cert_file': ''}}}

# task execution
SEND_ATTEMPT_COUNT = 2

# logs
LOG_CONF = {
    'version': 1,
    'filters': {},
    'handlers': {},
    'loggers': {}
}

__author__ = 'andrey.ushakov'
