from __future__ import unicode_literals
from common.unreliable_task_executer import UnreliableTaskExecuter

class StatSendTask(object):

    def __init__(self, storage, data_processors, endpoint, send_attempt_count):
        self._storage = storage
        self._data_processors = data_processors
        self._endpoint = endpoint
        self._send_attempt_count = send_attempt_count

    # spec: None -> bool
    def execute(self):
        try:
            # get data
            stat_data = self._storage.get_data()
            # process data
            data = stat_data
            for data_processor in self._data_processors:
                data = data_processor.process(data)
            # send data
            task = lambda: self._endpoint.send(data)
            send_executer = UnreliableTaskExecuter(task, self._send_attempt_count)
            result = send_executer.execute()
            if not result:
                return False
            # clear data
            self._storage.clear(stat_data.id_range)
        except:
            return False
        return True

    _storage = None
    _endpoint =None
    _data_processors = []
    _send_attempt_count = 1

__author__ = 'andrey.ushakov'
