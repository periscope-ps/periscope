from django.conf.urls.defaults import *

urlpatterns = patterns('periscope.measurements.views',
    (r'^data$', 'get_measurements_data'),
    (r'^view$', 'view_measurements_data'),
    (r'^get_iface$', 'get_iface_data'),
    (r'^get_chart$', 'get_dojo_chart'),
    (r'^get_res_chart$', 'get_res_chart'),
    (r'^get_res_data$', 'get_res_data'),
    (r'^get_host_info$', 'get_host_info'),
    (r'^get_host_data$', 'get_host_data'),
    (r'^get_host_data_mongo$', 'get_host_data_mongo'),
    (r'^get_perfometer_data$', 'get_perfometer_data'),
    
    (r'^get_measurements_data$', 'get_measurements_data_mongo'),
    (r'^chart_data$', 'get_dojo_chart_mongo'),
)
