from __future__ import unicode_literals
from ConfigParser import SafeConfigParser
import os

class Settings(object):

    # spec: None -> str
    @staticmethod
    def get_db_file():
        if Settings._db_file is None:
            Settings._load_conf_file()
        return Settings._db_file

    # spec: None -> str
    @staticmethod
    def get_remote_host():
        if Settings._remote_host is None:
            Settings._load_conf_file()
        return Settings._remote_host

    # spec: None -> str
    @staticmethod
    def get_key_file():
        if Settings._key_file is None:
            Settings._load_conf_file()
        return Settings._key_file

    # spec: None -> str
    @staticmethod
    def get_cert_file():
        if Settings._cert_file is None:
            Settings._load_conf_file()
        return Settings._cert_file

    # spec: None -> int
    @staticmethod
    def get_send_attempt_count():
        if Settings._send_attempt_count is None:
            Settings._load_conf_file()
        return Settings._send_attempt_count

    # spec: None -> str
    @staticmethod
    def get_log_conf():
        if Settings._log_conf is None:
            Settings._load_conf_file()
        return Settings._log_conf

    # spec: None -> None
    @staticmethod
    def _load_conf_file():
        main_conf_file = 'stat_sender.conf'
        main_conf_path = os.path.abspath(main_conf_file)
        conf_parser = SafeConfigParser()
        conf_parser.read(main_conf_path)
        Settings._db_file = conf_parser.get('storage_conf', 'db_file')
        Settings._remote_host = conf_parser.get('endpoint_conf', 'remote_url')
        Settings._key_file = conf_parser.get('endpoint_conf', 'key_file')
        Settings._cert_file = conf_parser.get('endpoint_conf', 'cert_file')
        Settings._send_attempt_count = conf_parser.getint('endpoint_conf', 'send_attempt_count')
        Settings._log_conf = conf_parser.get('log_conf', 'log_conf_file')

    # for storage
    _db_file = None
    # for endpoint
    _remote_host = None
    _key_file = None
    _cert_file = None
    # for task execution
    _send_attempt_count = None
    # for logs
    _log_conf = None

__author__ = 'andrey.ushakov'
