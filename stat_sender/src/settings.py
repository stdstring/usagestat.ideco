from __future__ import unicode_literals

class Settings(object):
    # TODO (andrey.ushakov) : use external file for settings

    # spec: None -> str
    @staticmethod
    def get_db_file():
        if Settings._db_file is None:
            Settings._db_file = ''
        return Settings._db_file

    # spec: None -> str
    @staticmethod
    def get_remote_host():
        if Settings._remote_host is None:
            Settings._remote_host = ''
        return Settings._remote_host

    # spec: None -> str
    @staticmethod
    def get_key_file():
        if Settings._key_file is None:
            Settings._key_file = ''
        return Settings._key_file

    # spec: None -> str
    @staticmethod
    def get_cert_file():
        if Settings._cert_file is None:
            Settings._cert_file = ''
        return Settings._cert_file

    # spec: None -> str
    @staticmethod
    def get_send_attempt_count():
        if Settings._send_attempt_count is None:
            Settings._send_attempt_count = ''
        return Settings._send_attempt_count

    # for storage
    _db_file = None
    # for endpoint
    _remote_host = None
    _key_file = None
    _cert_file = None
    # for task execution
    _send_attempt_count = None

__author__ = 'andrey.ushakov'
