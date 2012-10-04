from __future__ import unicode_literals
import logging
from common.stat_data import StatData
from common.unreliable_task_executer import UnreliableTaskExecuter
from src.common.logger_helper import LoggerHelper

class StatSendTask(object):

    def __init__(self, storage, data_processors, endpoint, send_attempt_count, logger = logging.getLogger('stat_sender.stat_send_task')):
        self._storage = storage
        self._data_processors = data_processors
        self._endpoint = endpoint
        self._send_attempt_count = send_attempt_count
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        self._logger.info('execute() enter')
        try:
            result = self._unsafe_execute()
            str_result = LoggerHelper.bool_result_to_str(result)
            self._logger.info('execute() exit with result %(result)s' % {'result': str_result})
            return result
        except Exception:
            self._logger.exception('exception in execute()')
            return False

    # spec: None -> bool
    def _unsafe_execute(self):
        # get data
        stat_data = self._storage.get_data()
        if not stat_data:
            return True
        # process data
        data = stat_data
        id_range = None
        for data_processor in self._data_processors:
            data = data_processor.process(data)
            # TODO (andrey.ushakov) : think about this spike
            if isinstance(data, StatData):
                id_range = data.id_range
        # send data
        task = lambda: self._endpoint.send(data)
        send_executer = UnreliableTaskExecuter(task, self._send_attempt_count, self._logger.getChild('unreliable_task_executer'))
        result = send_executer.execute()
        if not result:
            return False
        # clear data
        self._storage.clear(id_range)
        return True

    _storage = None
    _endpoint =None
    _data_processors = []
    _send_attempt_count = 1
    _logger = None

__author__ = 'andrey.ushakov'
