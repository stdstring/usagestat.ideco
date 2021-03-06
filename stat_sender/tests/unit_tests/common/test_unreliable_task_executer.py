from __future__ import unicode_literals
from logging import Logger
from mox import Mox
import unittest
from unittest.case import TestCase
from stat_sender.common.unreliable_task_executer import UnreliableTaskExecuter

class TestUnreliableTaskExecuter(TestCase):

    def __init__(self, methodName='runTest'):
        super(TestUnreliableTaskExecuter, self).__init__(methodName)
        self._mox = None
        self._task = None
        self._logger = None
        self._attempt_count = 2

    def setUp(self):
        self._mox = Mox()
        self._task = self._mox.CreateMockAnything()
        self._logger = self._mox.CreateMock(Logger)

    def test_good_first_attempt(self):
        self._logger.info('execute() enter')
        self._logger.info('execute(): iteration number 1')
        self._task().AndReturn(True)
        self._logger.info('execute() exit with result successfully')
        self._test_common_action(True)

    def test_bad_first_attempt(self):
        self._logger.info('execute() enter')
        self._logger.info('execute(): iteration number 1')
        self._task().AndReturn(False)
        self._logger.info('execute(): iteration number 2')
        self._task().AndReturn(True)
        self._logger.info('execute() exit with result successfully')
        self._test_common_action(True)

    def test_bad_all_attempts(self):
        self._logger.info('execute() enter')
        self._logger.info('execute(): iteration number 1')
        self._task().AndReturn(False)
        self._logger.info('execute(): iteration number 2')
        self._task().AndReturn(False)
        self._logger.info('execute() exit with result fails')
        self._test_common_action(False)

    def _test_common_action(self, expected_result):
        self._mox.ReplayAll()
        executer = UnreliableTaskExecuter(self._task, self._attempt_count, self._logger)
        actual_result = executer.execute()
        self.assertEquals(expected_result, actual_result)
        self._mox.VerifyAll()

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'

