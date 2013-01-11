from __future__ import unicode_literals

# ics.db connection string
ICS_DB_CONN_STR = {'host':'localhost', 'database':'/var/db/ics_main.gdb', 'user':'SYSDBA', 'password':'SYSDBA'}

# dest db connection string
DEST_DB_CONN_STR = '/var/lib/usage_stat/usage_stat.db'

# logs
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}},
    'filters': {},
    'handlers': {'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'default'},
                 'syslog': {'level': 'INFO', 'class': 'logging.handlers.SysLogHandler', 'formatter': 'default', 'address':('localhost', 514)}},
    'loggers': {'stat_ics_db_collector.entry_point': {'handlers': ['console', 'syslog'], 'level': 'INFO', 'propagate': True}}
}

__author__ = 'andrey.ushakov'
