from django.conf.urls.defaults import *

urlpatterns = patterns('periscope.monitoring.views',
    (r'^events$', 'get_events'),
    (r'^event$', 'post_event'),
)
