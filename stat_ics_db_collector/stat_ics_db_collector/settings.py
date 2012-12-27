from __future__ import unicode_literals

# ics.db connection string
ICS_DB_CONN_STR = {'host':'localhost', 'database':'', 'user':'', 'password':''}

# dest db connection string
DEST_DB_CONN_STR = ''

# logs
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                               'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console':{'level': 'DEBUG',
                            'class': 'logging.StreamHandler',
                            'formatter': 'default'}},
    'loggers': {'stat_ics_db_collector.entry_point': {'handlers': ['console'],
                                                      'level': 'INFO',
                                                      'propagate': True}}
}

__author__ = 'andrey.ushakov'
