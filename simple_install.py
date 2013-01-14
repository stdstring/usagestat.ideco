#! /usr/bin/python
from __future__ import unicode_literals
import compileall
import io
import os
import shutil
import stat
import subprocess
import tempfile

# credentials
_USER_ID = 13000
_USER_NAME = 'usage_stat'
_GROUP_ID = 13000
_GROUP_NAME = 'usage_stat'
_passwd_entry = '{user_name:s}:x:{uid!s}:{gid!s}:usage statistics:/:/sbin/nologin\n'.format(user_name=_USER_NAME, uid=_USER_ID, gid=_GROUP_ID)
_group_entry = '{group_name:s}::{gid!s}:\n'.format(group_name=_GROUP_NAME, gid=_GROUP_ID)

# common path
_LIB_DEST = '/usr/local/lib/python2.7/site-packages/'
_APP_DEST = '/usr/bin/'
_STAT_DB_DEST_DIR = '/var/lib/usage_stat'
_STAT_DB_DEST = os.path.join(_STAT_DB_DEST_DIR, 'usage_stat.db')
_STAT_DB_TEMP = '/tmp/usage_stat'

# app source name
_APP_SOURCE_NAME = 'entry_point.py'
_COMPILED_APP_NAME = 'entry_point.pyc'

# current dir
_current_dir = os.getcwd()
# known libs
_known_libs = ['stat_db_source', 'stat_file_source', 'stat_ics_conf_collector', 'stat_ics_db_collector', 'stat_sender', 'stat_source_common']
# known apps
_known_apps = ['stat_ics_conf_collector', 'stat_ics_db_collector', 'stat_sender']

_CRON_DEST_DIR = '/etc/cron.d'
_CRON_DEST = os.path.join(_CRON_DEST_DIR, 'usage_stat')
# crontab definition section begin
CRONTAB_DEF_BEGIN = '## ics statistic section begin'
# crontab definition section end
CRONTAB_DEF_END = '## ics statistic section end'

# 4 chattr command
_chattr_dest_list = ['/etc/group', '/etc/passwd', _CRON_DEST_DIR, _LIB_DEST, _APP_DEST, '/var/lib/']

def _remove_dir_tree_if_exist(root_path):
    if os.path.exists(root_path):
        subprocess.call(['chattr','-iR', root_path])
        shutil.rmtree(root_path)

def _remove_file_if_exist(file_path):
    if os.path.exists(file_path):
        subprocess.call(['chattr','-i', file_path])
        os.unlink(file_path)

def _remove_known_libs():
    for known_lib in _known_libs:
        dest_full_path = os.path.join(_LIB_DEST, known_lib)
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
        dest_full_path = os.path.join(_LIB_DEST, known_lib)
        shutil.copytree(src_full_path, dest_full_path)

def _remove_known_apps():
    for known_app in _known_apps:
        dest_full_path = os.path.join(_APP_DEST, known_app)
        _remove_file_if_exist(dest_full_path)

def _compile_known_apps():
    for known_app in _known_apps:
        src_full_path = os.path.join(_current_dir, known_app, _APP_SOURCE_NAME)
        compileall.compile_file(src_full_path)

def _copy_known_apps():
    for known_app in _known_apps:
        src_full_path = os.path.join(_current_dir, known_app, _COMPILED_APP_NAME)
        dest_full_path = os.path.join(_APP_DEST, known_app)
        shutil.copy(src_full_path, dest_full_path)

def _remove_usage_stat_db():
    _remove_dir_tree_if_exist(_STAT_DB_DEST_DIR)

def _compile_usage_stat_db():
    _remove_dir_tree_if_exist(_STAT_DB_TEMP)
    shutil.copytree(os.path.join(_current_dir, 'stat_sender_db'), _STAT_DB_TEMP)
    os.chdir(_STAT_DB_TEMP)
    subprocess.call([os.path.join(_STAT_DB_TEMP, 'create.sh')])
    os.chdir(_current_dir)

def _copy_usage_stat_db():
    if not os.path.exists(_STAT_DB_DEST_DIR):
        os.mkdir(_STAT_DB_DEST_DIR)
    shutil.copy(os.path.join(_STAT_DB_TEMP, 'usage_stat.db'), _STAT_DB_DEST)

def _clear_crontab_defs(source):
    dest = []
    statistic_section_flag = False
    for line in source:
        if line.startswith(CRONTAB_DEF_BEGIN):
            statistic_section_flag = True
            continue
        if line.startswith(CRONTAB_DEF_END):
            statistic_section_flag = False
            continue
        if not statistic_section_flag:
            dest.append(line)
    return dest


