from __future__ import unicode_literals
import os
import shutil
from stat_db_funtest_utils.firebird_db_manager import FirebirdDbManager
from stat_db_funtest_utils.pg_db_manager import PgDbManager
from stat_db_funtest_utils.sqlite_db_manager import SqliteDbManager

TEST_BASE_DIR = '/tmp/usagestat_test/'
DATA_DEST_DIR = os.path.join(TEST_BASE_DIR, 'data/')
CODE_DEST_DIR = os.path.join(TEST_BASE_DIR, 'code/')
PYTHONPATH_ENV = 'PYTHONPATH'

class TestManager(object):

    def __init__(self):
        self._stat_sender_db_manager = SqliteDbManager(os.path.abspath('../stat_sender_db'), os.path.join(DATA_DEST_DIR, 'usage_stat_db/'))
        self._server_db_manager = PgDbManager('postgres', '31415926')
        self._ics_db_manager = FirebirdDbManager(os.path.abspath('../stat_ics_db_collector/tests/ics_main.gdb'), '/tmp/usagestat_test/data/ics_main.gdb', 'SYSDBA', 'masterkey')

    def __enter__(self):
        self._create_prerequisites()
        self._stat_sender_db_manager.__enter__()
        self._server_db_manager.__enter__()
        self._ics_db_manager.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ics_db_manager.__exit__(exc_type, exc_val, exc_tb)
        self._server_db_manager.__exit__(exc_type, exc_val, exc_tb)
        self._stat_sender_db_manager.__exit__(exc_type, exc_val, exc_tb)
        self._rm_prerequisites()
        return True

    @property
    def stat_sender_db(self):
        return self._stat_sender_db_manager

    @property
    def server_db(self):
        return self._server_db_manager

    def _create_prerequisites(self):
        self._rm_prerequisites()
        create_dir_if_not_exist(TEST_BASE_DIR)
        os.mkdir(CODE_DEST_DIR)
        os.mkdir(DATA_DEST_DIR)
        self._copy_data()
        self._copy_code()
        self._prepare_code()

    def _rm_prerequisites(self):
        self._rm_data()
        self._rm_code()

    def _copy_data(self):
        # copy key and cert files
        shutil.copy2(os.path.abspath('../ssl/test.client.ideco.usagestat.crt'), os.path.join(DATA_DEST_DIR, 'test.client.ideco.usagestat.crt'))
        shutil.copy2(os.path.abspath('../ssl/test.client.ideco.usagestat.key'), os.path.join(DATA_DEST_DIR, 'test.client.ideco.usagestat.key'))
        shutil.copy2(os.path.abspath('../ssl/test.server.ideco.usagestat.crt'), os.path.join(DATA_DEST_DIR, 'test.server.ideco.usagestat.crt'))
        shutil.copy2(os.path.abspath('../ssl/test.server.ideco.usagestat.key'), os.path.join(DATA_DEST_DIR, 'test.server.ideco.usagestat.key'))
        # copy test_data.conf
        shutil.copy2(os.path.abspath('test_data.conf'), os.path.join(DATA_DEST_DIR, 'test_data.conf'))
        # copy ics.conf
        shutil.copy2(os.path.abspath('../stat_ics_conf_collector/tests/ics.conf'), os.path.join(DATA_DEST_DIR, 'ics.conf'))

    def _rm_data(self):
        rm_dir_if_exist(DATA_DEST_DIR)

    def _copy_code(self):
        # copy stat_source_common
        shutil.copytree(os.path.abspath('../stat_source_common'), os.path.join(CODE_DEST_DIR, 'stat_source_common'))
        # copy stat_db_source
        shutil.copytree(os.path.abspath('../stat_db_source'), os.path.join(CODE_DEST_DIR, 'stat_db_source'))
        # copy stat_file_source
        shutil.copytree(os.path.abspath('../stat_file_source'), os.path.join(CODE_DEST_DIR, 'stat_file_source'))
        # copy stat_ics_conf_collector & conf file
        shutil.copytree(os.path.abspath('../stat_ics_conf_collector'), os.path.join(CODE_DEST_DIR, 'stat_ics_conf_collector'))
        shutil.copy2(os.path.abspath('test_settings/stat_ics_conf_collector.settings.py'),
            os.path.join(CODE_DEST_DIR, 'stat_ics_conf_collector/stat_ics_conf_collector/settings.py'))
        # copy stat_ics_db_collector & conf file
        shutil.copytree(os.path.abspath('../stat_ics_db_collector'), os.path.join(CODE_DEST_DIR, 'stat_ics_db_collector'))
        shutil.copy2(os.path.abspath('test_settings/stat_ics_db_collector.settings.py'),
            os.path.join(CODE_DEST_DIR, 'stat_ics_db_collector/stat_ics_db_collector/settings.py'))
        # copy stat_sender & conf file
        shutil.copytree(os.path.abspath('../stat_sender'), os.path.join(CODE_DEST_DIR, 'stat_sender'))
        shutil.copy2(os.path.abspath('test_settings/stat_sender.settings.py'),
            os.path.join(CODE_DEST_DIR, 'stat_sender/stat_sender/settings.py'))
        # copy stat_server & conf file
        shutil.copytree(os.path.abspath('../stat_server'), os.path.join(CODE_DEST_DIR, 'stat_server'))
        shutil.copy2(os.path.abspath('test_settings/stat_server.settings.py'),
            os.path.join(CODE_DEST_DIR, 'stat_server/stat_server/settings.py'))

    def _rm_code(self):
        rm_dir_if_exist(CODE_DEST_DIR)

    def _prepare_code(self):
        python_path_list = [os.path.join(CODE_DEST_DIR, 'stat_source_common'),
                            os.path.join(CODE_DEST_DIR, 'stat_db_source'),
                            os.path.join(CODE_DEST_DIR, 'stat_file_source'),
                            os.path.join(CODE_DEST_DIR, 'stat_ics_conf_collector'),
                            os.path.join(CODE_DEST_DIR, 'stat_ics_db_collector'),
                            os.path.join(CODE_DEST_DIR, 'stat_sender'),
                            os.path.join(CODE_DEST_DIR, 'stat_server')]
        old_pythonpath = os.getenv(PYTHONPATH_ENV, '')
        delta_pythonpath = ':'.join(python_path_list)
        new_pythonpath = python_path_list if old_pythonpath == '' else old_pythonpath + ':' + delta_pythonpath
        os.putenv(PYTHONPATH_ENV, new_pythonpath)

def create_dir_if_not_exist(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

def rm_dir_if_exist(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

__author__ = 'andrey.ushakov'
