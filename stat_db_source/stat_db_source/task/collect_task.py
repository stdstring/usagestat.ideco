from __future__ import unicode_literals

class CollectTask(object):

    # spec: [str], ([[(...)]] -> [DataItem]), Logger -> CollectTask
    def __init__(self, query_list, process_task, logger):
        self._query_list = query_list
        self._process_task = process_task
        self._intermediate_data = None
        self._logger = logger

    # spec: (str -> [(...)]) -> None
    def collect_data(self, query_executer):
        self._logger.info('collect_data(query_executer) enter')
        try:
            self._intermediate_data = map(lambda query: self._collect_data_item(query_executer, query), self._query_list)
        except Exception:
            self._logger.exception('exception in collect_data(query_executer)')
            raise
        self._logger.info('collect_data(query_executer) exit')

    # spec: None -> [DataItem]
    def process_data(self):
        self._logger.info('process_data() enter')
        try:
            processed_data = self._process_task(self._intermediate_data)
            self._intermediate_data = None
        except Exception:
            self._logger.exception('exception in process_data()')
            raise
        self._logger.info('process_data() exit')
        return processed_data

    # spec: (str -> [(...)]), str -> [(...)]
    def _collect_data_item(self, query_executer, query):
        self._logger.info('_collect_data_item({query!s}) enter'.format(query=query))
        try:
            data = query_executer(query)
        except Exception:
            self._logger.exception('exception in _collect_data_item({query!s})'.format(query=query))
            raise
        self._logger.info('_collect_data_item({query!s}) exit'.format(query=query))
        return data

__author__ = 'andrey.ushakov'
