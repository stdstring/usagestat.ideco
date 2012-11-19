from __future__ import unicode_literals
from common.stat_data import StatData
from common.unreliable_task_executer import UnreliableTaskExecuter
from stat_sender.common import logger_helper

class StatSendTask(object):

    # spec: Storage, UserIdentityProvider, [DataProcessor], Endpoint, int, Logger
    def __init__(self, storage, user_identity_provider, data_processors, endpoint, send_attempt_count, logger):
        self._storage = storage
        self._user_identity_provider = user_identity_provider
        self._data_processors = data_processors
        self._endpoint = endpoint
        self._send_attempt_count = send_attempt_count
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        self._logger.info('execute() enter')
        try:
            result = self._unsafe_execute()
            str_result = logger_helper.bool_result_to_str(result)
            self._logger.info('execute() exit with result {0:s}'.format(str_result))
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
        user_id = self._user_identity_provider.get_user_identity()
        additional_data = {'user_id': user_id}
        data = stat_data
        id_range = None
        for data_processor in self._data_processors:
            data = data_processor.process(data, **additional_data)
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

__author__ = 'andrey.ushakov'
