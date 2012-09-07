from __future__ import unicode_literals

class UnreliableTaskExecuter(object):

    def __init__(self, task, max_attempt_count):
        self._task = task
        self._max_attempt_count = max_attempt_count

    # spec: None -> bool
    def execute(self):
        result = False
        attempt_count = 0
        # send data
        while attempt_count < self._max_attempt_count:
            result = self._safe_execute()
            if result:
                break
            attempt_count += 1
        return result

    def _safe_execute(self):
        try:
            return self._task()
        except:
            return False

    _max_attempt_count = 1
    _task = None

__author__ = 'andrey.ushakov'
