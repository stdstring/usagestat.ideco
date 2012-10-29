from __future__ import unicode_literals
import logging, logging.config
from data_processor.data2xml_processor import Data2XmlProcessor
from data_processor.raw2data_processor import Raw2DataProcessor
from stat_sender import settings
from stat_send_task import StatSendTask
from storage.sqlite_storage import SqliteStorage

# spec: None -> bool
def execute():
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_sender.entry_point')
    db_file = settings.DB_FILE
    endpoint_data = settings.ENDPOINTS_DEF[settings.USED_ENDPOINT]
    endpoint_class = endpoint_data['endpoint_impl']
    remote_host = endpoint_data['remote_host']
    add_params = endpoint_data['params']
    endpoint = endpoint_class(remote_host, root_logger.getChild(settings.USED_ENDPOINT + '_endpoint'), kwargs = add_params)
    send_attempt_count = settings.SEND_ATTEMPT_COUNT
    storage = SqliteStorage(db_file, root_logger.getChild('sqlite_storage_impl'))
    data_processors = [Raw2DataProcessor(), Data2XmlProcessor()]
    task = StatSendTask(storage, data_processors, endpoint, send_attempt_count, root_logger.getChild('stat_send_task'))
    result = task.execute()
    return result

__author__ = 'andrey.ushakov'
