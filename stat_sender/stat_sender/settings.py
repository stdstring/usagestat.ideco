from __future__ import unicode_literals
from stat_sender.endpoint.http_endpoint_factory import HttpEndpointFactory
from stat_sender.endpoint.https_endpoint_factory import HttpsEndpointFactory

# storage
DB_FILE = '/var/lib/usage_stat/usage_stat.db'

# user_identity source
USER_IDENTITY_SOURCE = '/var/lib/usage_stat/user.id'

# endpoint
USED_ENDPOINT = 'https'

ENDPOINTS_DEF = {'http':  {'endpoint_factory': HttpEndpointFactory,
                           'remote_host': 'http://10.80.1.222:8000/statserver/api/v1/collect/',
                           'params': {}},
                 'https': {'endpoint_factory': HttpsEndpointFactory,
                           'remote_host': 'https://10.80.1.222:8000/statserver/api/v1/collect/',
                           'params': {'key_file': '/var/lib/usage_stat/test.client.ideco.usagestat.key', 'cert_file': '/var/lib/usage_stat/test.client.ideco.usagestat.crt'}}}

# task execution
SEND_ATTEMPT_COUNT = 2

# logs
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'default'},
                 'syslog': {'level': 'INFO', 'class': 'logging.handlers.SysLogHandler', 'formatter': 'default'},
                 'filelog': {'level': 'INFO', 'class': 'logging.handlers.RotatingFileHandler', 'formatter': 'default', 'filename': '/var/log/stat_sender.log', 'maxBytes': 4096000, 'backupCount': 3}},
    'loggers': {'stat_sender.entry_point': {'handlers': ['console', 'syslog', 'filelog'], 'level': 'INFO', 'propagate': True}}
}

__author__ = 'andrey.ushakov'
