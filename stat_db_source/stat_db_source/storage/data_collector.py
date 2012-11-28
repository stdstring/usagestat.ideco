from __future__ import unicode_literals

class DataCollector(object):

    # spec: (None -> ?DbConnection?), Logger -> DataCollector
    def __init__(self, connection_factory, logger):
        self._connection_factory = connection_factory
        self._logger = logger

    # spec: [CollectTask] -> None
    def collect_data(self, collect_task_list):
        connection = self._connection_factory()
        self._logger.info('collect_data(collect_task_list) enter')
        try:
            cursor = connection.cursor()
            query_executer = lambda query: query_executer_body(query, cursor)
            collect_task_logger = self._logger.getChild('collect_task')
            for collect_task in collect_task_list:
                collect_task.collect_data(query_executer, collect_task_logger)
        except Exception:
            self._logger.exception('exception in collect_data(collect_task_list)')
            raise
        finally:
            connection.close()
        self._logger.info('collect_data(collect_task_list) exit')

# spec: str, ?DbCursor? -> [{...}]
def query_executer_body(query, cursor):
    cursor.execute(query)
    return cursor.fetchall()


__author__ = 'andrey.ushakov'
