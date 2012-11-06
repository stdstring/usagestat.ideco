from __future__ import unicode_literals
import logging, logging.config
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from stat_server import settings
from stat_server.api.not_supported_error import NotSupportedError
from stat_server.api.stat_data_entity import StatDataEntity
from stat_server.storage.pg_storage_impl import PgStorageImpl

class ReceiverResource(Resource):

    id = fields.CharField(attribute = 'id')
    source = fields.CharField(attribute = 'source')
    category = fields.CharField(attribute = 'category')
    timemarker = fields.CharField(attribute = 'timemarker')
    data = fields.CharField(attribute = 'data')

    class Meta:
        resource_name = 'collect'
        authentication = Authentication()
        authorization= Authorization()
        default_format = 'application/xml'
        object_class = StatDataEntity
        allowed_methods = ['put']

    def __init__(self, api_name=None):
        super(ReceiverResource, self).__init__(api_name)
        logging.config.dictConfig(settings.LOGGING)
        self._logger = logging.getLogger('stat_server.receiver_resource')
        conn_params = settings.DATABASES['stat_db']
        self._storage = PgStorageImpl.create(conn_params['NAME'],
            conn_params['USER'],
            conn_params['PASSWORD'],
            conn_params['HOST'],
            conn_params['PORT'],
            self._logger.getChild('pg_storage_impl'))
        self._temp_storage = []

    def dispatch_list(self, request, **kwargs):
        request_repr = request.__repr__()
        try:
            self._logger.info('dispatch_list({0:s}, **kwargs) enter'.format(request_repr))
            response = super(ReceiverResource, self).dispatch_list(request, kwargs = kwargs)
            self._storage.save_data(self._temp_storage)
            self._logger.info('dispatch_list({0:s}, **kwargs) exit'.format(request_repr))
            return response
        except BaseException as e:
            self._logger.exception('exception in dispatch_list({0:s}, **kwargs)'.format(request_repr))
            raise

    # TODO (andrey.ushakov) : large spike
    def alter_deserialized_list_data(self, request, data):
        if isinstance(data, list):
            return {'objects': data}
        return data

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {'resource_name': self._meta.resource_name}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id # pk is referenced in ModelResource
        else:
            kwargs['pk'] = bundle_or_obj.id
        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name
        return self._build_reverse_url('api_dispatch_detail', kwargs = kwargs)

    def get_object_list(self, request):
        raise NotSupportedError()

    def obj_get_list(self, request=None, **kwargs):
        raise NotSupportedError()

    def obj_get(self, request=None, **kwargs):
        raise NotSupportedError()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle_repr= bundle.__repr__()
        try:
            self._logger.info('obj_create({0:s}, request, **kwargs): enter'.format(bundle_repr))
            bundle = self.full_hydrate(bundle)
            new_obj = bundle.obj
            self._temp_storage.append(new_obj)
            self._logger.info('obj_create({0:s}, request, **kwargs): exit'.format(bundle_repr))
            return bundle
        except BaseException:
            self._logger.exception('exception in obj_create({0:s}, request, **kwargs): enter'.format(bundle_repr))
            raise

    def obj_update(self, bundle, request=None, **kwargs):
        raise NotSupportedError()

    def obj_delete_list(self, request=None, **kwargs):
        self._temp_storage = []

    def obj_delete(self, request=None, **kwargs):
        raise NotSupportedError()

    def rollback(self, bundles):
        raise NotSupportedError()

__author__ = 'andrey.ushakov'
