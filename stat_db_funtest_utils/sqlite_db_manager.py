from __future__ import unicode_literals
import os
import shutil
import sqlite3
import subprocess
import db_manager

class SqliteDbManager(db_manager.DbManager):

    # spec: str -> SqliteDbManager
    def __init__(self, db_create_script, db_dirname='/tmp/usage_stat_db', db_filename='usage_stat.db'):
        super(SqliteDbManager, self).__init__()
        self._initial_working_dir = os.getcwd()
        self._db_create_script = db_create_script
        self._db_create_script_name = 'create.sh'
        self._db_dirname = db_dirname
        self._db_filename = os.path.join(db_dirname, db_filename)
        self.connection_string = self._db_filename

    # spec: None -> str
    @property
    def db_filename(self):
        return self._db_filename

    # spec: None -> None
    def _prepare_db(self):
        os.chdir(self._initial_working_dir)
        self._create_dest_db_dir()
        abs_create_script = os.path.abspath(self._db_create_script)
        self._remove_dest_db_dir()
        create_result = subprocess.call(['python', abs_create_script, os.path.join(self._db_dirname, self._db_filename)])
        if create_result:
            raise db_manager.DbCreationException()
        os.chdir(self._initial_working_dir)

    # spec: None -> None
    def _clear_db(self):
        self._remove_dest_db_dir()
        os.chdir(self._initial_working_dir)

    # spec: None -> ?Connection?
    def _create_connection(self):
        return sqlite3.connect(self.connection_string)

    # spec : None -> None
    def _create_dest_db_dir(self):
        if not os.path.exists(self._db_dirname):
            os.makedirs(self._db_dirname)

    # spec: None -> None
    def _remove_dest_db_dir(self):
        if os.path.exists(self._db_dirname):
            shutil.rmtree(self._db_dirname)

__author__ = 'andrey.ushakov'
