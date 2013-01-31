from __future__ import unicode_literals
import logging
import os
import subprocess
from unittest.case import TestCase
import time
import signal
from test_file_source import TestFileSource
import test_manager
from test_other_source import TestOtherSource

class StatLifeCycleTestScenario(TestCase):

    def __init__(self, methodName='runTest'):
        super(StatLifeCycleTestScenario, self).__init__(methodName)
        self._test_manager = test_manager.TestManager()

    def setUp(self):
        self._test_manager.__enter__()

    def tearDown(self):
        self._test_manager.__exit__(None, None, None)

    def test_scenario(self):
        stat_server_pid = None
        try:
           # execute stat_server
           stat_server_pid = self._start_stat_server()
           # execute test source
           self._execute_test_other_source()
           # execute test file source
           self._execute_test_file_source()
           # execute stat_sender
           self._execute_stat_sender()
        finally:
            # stop stat_server
            self._stop_stat_server(stat_server_pid)
        # check data in stat_db
        pass

    def _start_stat_server(self):
        stat_server_path = os.path.join(test_manager.CODE_DEST_DIR, 'stat_server/entry_point.py')
        stat_server_proc_args = ['python', stat_server_path]
        stat_server_proc = subprocess.Popen(stat_server_proc_args)
        stat_server_pid = stat_server_proc.pid
        os.setpgid(stat_server_pid, stat_server_pid)
        time.sleep(5)
        return stat_server_pid

    def _execute_test_other_source(self):
        test_other_source_logger = logging.getLogger('test_other_source')
        test_other_source = TestOtherSource(self._test_manager.stat_sender_db.db_filename, test_other_source_logger)
        test_other_source.collect_stat_data()

    def _execute_test_file_source(self):
        source_file = os.path.join(test_manager.DATA_DEST_DIR, 'test_data.conf')
        test_file_source_logger = logging.getLogger('test_file_source')
        test_file_source = TestFileSource(source_file, self._test_manager.stat_sender_db.db_filename, test_file_source_logger)
        test_file_source.collect_stat_data()

    def _execute_stat_sender(self):
        stat_sender_path = os.path.join(test_manager.CODE_DEST_DIR, 'stat_sender/entry_point.py')
        stat_sender_proc_args = ['python', stat_sender_path]
        stat_sender_proc = subprocess.Popen(stat_sender_proc_args)
        stat_sender_proc.wait()

    def _stop_stat_server(self, stat_server_pid):
        if stat_server_pid is not None:
            os.killpg(stat_server_pid, signal.SIGTERM)

__author__ = 'andrey.ushakov'
