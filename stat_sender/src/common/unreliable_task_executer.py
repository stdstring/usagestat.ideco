from __future__ import unicode_literals
import logging
from src.common.logger_helper import LoggerHelper

class UnreliableTaskExecuter(object):

    def __init__(self, task, max_attempt_count, logger = logging.getLogger('stat_sender.unreliable_task_executer')):
        self._task = task
        self._max_attempt_count = max_attempt_count
        self._logger = logger

    # spec: None -> bool
    def execute(self):
        result = False
        attempt_count = 0
        self._logger.info('UnreliableTaskExecuter.execute() enter')
        while attempt_count < self._max_attempt_count:
            self._logger.info('UnreliableTaskExecuter.execute(): iteration number %(iteration)d' % {'iteration': attempt_count+1})
            result = self._safe_execute()
            if result:
                break
            attempt_count += 1
        str_result = LoggerHelper.bool_result_to_str(result)
        self._logger.info('UnreliableTaskExecuter.execute() exit with result %(result)s' % {'result': str_result})
        return result

    # spec: None -> bool
    def _safe_execute(self):
        try:
            return self._task()
        except Exception:
            return False

    _max_attempt_count = 1
    _task = None
    _logger = None

__author__ = 'andrey.ushakov'
