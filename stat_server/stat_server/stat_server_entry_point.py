from __future__ import unicode_literals
import logging, logging.config
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
import settings
from handler.collect_handler import CollectHandler
from xml_serialization.xml_deserializer import XmlDeserializer
from entity.stat_data_packet import StatDataPacket
from storage.pg_storage_impl import PgStorageImpl

# spec; None -> None
def execute():
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_collector.entry_point')
    storage_logger = root_logger.getChild('pg_storage_impl')
    collect_handler_logger = root_logger.getChild('collect_handler')
    storage = PgStorageImpl(settings.DB_CONN_STR, storage_logger)
    deserializer_obj = XmlDeserializer()
    deserializer = lambda source: deserializer_obj.deserialize(StatDataPacket, source)
    app = Application([('/statserver/api/v1/collect', CollectHandler, dict(storage=storage, deserializer=deserializer, logger=collect_handler_logger)),
                       ('/statserver/api/v1/collect/', CollectHandler, dict(storage=storage, deserializer=deserializer, logger=collect_handler_logger))])
    # endpoint
    host = settings.ENDPOINT['HOST']
    port = settings.ENDPOINT['PORT']
    key_file = settings.ENDPOINT['KEY'] if 'KEY' in settings.ENDPOINT else None
    cert_file = settings.ENDPOINT['CERT'] if 'CERT' in settings.ENDPOINT else None
    # server
    ssl_options = {'certfile': cert_file, 'keyfile': key_file} if (key_file is not None) and (cert_file is not None) else None
    http_server = HTTPServer(app, ssl_options=ssl_options)
    http_server.listen(port=port, address=host)
    IOLoop.instance().start()

__author__ = 'andrey.ushakov'
