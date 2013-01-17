from __future__ import unicode_literals
import logging, logging.config
from tornado.ioloop import IOLoop
import settings
from deserializer import simple_json_deserializer
from handler.collect_handler import CollectHandler
from stat_source_common.storage.sqlite_storage import SqliteStorage
from tornado.web import Application

# spec: None -> None
def execute():
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_collector.entry_point')
    storage_logger = root_logger.getChild('sqlite_storage')
    storage = SqliteStorage(settings.DB_CONN_STR, storage_logger)
    collect_handler_logger = root_logger.getChild('collect_handler')
    deserializer = simple_json_deserializer.deserialize
    app = Application([('/collect', CollectHandler, dict(storage=storage, deserializer=deserializer, logger=collect_handler_logger)),
                       ('/collect/', CollectHandler, dict(storage=storage, deserializer=deserializer, logger=collect_handler_logger))])
    app.listen(port=settings.ENDPOINT['PORT'], address=settings.ENDPOINT['HOST'])
    IOLoop.instance().start()

__author__ = 'andrey.ushakov'
