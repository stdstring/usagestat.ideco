from __future__ import unicode_literals
from stat_sender.endpoint.http_endpoint_factory import HttpEndpointFactory
from stat_sender.endpoint.https_endpoint_factory import HttpsEndpointFactory

# storage
DB_FILE = '/tmp/usage_stat.db'

# user_identity source
USER_IDENTITY_SOURCE = '/tmp/user.id'

# endpoint
USED_ENDPOINT = 'http'

ENDPOINTS_DEF = {'http':  {'endpoint_factory': HttpEndpointFactory,
                           'remote_host': 'http://localhost:8000/statserver/api/v1/collect/',
                           'params': {}},
                 'https': {'endpoint_factory': HttpsEndpointFactory,
                           'remote_host': 'http://localhost:8000/statserver/api/v1/collect/',
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
