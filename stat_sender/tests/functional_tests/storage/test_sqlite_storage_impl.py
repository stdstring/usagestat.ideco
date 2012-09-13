from __future__ import unicode_literals
from datetime import datetime
import os
import shutil
import sqlite3
import subprocess
import tempfile
from unittest.case import TestCase
from src.storage.sqlite_storage_impl import SqliteStorageImpl
from tests.common.exceptions_def import DbCreationException

class TestSqliteStorageImpl(TestCase):

    def setUp(self):
        self._prepare_db()

    def tearDown(self):
        self._remove_temp_db_dir()

    def test_db_metadata(self):
        actual_metadata = self._execute_query("select name, sql from SQLITE_MASTER where type = 'table'")
        expected_metadata = [('STAT_DATA', 'CREATE TABLE STAT_DATA(ID INTEGER PRIMARY KEY, CATEGORY TEXT, TIMEMARKER TEXT, DATA BLOB)')]
        self.assertEquals(expected_metadata, actual_metadata)

    def test_get_data(self):
        now = datetime.now()
        source_data = [('CAT1', str(now), 'some data'), ('CAT2', str(now), 'some another data')]
        self._execute_nonquery('insert into STAT_DATA(CATEGORY, TIMEMARKER, DATA) values(?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._get_db_file())
        actual_data = storage.get_data()
        expected_data = [(1, 'CAT1', str(now), 'some data'), (2, 'CAT2', str(now), 'some another data')]
        self.assertEquals(expected_data, actual_data)

    def test_clear(self):
        now = datetime.now()
        source_data = [('CAT1', str(now), 'some data'), ('CAT2', str(now), 'some other data'), ('CAT3', str(now), 'some another data'), ('CAT4', str(now), 'yet some other data')]
        self._execute_nonquery('insert into STAT_DATA(CATEGORY, TIMEMARKER, DATA) values(?, ?, ?)', source_data)
        storage = SqliteStorageImpl(self._get_db_file())
        storage.clear((2, 3))
        actual_data = self._execute_query('SELECT ID, CATEGORY, TIMEMARKER, DATA FROM STAT_DATA ORDER BY ID')
        expected_data = [(1, 'CAT1', str(now), 'some data'), (4, 'CAT4', str(now), 'yet some other data')]
        self.assertEquals(expected_data, actual_data)

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

    # spec: None -> str
    def _get_db_file(self):
        temp_dir = tempfile.gettempdir()
        return os.path.join(temp_dir, self._db_dirname, self._db_filename)

    def _execute_query(self, query):
        db_filename = self._get_db_file()
        conn = sqlite3.connect(db_filename)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()

    def _execute_nonquery(self, query, params):
        db_filename = self._get_db_file()
        conn = sqlite3.connect(db_filename)
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params)
            conn.commit()
        finally:
            conn.close()

    _initial_working_dir = os.getcwd()
    _db_create_script_path = '../stat_sender_db'
    _db_create_script_name = 'create.sh'
    _db_dirname = 'usage_stat_db'
    _db_filename = 'usage_stat.db'

__author__ = 'andrey.ushakov'