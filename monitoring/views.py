# Create your views here.
from periscope.monitoring.soap import DjangoSoapApp
from periscope.monitoring.soap import soapmethod
from periscope.monitoring.soap import soap_types
from soaplib.serializers.clazz import ClassSerializer
from periscope.monitoring.models import PathDataModel

class PathData(ClassSerializer):
    class types:
        path_id = soap_types.String
        src = soap_types.String
        dst = soap_types.String
        src_port_range = soap_types.String
        dst_port_range = soap_types.String
        vlan_id = soap_types.String
        direction = soap_types.String
        start_time = soap_types.Integer
        duration = soap_types.Integer
        bandwidth = soap_types.Integer
        bw_class = soap_types.String
        status = soap_types.String

class MonitoringApp(DjangoSoapApp):
 
    __tns__ = 'http://blackseal.damsl.cis.udel.edu/escpscope/monitor-service/'

    @soapmethod(PathData, _returns=soap_types.String, 
                _outMessage='{'+__tns__+'}new_pathResponse')
#                _outMessage='newpathResponse')
    def new_path(self, newpath):
        path = PathDataModel(path_id = newpath.path_id,
                             src = newpath.src,
                             dst = newpath.dst,
                             src_port_range = newpath.src_port_range,
                             dst_port_range = newpath.dst_port_range,
                             vlan_id = newpath.vlan_id,
                             direction = newpath.direction,
                             start_time = newpath.start_time,
                             duration = newpath.duration,
                             bandwidth = newpath.bandwidth,
                             bw_class = newpath.bw_class,
                             status = newpath.status)
    
        path.save()
        results = 'OK'
        return results

    @soapmethod(PathData, _returns=soap_types.String,
                _outMessage='{'+__tns__+'}status_pathResponse')
#                _outMessage='status_pathResponse')
    def status_path(self, path):
        p=PathDataModel.objects.get(path_id=path.path_id)
        p.status = path.status
        p.save()
        results = 'OK'
        return results
     
    @soapmethod(soap_types.String, _returns=soap_types.String,
                _outMessage='{'+__tns__+'}remove_pathResponse')
#                _outMessage='remove_pathResponse')

    def remove_path(self, pathid):
        paths = PathDataModel.objects.filter(path_id=pathid)
        for p in paths:
            p.delete()
        results = 'OK'
        return results

    
monitor_service = MonitoringApp()
