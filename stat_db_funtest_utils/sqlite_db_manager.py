from __future__ import unicode_literals
import os
import shutil
import sqlite3
import subprocess
import tempfile
import db_manager

class SqliteDbManager(db_manager.DbManager):

    # spec: str -> SqliteDbManager
    def __init__(self, db_create_script_path, db_dirname='usage_stat_db', db_filename='usage_stat.db'):
        super(SqliteDbManager, self).__init__()
        self._initial_working_dir = os.getcwd()
        self._db_create_script_path = db_create_script_path
        self._db_create_script_name = 'create.sh'
        #db_dirname = 'usage_stat_db'
        #db_filename = 'usage_stat.db'
        self._db_dirname = os.path.join(tempfile.gettempdir(), db_dirname)
        self._db_filename = os.path.join(tempfile.gettempdir(), db_dirname, db_filename)
        self.connection_string = self._db_filename

    # spec: None -> str
    @property
    def db_filename(self):
        return self._db_filename

    # spec: None -> None
    def _prepare_db(self):
        os.chdir(self._initial_working_dir)
        self._create_temp_db_dir()
        abs_create_script_path = os.path.abspath(self._db_create_script_path)
        self._remove_temp_db_dir()
        shutil.copytree(abs_create_script_path, self._db_dirname)
        os.chdir(self._db_dirname)
        create_result = subprocess.call([os.path.join(self._db_dirname, self._db_create_script_name)])
        if create_result:
            raise db_manager.DbCreationException()

    # spec: None -> None
    def _clear_db(self):
        self._remove_temp_db_dir()
        os.chdir(self._initial_working_dir)

    # spec: None -> ?Connection?
    def _create_connection(self):
        return sqlite3.connect(self.connection_string)

    # spec : None -> None
    def _create_temp_db_dir(self):
        if not os.path.exists(self._db_dirname):
            os.makedirs(self._db_dirname)

    # spec: None -> None
    def _remove_temp_db_dir(self):
        if os.path.exists(self._db_dirname):
            shutil.rmtree(self._db_dirname)

__author__ = 'andrey.ushakov'
