from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from tastypie.api import Api
from stat_server.api.resources import ReceiverResource

v1_api = Api(api_name='v1')
v1_api.register(ReceiverResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stat_server.views.home', name='home'),
    # url(r'^stat_server/', include('stat_server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^statserver/api/', include(v1_api.urls)),
)
