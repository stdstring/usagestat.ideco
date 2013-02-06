#! /usr/bin/python

from __future__ import unicode_literals
import sqlite3
import sys

DEF_LIST = ['create table if not exists STAT_DATA(ID INTEGER PRIMARY KEY, SOURCE TEXT not null, CATEGORY TEXT not null, TIMEMARKER TEXT not null, DATA BLOB not null)']

def main():
    # extract dest db filename from args
    argv = sys.argv
    if len(argv) != 2:
        raise Exception('...')
    dest_db_filename = argv[1]
    # create database
    _create_db(dest_db_filename)

def _create_db(dest_db_filename):
    conn = sqlite3.connect(dest_db_filename)
    try:
        cur = conn.cursor()
        for definition in DEF_LIST:
            cur.execute(definition)
        conn.commit()
    finally:
        conn.close()

if __name__ == '__main__':
    main()

__author__ = 'andrey.ushakov'
