from __future__ import unicode_literals
from stat_db_source.db_source_collector import DbSourceCollector

class DbSourceCollectTask(object):

    # spec: str, [CollectTask], (None -> ?DbConnection?), Storage, Logger -> DbSourceCollectTask
    def __init__(self, source_id, collect_task_list, source_connection_factory, dest_storage, logger):
        self._source_id = source_id
        self._collect_task_list = collect_task_list
        self._source_connection_factory = source_connection_factory
        self._dest_storage = dest_storage
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        try:
            self._logger.info('execute() enter')
            collector = DbSourceCollector(self._source_id,
                self._collect_task_list,
                self._source_connection_factory,
                self._dest_storage,
                self._logger.getChild('db_source_collector'))
            collector.collect()
            self._logger.info('execute() exit')
        except Exception:
            self._logger.exception('exception in execute()')
            return False
        return True

__author__ = 'andrey.ushakov'
