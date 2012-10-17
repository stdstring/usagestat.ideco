from __future__ import unicode_literals
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from stat_server.api.stat_data_entity import StatDataEntity

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
        # allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
        allowed_methods = ['put']
        # serializer = Serializer(formats=['xml', 'json'])

    def dispatch_list(self, request, **kwargs):
        response = super(ReceiverResource, self).dispatch_list(request, kwargs = kwargs)
        # save data
        return response

    #def dispatch(self, request_type, request, **kwargs):
    #    pass

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

    #def get_object_list(self, request):
    #    pass

    #def obj_get_list(self, request=None, **kwargs):
    #    pass

    #def obj_get(self, request=None, **kwargs):
    #    pass

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = self.full_hydrate(bundle)
        new_obj = bundle.obj
        self._temp_storage.append(new_obj)
        return bundle

        #def obj_update(self, bundle, request=None, **kwargs):
    #    pass

    def obj_delete_list(self, request=None, **kwargs):
        self._temp_storage = []

    #def obj_delete(self, request=None, **kwargs):
    #    pass

    #def rollback(self, bundles):
    #    pass

    _temp_storage = None

__author__ = 'andrey.ushakov'
