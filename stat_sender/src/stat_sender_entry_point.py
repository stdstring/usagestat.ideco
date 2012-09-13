from __future__ import unicode_literals
from data_processor.data2xml_processor import Data2XmlProcessor
from data_processor.raw2data_processor import Raw2DataProcessor
from endpoint.endpoint_impl import EndPointImpl
from settings import Settings
from stat_send_task import StatSendTask
from storage.sqlite_storage_impl import SqliteStorageImpl

def execute():
    db_file = Settings.get_db_file()
    remote_host = Settings.get_remote_host()
    key_file = Settings.get_key_file()
    cert_file = Settings.get_cert_file()
    send_attempt_count = Settings.get_send_attempt_count()
    storage = SqliteStorageImpl(db_file)
    endpoint = EndPointImpl(remote_host, key_file, cert_file)
    data_processors = [Raw2DataProcessor(), Data2XmlProcessor()]
    task = StatSendTask(storage, data_processors, endpoint, send_attempt_count)
    result = task.execute()
    return result

__author__ = 'andrey.ushakov'
