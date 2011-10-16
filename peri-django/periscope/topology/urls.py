from django.conf.urls.defaults import *

urlpatterns = patterns('periscope.topology.views',
    (r'^$', 'topology_list'),
    (r'^escps/((?P<topology_id>\d+)/)?$', 'topology_escps'),
    (r'^generic/((?P<topology_id>\d+)/)?$', 'topology_generic'),
    (r'^get_res', 'topology_get_reservations'),
    (r'^get_users', 'topology_get_users'),
    #(r'^get_xfers', 'topology_get_user_transfers'),
    (r'^get_xfers', 'topology_get_transfers'),
    (r'^delete_paths$', 'delete_paths'),
    (r'^add_transfer$', 'add_transfer'),
    (r'^del_transfer$', 'del_transfer'),
    (r'^get_endpoints_mas$', 'get_endpoints_mas'),
    (r'^save_locations$', 'save_locations'),
    (r'^update_transfer$', 'update_transfer'),
    (r'^esnet/((?P<topology_id>\d+)/)?$', 'topology_esnet'),
)
