from __future__ import unicode_literals
import os
import shutil
import sqlite3
import subprocess
import tempfile
import psycopg2

class DbCreationException(Exception):
    pass

class InvalidOperationException(Exception):
    pass

# TODO (andrey.ushakov) : make this class abstract
class DbManager(object):

    def __init__(self):
        self._ready = False
        self._connection_string = None

    def __enter__(self):
        self._prepare_db()
        self.ready = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ready = False
        self._clear_db()
        return True

    @property
    def connection_string(self):
        return self._connection_string

    @connection_string.setter
    def connection_string(self, value):
        self._connection_string = value

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, value):
        self._ready = value

    # spec: str, tuple -> tuple
    def execute_query(self, query, params=()):
        if not self._ready:
            raise InvalidOperationException()
        conn = self._create_connection()
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
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            if params == ():
                cursor.execute(query)
            else:
                cursor.executemany(query, params)
            conn.commit()
        finally:
            conn.close()

    def _prepare_db(self):
        raise NotImplementedError()

    def _clear_db(self):
        raise NotImplementedError()

    def _create_connection(self):
        raise NotImplementedError()

__author__ = 'andrey.ushakov'
