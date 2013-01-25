from __future__ import unicode_literals
import kinterbasdb
import os
import shutil
import stat
import db_manager

class FirebirdDbManager(db_manager.DbManager):

    def __init__(self, source, dest, username, pwd, hostname='localhost'):
        super(FirebirdDbManager, self).__init__()
        self.connection_string = self._create_connection_string(hostname, dest, username, pwd)
        self._source = source
        self._dest = dest

    # spec: None -> None
    def _prepare_db(self):
        if os.path.exists(self._dest):
            self._clear_db()
        shutil.copy(self._source, self._dest)
        mode = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
        os.chmod(self._dest, mode)

    # spec: None -> None
    def _clear_db(self):
        os.unlink(self._dest)

    # spec: None -> ?Connection?
    def _create_connection(self):
        return kinterbasdb.connect(**self.connection_string)

    def _create_connection_string(self, hostname, filename, username, pwd):
        return {'host':hostname, 'database':filename, 'user':username, 'password':pwd}

__author__ = 'andrey.ushakov'
