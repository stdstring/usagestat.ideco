from __future__ import unicode_literals

# db
DB_CONN_STR = 'dbname=stat_db user=postgres password=31415926 host=localhost port=5432'

# endpoint
ENDPOINT = {'HOST': 'localhost', 'PORT': 8000}

# logs
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
                               'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console':{'level': 'DEBUG',
                            'class': 'logging.StreamHandler',
                            'formatter': 'default'}},
    'loggers': {'stat_server.entry_point': {'handlers': ['console'],
                                            'level': 'INFO',
                                            'propagate': True}}
}


__author__ = 'andrey.ushakov'
