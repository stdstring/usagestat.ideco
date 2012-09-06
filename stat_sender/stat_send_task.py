from __future__ import unicode_literals

class StatSendTask(object):

    def __init__(self, storage, data_processors, endpoint, send_attempt_count):
        self._storage = storage
        self._data_processors = data_processors
        self._endpoint = endpoint
        self._send_attempt_count = send_attempt_count

    # spec: None -> None
    def execute(self):
        # get data
        stat_data = self._storage.get_data()
        # process data
        data = stat_data
        for data_processor in self._data_processors:
            data = data_processor.process(data)
        result = False
        attempt_count = 0
        # send data
        while attempt_count < self._send_attempt_count:
            result = self._endpoint.send(data)
            if result:
                break
            attempt_count += 1
        # clear data
        if result:
            self._storage.clear(stat_data.id_range)

    _storage = None
    _endpoint =None
    _data_processors = []
    _send_attempt_count = 1

__author__ = 'andrey.ushakov'
