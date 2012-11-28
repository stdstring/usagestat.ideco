from __future__ import unicode_literals
from stat_db_source.storage.data_collector import DataCollector

class DbSourceCollector(object):

    # spec: str, [CollectTask], (None -> ?DbConnection?), Storage, Logger -> DbSourceCollector
    def __init__(self, source_id, collect_task_list, source_connection_factory, dest_storage, logger):
        self._source_id = source_id
        self._collect_task_list = collect_task_list
        self._source_connection_factory = source_connection_factory
        self._dest_storage = dest_storage
        self._logger = logger

    # spec: None -> None
    def collect(self):
        self._logger.info('collect() enter')
        try:
            data_collector = DataCollector(self._source_connection_factory, self._logger.getChild('data_collector'))
            data_collector.collect_data(self._collect_task_list)
            collect_task_logger = self._logger.getChild('collect_task')
            for collect_task in self._collect_task_list:
                data_item_list = collect_task.process_data(collect_task_logger)
                self._dest_storage.save_data(self._source_id, data_item_list)
        except Exception as e:
            print e
            self._logger.exception('exception in collect()')
            raise
        self._logger.info('collect() exit')

__author__ = 'andrey.ushakov'