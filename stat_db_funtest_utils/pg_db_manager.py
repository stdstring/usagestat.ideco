from __future__ import unicode_literals
import os
import subprocess
import psycopg2
import db_manager

class PgDbManager(db_manager.DbManager):

    def __init__(self, username, pwd, host=None, port=None):
        super(PgDbManager, self).__init__()
        self.connection_string = self._create_connection_string(host, port, username, pwd)
        self._create_db_args = self._create_metascript_args('../stat_server_db/metadata.sql', host, port, username)
        self._clear_db_args = self._create_metascript_args('../stat_server_db/clear.sql', host, port, username)
        self._pwd = pwd

    def _prepare_db(self):
        clear_result = self._execute_metascript(self._clear_db_args)
        if clear_result:
            raise db_manager.DbCreationException()
        create_result = self._execute_metascript(self._create_db_args)
        if create_result:
            raise db_manager.DbCreationException()

    def _clear_db(self):
        self._execute_metascript(self._clear_db_args)

    def _create_connection_string(self, host, port, user, pwd):
        storage = ['dbname=stat_db', 'user={0:s}'.format(user), 'password={0:s}'.format(pwd)]
        if host is not None:
            storage.append('host={0:s}'.format(host))
        if host is not None:
            storage.append('port={0:d}'.format(port))
        return ' '.join(storage)

    def _create_metascript_args(self, filename, host, port, user):
        metascript_filename = os.path.abspath(filename)
        args = ['psql', '--file={0:s}'.format(metascript_filename), '--username={0:s}'.format(user)]
        if host is not None:
            args.append('--host={0:s}'.format(host))
        if port is not None:
            args.append('--host={0:d}'.format(port))
        return args

    def _execute_metascript(self, metascript_args):
        metascript_process = subprocess.Popen(args=metascript_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        metascript_process.communicate(self._pwd)
        metascript_process.wait()
        return metascript_process.returncode

    def _create_connection(self):
        return psycopg2.connect(self._connection_string)

__author__ = 'andrey.ushakov'
