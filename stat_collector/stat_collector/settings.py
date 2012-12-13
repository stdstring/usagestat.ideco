from __future__ import unicode_literals

# storage
DB_CONN_STR = '/tmp/usage_stat.db'

# logs
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console':{'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'default'}},
    'loggers': {'stat_collector.entry_point': {'handlers': ['console'], 'level': 'INFO', 'propagate': True}}
}

# endpoint
ENDPOINT = {'HOST': 'localhost', 'PORT': 8888}

__author__ = 'andrey.ushakov'
