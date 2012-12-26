from __future__ import unicode_literals
import logging
import logging.config
import kinterbasdb
from stat_db_source.db_source_collect_task import DbSourceCollectTask
from stat_source_common.storage.sqlite_storage import SqliteStorage
from stat_ics_db_collector import settings, collect_task_def

# spec: None -> bool
def execute():
    source_id = 'ics.db'
    # logger
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_ics_db_collector.entry_point')
    # source
    ics_db_conn_str = settings.ICS_DB_CONN_STR
    prepared_conn_str = dict(map(lambda k: (k, str(ics_db_conn_str[k])), ics_db_conn_str))
    source_connect_factory = lambda: kinterbasdb.connect(prepared_conn_str)
    # dest
    dest_db_conn_str = settings.DEST_DB_CONN_STR
    dest_storage = SqliteStorage(dest_db_conn_str, root_logger.getChild('dest_storage'))
    # collect_task
    collect_task_list = collect_task_def.collect_task_def
    # db source collect task
    task = DbSourceCollectTask(source_id, collect_task_list, source_connect_factory, dest_storage, root_logger)
    return task.execute()
    pass

__author__ = 'andrey.ushakov'
