from __future__ import unicode_literals
import os
import subprocess
import psycopg2
import db_manager

class PgDbManager(db_manager.DbManager):

    # spec: str, str, str, int, str, str, str -> PgDbManager
    def __init__(self, username, pwd, host=None, port=None, dbname='stat_db', create_script='../stat_server_db/metadata.sql', clear_script='../stat_server_db/clear.sql'):
        super(PgDbManager, self).__init__()
        self.connection_string = self._create_connection_string(dbname, host, port, username, pwd)
        self._create_db_args = self._create_metascript_args(create_script, host, port, username)
        self._clear_db_args = self._create_metascript_args(clear_script, host, port, username)
        self._pwd = pwd

    # spec: None -> None
    def _prepare_db(self):
        clear_result = self._execute_metascript(self._clear_db_args)
        if clear_result:
            raise db_manager.DbCreationException()
        create_result = self._execute_metascript(self._create_db_args)
        if create_result:
            raise db_manager.DbCreationException()

    # spec: None -> None
    def _clear_db(self):
        self._execute_metascript(self._clear_db_args)

    # spec: str, str, int, str, str -> str
    def _create_connection_string(self, dbname, host, port, user, pwd):
        storage = ['dbname={0:s}'.format(dbname), 'user={0:s}'.format(user), 'password={0:s}'.format(pwd)]
        if host is not None:
            storage.append('host={0:s}'.format(host))
        if host is not None:
            storage.append('port={0:d}'.format(port))
        return ' '.join(storage)

    # spec: None -> [str]
    def _create_metascript_args(self, filename, host, port, user):
        metascript_filename = os.path.abspath(filename)
        args = ['psql', '--file={0:s}'.format(metascript_filename), '--username={0:s}'.format(user)]
        if host is not None:
            args.append('--host={0:s}'.format(host))
        if port is not None:
            args.append('--host={0:d}'.format(port))
        return args

    # spec: str -> int
    def _execute_metascript(self, metascript_args):
        metascript_process = subprocess.Popen(args=metascript_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        metascript_process.communicate(self._pwd)
        metascript_process.wait()
        return metascript_process.returncode

    # spec: None -> ?Connection?
    def _create_connection(self):
        return psycopg2.connect(self._connection_string)

__author__ = 'andrey.ushakov'
