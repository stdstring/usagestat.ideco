from __future__ import unicode_literals
from mox import Mox
import unittest
from unittest.case import TestCase
from src.common.unreliable_task_executer import UnreliableTaskExecuter

class TestUnreliableTaskExecuter(TestCase):

    def setUp(self):
        self._mox = Mox()
        self._task = self._mox.CreateMockAnything()

    def test_good_first_attempt(self):
        self._task().AndReturn(True)
        self._test_common_action(True)

    def test_bad_first_attempt(self):
        self._task().AndReturn(False)
        self._task().AndReturn(True)
        self._test_common_action(True)

    def test_exception_at_first_attempt(self):
        self._task().AndRaise(Exception())
        self._task().AndReturn(True)
        self._test_common_action(True)

    def test_bad_all_attempts(self):
        self._task().AndReturn(False)
        self._task().AndReturn(False)
        self._test_common_action(False)

    def test_exception_at_all_attempts(self):
        self._task().AndRaise(Exception())
        self._task().AndRaise(Exception())
        self._test_common_action(False)

    def _test_common_action(self, expected_result):
        self._mox.ReplayAll()
        executer = UnreliableTaskExecuter(self._task, self._attempt_count)
        actual_result = executer.execute()
        self.assertEquals(expected_result, actual_result)
        self._mox.VerifyAll()

    _mox = None
    _task = None
    _attempt_count = 2

if __name__ == '__main__':
    unittest.main()

__author__ = 'andrey.ushakov'

