from __future__ import unicode_literals
import logging, logging.config
from bottle import Bottle, request, run, Route
from stat_server import settings
from stat_server.stat_server_task import StatServerTask
from stat_server.storage.pg_storage_impl import PgStorageImpl

# spec; None -> None
def execute():
    # app
    app = Bottle()
    # initialization
    logging.config.dictConfig(settings.LOG_CONF)
    root_logger = logging.getLogger('stat_server.entry_point')
    storage_logger = root_logger.getChild('pg_storage_impl')
    storage = PgStorageImpl.create(settings.DB['NAME'],
        settings.DB['USER'],
        settings.DB['PASSWORD'],
        settings.DB['HOST'],
        settings.DB['PORT'],
        storage_logger)
    stat_collect_task = StatServerTask(storage, root_logger)
    # routes
    app.add_route(Route(app, '/statserver/api/v1/collect/', 'POST', lambda: stat_collect_task.process_request(request.body.getvalue()), 'collect_endpoint'))
    app.add_route(Route(app, '/statserver/api/v1/collect', 'POST', lambda: stat_collect_task.process_request(request.body.getvalue()), 'alt_collect_endpoint'))
    # run
    run(app, host=settings.ENDPOINT['HOST'], port=settings.ENDPOINT['PORT'])

__author__ = 'andrey.ushakov'
