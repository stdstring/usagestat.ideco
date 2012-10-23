from __future__ import unicode_literals
from stat_sender.endpoint.http_endpoint import HttpEndpoint
from stat_sender.endpoint.https_endpoint import HttpsEndpoint

# storage
DB_FILE = ''

# endpoint
USED_ENDPOINT = 'http'

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
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                               'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console':{'level': 'DEBUG',
                            'class': 'logging.StreamHandler',
                            'formatter': 'default'}},
    'loggers': {'stat_sender.entry_point': {'handlers': ['console'],
                                            'level': 'INFO',
                                            'propagate': True}}
}

__author__ = 'andrey.ushakov'
