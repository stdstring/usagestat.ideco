from __future__ import unicode_literals
import logging
import os
import subprocess
from unittest.case import TestCase
import time
import signal
from test_file_source import TestFileSource
from test_other_source import TestOtherSource

class StatLifeCycleScenario(TestCase):

    def test(self):
        # prepare db for server
        # execute stat_server
        stat_server_path = os.path.abspath('../stat_server/manage.py')
        stat_server_proc_args = ['python', stat_server_path, 'runserver']
        stat_server_proc = subprocess.Popen(stat_server_proc_args)
        stat_server_pid = stat_server_proc.pid
        os.setpgid(stat_server_pid, stat_server_pid)
        time.sleep(5)
        # prepare db for sources
        stat_sender_db_file = '/tmp/usage_stat.db'
        # execute test source
        test_other_source_logger = logging.getLogger('test_other_source')
        test_other_source = TestOtherSource(stat_sender_db_file, test_other_source_logger)
        test_other_source.collect_stat_data()
        # execute test file source
        source_file = os.path.abspath('test_data.conf')
        test_file_source_logger = logging.getLogger('test_file_source')
        test_file_source = TestFileSource(source_file, stat_sender_db_file, test_file_source_logger)
        test_file_source.collect_stat_data()
        # execute stat_sender
        stat_sender_path = os.path.abspath('../stat_sender/entry_point.py')
        stat_sender_proc_args = ['python', stat_sender_path]
        stat_sender_proc = subprocess.Popen(stat_sender_proc_args)
        stat_sender_proc.wait()
        # stop stat_server
        os.killpg(stat_server_pid, signal.SIGTERM)
        # check data in stat_db

__author__ = 'andrey.ushakov'
