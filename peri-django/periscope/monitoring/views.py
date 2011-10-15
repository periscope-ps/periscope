# Create your views here.
from periscope.monitoring.soap import DjangoSoapApp
from periscope.monitoring.soap import soapmethod
from periscope.monitoring.soap import soap_types
from soaplib.serializers.clazz import ClassSerializer
from periscope.monitoring.models import PathDataModel
from periscope.monitoring.models import NetworkObjectStatus
from periscope.topology.models import *

from django.views.decorators.cache import never_cache
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from datetime import datetime
import json


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

@never_cache
def get_events(request):
    last_update = request.GET.get('last_update', None)
    if last_update:
        try:
            last_update = datetime.fromtimestamp(int(last_update))
            network_objects = NetworkObjectStatus.objects.filter(last_update__gt=last_update)
        except Exception as ex:
            return HttpResponseBadRequest("Wrong date format use timestamps " + str(ex))
    else:
        network_objects = NetworkObjectStatus.objects.all()
        
    
    status = []
    for obj in network_objects:
        status.append({
            'unisId' : obj.network_object.unis_id,
            'status': obj.status,
            'type': obj.obj_type,
            'gri': obj.gri,
            'userid': obj.userid,
            'username': obj.username,
            'last_update': obj.last_update})
    
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    return HttpResponse(json.dumps(status,  default=dthandler), mimetype="text/plain")
    


# curl -i -H "Accept: application/json" -X POST -d "urn=urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth4:link=eth4##192.168.100.58&status=DOWN" http://127.0.0.1:8000/monitoring/event 

# curl -i -H "Accept: application/json" -X POST -d "src_node=newy-tb-rt-1&src_port=xe-1/3/0&dst_node=bnl-tb-rt-2&dst_port=xe-0/0/1&type=link&status=UP" http://127.0.0.1:8000/monitoring/event 

def post_event(request):
    
    urn = request.POST.get('urn', None)
    status = request.POST.get('status', None)
    src_node = request.POST.get('src_node', None)
    src_port = request.POST.get('src_port', None)
    dst_node = request.POST.get('dst_node', None)
    dst_port = request.POST.get('dst_port', None)
    username = request.POST.get('username', None)
    userid = request.POST.get('userid', None)
    gri = request.POST.get('gri', None)
    otype = request.POST.get('type', None)
    
    if not gri:
        return HttpResponseBadRequest("GRI is not defined")
    
    if dst_node:
        ndst =  Node.objects.get(unis_id__contains=dst_node)
    else:
        return HttpResponseBadRequest("dst_node is not defined")
    
    if src_node:
        nsrc = Node.objects.get(unis_id__contains=src_node)
    else:
        return HttpResponseBadRequest("src_node is not defined")
        
    if src_node and src_port:
        psrc = Port.objects.get(parent__unis_id__contains=src_node, unis_id__contains=src_port)
    if dst_node and dst_port:
        pdst= Port.objects.get(parent__unis_id__contains=dst_node, unis_id__contains=dst_port)
    
    net_objs = NetworkObjectStatus.objects.filter(gri=str(gri))
    if not urn:
        if otype == 'link':
            links = Link.objects.filter(relations__type='source', relations__targets=psrc).filter(relations__type='sink', relations__targets=pdst)
            if not links:
                return HttpResponseBadRequest("Link with src_node=%s, "
                    "src_port=%s, dst_node=%s, dst_port=%s"
                    " is not found." % (src_node, src_port, dst_node, dst_port))
            net_obj = links[0]
            
        if otype == 'transfer':
            net_objs = net_objs.filter(obj_type='transfer')
            net_obj = None
            
            if len(net_objs) > 0:
                net_obj = net_objs[0].network_object.toRealType()
            else:
                unis_id = src_node + ":" + dst_node
                endpoints = EndPointPair.objects.filter(unis_id=unis_id)
                if len(endpoints) > 0:
                    net_obj = endpoints[0]
                else:
                    net_obj = EndPointPair.objects.create(unis_id=unis_id, src=nsrc, dst=ndst)
                    net_obj.save()
            
            if not net_obj:
                return HttpResponseBadRequest("Transfer with src_node=%s, "
                    "src_port=%s, dst_node=%s, dst_port=%s"
                    " is not found." % (src_node, src_port, dst_node, dst_port))
    
    urn = net_obj.unis_id
    objs = NetworkObjectStatus.objects.filter(network_object__unis_id = urn)
    
    if len(objs) == 0:
        net_objs = NetworkObject.objects.filter(unis_id = urn)
        
        if len(net_objs) == 0:
            return HttpResponseBadRequest("URN is is not defined.")
        
        NetworkObjectStatus(network_object=net_objs[0],
            status=status,
            username = username,
            userid = userid,
            gri = gri,
            obj_type = otype,
            last_update=datetime.now()).save()
    else:
        obj = objs[0]
        obj.status = status
        obj.last_update = datetime.now()
        obj.save()
    return HttpResponse("updated", mimetype="text/plain")

monitor_service = MonitoringApp()
