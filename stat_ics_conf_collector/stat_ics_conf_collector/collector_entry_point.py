from __future__ import unicode_literals
import logging
import logging.config
from stat_file_source.file_source_collect_task import FileSourceCollectTask
from stat_ics_conf_collector import settings, filters_def, handlers_def

# spec: None -> bool
def execute():
    source_id = 'ics.conf'
    # source and dest
    ics_conf_source = settings.ICS_CONF_SOURCE
    dest_db_conn_str = settings.DEST_DB_CONN_STR
    # filters and handlers
    filters = filters_def.filters_def
    handlers = handlers_def.handlers_def
    # logger
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_ics_conf_collector.entry_point')
    # file source collect task
    task = FileSourceCollectTask(source_id, filters, handlers, ics_conf_source, dest_db_conn_str, root_logger)
    return task.execute()


__author__ = 'andrey.ushakov'