def _add_crontab_defs(source):
    dest = []
    with io.open(os.path.abspath('crontab_defs')) as crontab_defs_file:
        crontab_defs_content = crontab_defs_file.readlines()
    dest.extend(source)
    dest.extend([CRONTAB_DEF_BEGIN, '\n'])
    dest.extend(crontab_defs_content)
    dest.extend([CRONTAB_DEF_END, '\n'])
    return dest

def _read_from_crontab(user_name):
    try:
        content = subprocess.check_output(['crontab', '-u', user_name, '-l'])
        # TODO (andrey.ushakov) : think about transformation 2 unicode
        return map(lambda bytestr: unicode(bytestr), content.splitlines())
    except subprocess.CalledProcessError:
        return []

def _write_to_crontab(user_name, content):
    with tempfile.NamedTemporaryFile() as content_file:
        content_file.writelines(content)
        content_file.flush()
        os.fsync(content_file)
        subprocess.check_output(['crontab', '-u', user_name, content_file.name])

def _modify_crontab(user_name, content_modificator):
    content_before = _read_from_crontab(user_name)
    content_after = content_modificator(content_before)
    _write_to_crontab(user_name, content_after)

def _cleanup_crontab():
    try:
        _modify_crontab(_USER_NAME, lambda content_before: _clear_crontab_defs(content_before))
    except subprocess.CalledProcessError:
        pass

def _setup_crontab():
    _modify_crontab(_USER_NAME, lambda content_before: _add_crontab_defs(content_before))

def _alt_cleanup_crontab():
    _remove_file_if_exist(_CRON_DEST)

def _alt_setup_crontab():
    with io.open(os.path.abspath('alt_crontab_defs')) as crontab_defs_file:
        content= crontab_defs_file.readlines()
    with io.open(_CRON_DEST, 'wt') as cron_dest_file:
        cron_dest_file.writelines(content)

def _add_line_if_not_exist(file_name, source_line):
    with io.open(file_name, 'rt') as rfile:
        content = rfile.readlines()
        filter_result = filter(lambda current_line: current_line.startswith(source_line), content)
        if len(filter_result) > 0:
            return
        lastline = content[len(content) - 1] if content != [] else ''
    with io.open(file_name, 'at') as wfile:
        wfile.writelines([source_line] if lastline.endswith('\n') else ['\n', source_line])

def _setup_preparation():
    for chattr_dest in _chattr_dest_list:
        subprocess.call(['chattr','-i', chattr_dest])

def _setup_credentials():
    # etc/group
    _add_line_if_not_exist('/etc/group', _group_entry)
    _add_line_if_not_exist('/etc/passwd', _passwd_entry)

def _set_right_for_known_apps():
    for known_app in _known_apps:
        dest_full_path = os.path.join(_APP_DEST, known_app)
        rx_rights = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP
        os.chown(dest_full_path, _USER_ID, _GROUP_ID)
        os.chmod(dest_full_path, rx_rights)

def _set_right_for_known_libs():
    for known_lib in _known_libs:
        dest_full_path = os.path.join(_LIB_DEST, known_lib)
        # set owner
        subprocess.call(['chown','--recursive', '{uid!s}:{gid!s}'.format(uid=_USER_ID, gid=_GROUP_ID), dest_full_path])
        # set rights
        subprocess.call(['chmod','--recursive', '555', dest_full_path])

def _set_right_for_usage_stat_db():
    rx_rights = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR | stat.S_IWGRP
    os.chown(_STAT_DB_DEST, _USER_ID, _GROUP_ID)
    os.chmod(_STAT_DB_DEST, rx_rights)

def cleanup():
    #_cleanup_crontab()
    _alt_cleanup_crontab()
    _remove_usage_stat_db()
    _remove_known_apps()
    _remove_known_libs()

def build():
    # compile new
    _compile_known_libs()
    _compile_known_apps()
    _compile_usage_stat_db()
    # remove source from known libs
    _remove_source_for_known_libs()

def setup():
    _copy_known_libs()
    _copy_known_apps()
    _copy_usage_stat_db()
    # set rights
    _set_right_for_known_libs()
    _set_right_for_known_apps()
    _set_right_for_usage_stat_db()
    # setup crontab
    #_setup_crontab()
    _alt_setup_crontab()

def main():
    # preparation
    _setup_preparation()
    _setup_credentials()
    # actions
    cleanup()
    build()
    setup()

if __name__ == '__main__':
    main()

__author__ = 'andrey.ushakov'

