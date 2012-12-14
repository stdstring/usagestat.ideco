from __future__ import unicode_literals
import logging, logging.config
import os
from data_processor.data2xml_processor import Data2XmlProcessor
from data_processor.raw2data_processor import Raw2DataProcessor
from stat_sender import settings
from stat_send_task import StatSendTask
from stat_sender.user_identity.user_identity_provider import UserIdentityProvider
from storage.sqlite_storage import SqliteStorage

# spec: None -> bool
def execute():
    # logger
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_sender.entry_point')
    # endpoint
    endpoint_data = settings.ENDPOINTS_DEF[settings.USED_ENDPOINT]
    endpoint_factory_class = endpoint_data['endpoint_factory']
    remote_host = endpoint_data['remote_host']
    add_params = endpoint_data['params']
    endpoint = endpoint_factory_class().create(remote_host, root_logger.getChild(settings.USED_ENDPOINT + '_endpoint'), kwargs = add_params)
    # storage
    db_file = os.path.abspath(settings.DB_FILE)
    storage = SqliteStorage(db_file, root_logger.getChild('sqlite_storage_impl'))
    # user_identity provider
    user_identity_source = os.path.abspath(settings.USER_IDENTITY_SOURCE)
    user_identity_provider = UserIdentityProvider(user_identity_source)
    # processors
    data_processors = [Raw2DataProcessor(), Data2XmlProcessor()]
    # task
    send_attempt_count = settings.SEND_ATTEMPT_COUNT
    task = StatSendTask(storage, user_identity_provider, data_processors, endpoint, send_attempt_count, root_logger.getChild('stat_send_task'))
    result = task.execute()
    return result

__author__ = 'andrey.ushakov'
