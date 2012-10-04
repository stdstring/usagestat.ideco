from __future__ import unicode_literals
from sqlite3 import connect
import os
import shutil
import subprocess
import tempfile

class DbCreationException(Exception):
    pass

class InvalidOperationException(Exception):
    pass

class DBManager(object):

    # spec: str -> DBManager
    def __init__(self, db_create_script_path):
        self._db_create_script_path = db_create_script_path

    def __enter__(self):
        self._prepare_db()
        self._ready = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ready = False
        self._remove_temp_db_dir()
        os.chdir(self._initial_working_dir)
        return True

    # spec: str, tuple -> tuple
    def execute_query(self, query, params=()):
        if not self._ready:
            raise InvalidOperationException()
        db_filename = self.get_db_file()
        conn = connect(db_filename)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()

    # spec: str, tuple -> None
    def execute_nonquery(self, query, params=()):
        if not self._ready:
            raise InvalidOperationException()
        db_filename = self.get_db_file()
        conn = connect(db_filename)
        try:
            cursor = conn.cursor()
            if params == ():
                cursor.execute(query)
            else:
                cursor.executemany(query, params)
            conn.commit()
        finally:
            conn.close()

    # spec: None -> str
    def get_db_file(self):
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, self._db_dirname, self._db_filename)

    # spec: None -> None
    def _prepare_db(self):
        os.chdir(self._initial_working_dir)
        self._create_temp_db_dir()
        abs_create_script_path = os.path.abspath(self._db_create_script_path)
        self._remove_temp_db_dir()
        shutil.copytree(abs_create_script_path, self._get_db_dir())
        os.chdir(self._get_db_dir())
        create_result = subprocess.call([os.path.join(self._get_db_dir(), self._db_create_script_name)])
        if create_result:
            raise DbCreationException()

    # spec : str -> None
    def _create_temp_db_dir(self):
        temp_db_dir = self._get_db_dir()
        if not os.path.exists(temp_db_dir):
            os.makedirs(temp_db_dir)

    # spec: None -> None
    def _remove_temp_db_dir(self):
        temp_db_dir = self._get_db_dir()
        if os.path.exists(temp_db_dir):
            shutil.rmtree(temp_db_dir)

    # spec: None -> str
    def _get_db_dir(self):
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, self._db_dirname)

    _ready = False
    _initial_working_dir = os.getcwd()
    _db_create_script_path = None
    _db_create_script_name = 'create.sh'
    _db_dirname = 'usage_stat_db'
    _db_filename = 'usage_stat.db'

__author__ = 'andrey.ushakov'
