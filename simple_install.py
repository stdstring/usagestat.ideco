#! /usr/bin/python
from __future__ import unicode_literals
import compileall
import os
import shutil
import stat
import subprocess

# common path
LIB_DEST = '/usr/local/lib/python2.7/site-packages/'
APP_DEST = '/usr/bin/'
STAT_DB_DEST = '/var/lib/usage_stat.db'

# app source name
APP_SOURCE_NAME = 'entry_point.py'
COMPILED_APP_NAME = 'entry_point.pyc'

# current dir
_current_dir = os.getcwd()
# known libs
_known_libs = ['stat_db_source', 'stat_file_source', 'stat_ics_conf_collector', 'stat_ics_db_collector', 'stat_sender', 'stat_source_common']
# known apps
_known_apps = ['stat_ics_conf_collector', 'stat_ics_db_collector', 'stat_sender']

def _remove_dir_tree_if_exist(root_path):
    if os.path.exists(root_path):
        shutil.rmtree(root_path)

def _remove_file_if_exist(file_path):
    if os.path.exists(file_path):
        os.unlink(file_path)

def _remove_known_libs():
    for known_lib in _known_libs:
        dest_full_path = os.path.join(LIB_DEST, known_lib)
        _remove_dir_tree_if_exist(dest_full_path)

def _compile_known_libs():
    for known_lib in _known_libs:
        src_full_path = os.path.join(_current_dir, known_lib, known_lib)
        compileall.compile_dir(src_full_path)

def _remove_sources(root_path):
    result = subprocess.call(['find', root_path, '-name', '*.py', '-delete'])
    if result:
        raise OSError("Can't remove source for '{0:s}'".format(root_path))

def _remove_source_for_known_libs():
    for known_lib in _known_libs:
        src_full_path = os.path.join(_current_dir, known_lib, known_lib)
        _remove_sources(src_full_path)

def _copy_known_libs():
    for known_lib in _known_libs:
        src_full_path = os.path.join(_current_dir, known_lib, known_lib)
        dest_full_path = os.path.join(LIB_DEST, known_lib)
        shutil.copytree(src_full_path, dest_full_path)

def _remove_known_apps():
    for known_app in _known_apps:
        dest_full_path = os.path.join(APP_DEST, known_app)
        _remove_file_if_exist(dest_full_path)

def _compile_known_apps():
    for known_app in _known_apps:
        src_full_path = os.path.join(_current_dir, known_app, APP_SOURCE_NAME)
        compileall.compile_file(src_full_path)

def _set_right_for_known_apps():
    for known_app in _known_apps:
        src_full_path = os.path.join(_current_dir, known_app, COMPILED_APP_NAME)
        rx_rights = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(src_full_path, rx_rights)

def _copy_known_apps():
    for known_app in _known_apps:
        src_full_path = os.path.join(_current_dir, known_app, COMPILED_APP_NAME)
        dest_full_path = os.path.join(APP_DEST, known_app)
        shutil.copy(src_full_path, dest_full_path)

def main():
    # remove old
    _remove_known_apps()
    _remove_known_libs()
    # compile new
    _compile_known_libs()
    _compile_known_apps()
    # remove source
    _remove_source_for_known_libs()
    # set rights
    _set_right_for_known_apps()
    # copy
    _copy_known_libs()
    _copy_known_apps()

if __name__ == '__main__':
    main()

__author__ = 'andrey.ushakov'

