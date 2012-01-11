from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^my-soap-service/', 'periscope.mysoapapp.views.my_soap_service'),
    (r'^$', include('periscope.topology.urls')),
    (r'^topology/', include('periscope.topology.urls')),
    (r'^measurements/', include('periscope.measurements.urls')),
    (r'^static_media/(.*)', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^restapi/', include('periscope.restapi.urls')),

    (r'^monitoring/', include('periscope.monitoring.urls')),
    (r'^monitor-service/', 'periscope.monitoring.views.monitor_service')
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
