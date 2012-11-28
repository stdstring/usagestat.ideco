from __future__ import unicode_literals

class CollectTask(object):

    # spec: [str], ProcessTask -> CollectTask
    def __init__(self, query_list, process_task):
        self._query_list = query_list
        self._process_task = process_task
        self._intermediate_data = None

    # spec: (str -> [(...)]), Logger -> None
    def collect_data(self, query_executer, logger):
        logger.info('collect_data(query_executer) enter')
        try:
            self._intermediate_data = map(lambda query: self._collect_data_item(query_executer, query, logger), self._query_list)
        except Exception:
            logger.exception('exception in collect_data(query_executer)')
            raise
        logger.info('collect_data(query_executer) exit')

    # spec: Logger -> [DataItem]
    def process_data(self, logger):
        logger.info('process_data() enter')
        try:
            processed_data = self._process_task.process(self._intermediate_data)
            self._intermediate_data = None
        except Exception:
            logger.exception('exception in process_data()')
            raise
        logger.info('process_data() exit')
        return processed_data

    # spec: (str -> [(...)]), str, Logger -> [(...)]
    def _collect_data_item(self, query_executer, query, logger):
        logger.info('_collect_data_item({query:s}) enter'.format(query=query))
        try:
            data = query_executer(query)
        except Exception:
            logger.exception('exception in _collect_data_item({query:s})'.format(query=query))
            raise
        logger.info('_collect_data_item({query:s}) exit'.format(query=query))
        return data

__author__ = 'andrey.ushakov'
