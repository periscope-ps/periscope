import os
import sys
from datetime import datetime

try:
    import json
except ImportError:
    import simplejson as json

from django.core.serializers import serialize
from django.views.decorators.cache import never_cache

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.conf import settings

from periscope.topology.lib.topology import create_from_xml_string
from periscope.topology.lib.util import *
from periscope.topology.models import *
from periscope.monitoring.models import PathDataModel, GridFTPTransfer, NetworkObjectStatus
from periscope.measurements.lib.CollectLib import get_endpoints_info
from periscope.measurements.lib.CollectLib import validIP4
from periscope.measurements.lib.CollectLib import get_host_ips, find_cloud
from periscope.measurements.models import DNSCache
    

def save_locations(request):

    post_data = request.raw_post_data

    items = json.loads(post_data)['items']
    error_msg = ""

    print items

    for i in items:
        props = []
        
        if (i['type'] == "node"):
            node = Node.objects.get(id=i['id'])
            try:
                prop = PeriscopeNodeProperties.objects.get(parent=node)
                prop.shape.x = i['x']
                prop.shape.y = i['y']
                prop.shape.save()
            except:
                PeriscopeNodeProperties.objects.create(parent=node, shape=PeriscopeShape.objects.create(
                        shape="circle", x=i['x'], y=i['y'], width=30, height=30, fill="lightcyan",
                        text_xdisp="0", text_ydisp="0", text_align="middle"))

        if (i['type'] == "port"):
            port = Port.objects.get(id=i['id'])
            props = port.properties_bag.all()

            if (len(props) > 0):
                for prop in props:
                    prop = prop.toRealType()
                    if isinstance(prop, PeriscopePortProperties):
                        prop.shape.x = i['x']
                        prop.shape.y = i['y']
                        prop.shape.save()
            else:
                PeriscopePortProperties.objects.create(parent=port, shape=PeriscopeShape.objects.create(
                        shape="circle", x=i['x'], y=i['y'], width=5, height=5, fill="aliceblue",
                        text_xdisp="-10", text_ydisp="-10", text_align="middle"))
                
    return HttpResponse("OK ERROR:" + error_msg, mimetype="text/plain")

def get_endpoints_mas(request):
    post_data = request.POST
    
    if (len(post_data) < 8):
        result = {'status': 'FAIL', 'msg':"TOO FEW ARGUMENTS"}
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json", status=200)
    try:
        result = get_endpoints_info(post_data['src'], post_data['dst'])
    except:
        result = {'status': 'FAIL', 'msg':"ENDPOINTS ERROR"}
        return HttpResponse(json.dumps(result, indent=4), status=200)
    
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")
    

def add_transfer(request):
    post_data = request.POST

    #print >> sys.stderr, post_data.items()

    if (len(post_data) < 8):
        result = {'status': 'FAIL', 'msg':"TOO FEW ARGUMENTS"}
        return HttpResponse(json.dumps(result, indent=4), mimetype="application/json", status=200)
    
    xfers = GridFTPTransfer.objects.filter(transfer_id=post_data['t_id'])
    if (len(xfers) == 0):
        xfer = GridFTPTransfer(transfer_id=post_data['t_id'],
                               status=post_data['status'],
                               src=post_data['src'],
                               dst=post_data['dst'],
                               src_port=post_data['sport'],
                               dst_port=post_data['dport'],
                               user=post_data['user'],
                               misc=post_data['misc']
                               )
        
        try:
            xfer.save()
        except:
            result = {'status': 'FAIL', 'msg':"SAVE ERROR"}
            return HttpResponse(json.dumps(result, indent=4), mimetype="application/json", status=500)
        
    try:
        result = get_endpoints_info(post_data['src'], post_data['dst'])
    except:
        result = {'status': 'INFO', 'msg':"NO ENDPOINTS"}
        #return HttpResponse(json.dumps(result, indent=4), status=200)
    
    return HttpResponse(json.dumps(result, indent=4), mimetype="application/json")



def update_transfer(request):
    post_data = request.POST

    if (len(post_data) < 2):
        return HttpResponse("POST ERROR", mimetype="text/plain")

    tid = post_data['t_id']
    status = post_data['status']

    try:
        xfers = GridFTPTransfer.objects.filter(transfer_id=tid)
    except:
        return HttpResponse("LOOKUP ERROR", mimetype="text/plain")

    for x in xfers:
        x.status = status
        x.save()

    return HttpResponse("OK", mimetype="text/plain")

def del_transfer(request):
    post_data = request.POST

    if (len(post_data) < 1):
        return HttpResponse("POST ERROR", mimetype="text/plain")
        
    for p in post_data.items():
        if p:
            xfer_ids = p[0].split(',')
            
            #print >> sys.stderr, res_ids
            
            for r in xfer_ids:
                xfers = GridFTPTransfer.objects.filter(transfer_id=r)
                for x in xfers:
                    x.delete()

    return HttpResponse("OK", mimetype="text/plain")


def delete_paths(request):
    post_data = request.POST
    for p in post_data.items():
        if p:
            res_ids = p[0].split(',')

    #print >> sys.stderr, res_ids

    for r in res_ids:
        paths = PathDataModel.objects.filter(path_id=r)
        for p in paths:
            p.delete()

    return HttpResponse("OK" , mimetype="text/plain")

@never_cache
def topology_get_users(request):
    from cStringIO import StringIO

    json_users = StringIO()
    json_users.write('[\n');
    
    users = GridFTPTransfer.objects.values_list('user', flat='True').distinct()

    for u in users:
        json_users.write(' {"user": "%s", t_ids: [' % (u))
        xfers = GridFTPTransfer.objects.filter(user=u)
        for x in xfers:
            json_users.write('"%s",' % x.misc)
        
        json_users.write(']},\n')
    
    json_users.write(']')
        
    return HttpResponse(json_users.getvalue(), mimetype="application/json")

@never_cache
def topology_get_user_transfers(request):
    from cStringIO import StringIO

    user = request.GET['user']

    #print >> sys.stderr, user

    json_xfers = StringIO()
    #json_xfers.write('[');

    user_xfers = GridFTPTransfer.objects.filter(user=user)

    json_xfers.write('\n{"xfers": [')
    
    for xfer in user_xfers:
        # need to do some lookups/matching in here
        json_xfers.write('\n {"t_id":"%s",\n "status":"%s",\n "src":"%s",\n "dst":"%s",\n "sport":"%s",\n'
                       ' "dport":"%s",\n "misc":"%s",\n },' % \
                       (xfer.transfer_id, xfer.status, xfer.src, xfer.dst, xfer.src_port, \
                        xfer.dst_port, xfer.misc))
        
    json_xfers.write('],\npaths: [')

    for xfer in user_xfers:        
        if validIP4(xfer.src):
            src = xfer.src
        else:
            try:
                src = DNSCache.objects.get(hostname=xfer.src).ip
            except:
                src = get_host_ips(xfer.src)
                if (len(src) == 0):
                    continue
                else:
                    src = src[0]
                    d = DNSCache(hostname=xfer.src, ip=src)
                    d.save()

        if validIP4(xfer.dst):
            dst = xfer.dst
        else:
            try:
                dst = DNSCache.objects.get(hostname=xfer.dst).ip
            except:
                dst = get_host_ips(xfer.dst)
                if (len(dst) == 0):
                    continue
                else:
                    dst = dst[0]
                    d = DNSCache(hostname=xfer.dst, ip=dst)
                    d.save()

        src_node = find_cloud(src)
        dst_node = find_cloud(dst)    

        if (src_node is None or dst_node is None):
            continue
        
        path = find_path(src_node, dst_node)

        if (path):
            json_xfers.write('\n {"t_id": "%s", "src_id": %s, "dst_id": %s, "link_ids": [' %
                             (xfer.transfer_id, src_node.id, dst_node.id))
            
            hops = path.hops.all()
            for h in hops:
                # we just assume each hop is a link right now
                link = h.target.toRealType()
                json_xfers.write('%s,' % (link.id))

            json_xfers.write(']},')
            
    json_xfers.write(']\n}')
    
    return HttpResponse(json_xfers.getvalue(), mimetype="application/json")

@never_cache
def topology_get_transfers(request):
    """
    ANI demo
    """
    from cStringIO import StringIO

    user = request.GET.get('user', None)
    
    json_xfers = {'xfers': [], 'paths': []}
    user_xfers = NetworkObjectStatus.objects.filter(obj_type='transfer')
    
    if user:
        user_xfers = user_xfers.filter(username=user)
    
    newy_links = [
        'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth5:link=eth5##192.168.100.82',
        'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/26:link=10GBE0/26##192.168.100.82',
        'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/3/0:link=xe-1/3/0.0##192.168.100.21',
        'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/3/0:link=xe-1/3/0.0##192.168.100.181',
        'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/26:link=10GBE0/26##192.168.100.182',
    ]
    bnl_links = [
        'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth5:link=eth5##192.168.100.58',
        'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=10GBE0/25:link=10GBE0/25##192.168.100.182',
        'urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/1:link=xe-0/0/1.0##192.168.100.22',
        'urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/3:link=xe-0/0/3.0##192.168.100.81',
        'urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=10GBE0/25:link=10GBE0/25##192.168.100.82'
    ]
    
    newy_links_ids = []
    bnl_links_ids = []
    for link in newy_links:
        newy_links_ids.append(Link.objects.get(unis_id=link).id)
    for link in bnl_links:
        bnl_links_ids.append(Link.objects.get(unis_id=link).id)
    
    for xfer in user_xfers:
        json_xfer = {
            'resId': xfer.gri,
            'status': xfer.status,
            'src': xfer.network_object.unis_id.split(':')[0],
            'dst': xfer.network_object.unis_id.split(':')[1],
            'username': xfer.username,
            'userid': xfer.userid,
            }
        json_xfers['xfers'].append(json_xfer)
        if json_xfer['src'] == 'bnl-diskpt-1':
            links = bnl_links_ids
        else:
            links = newy_links_ids
        path = {
            'resId': xfer.gri,
            'src_id': xfer.network_object.toRealType().src_id,
            'dst_id': xfer.network_object.toRealType().dst_id,
            'link_ids': links
        }
        json_xfers['paths'].append(path)

    
    
    return HttpResponse(json.dumps(json_xfers), mimetype="application/json")

@never_cache
def topology_get_reservations(request):
    from cStringIO import StringIO

    json_res = StringIO() 
    json_res.write('[');

    reservations = PathDataModel.objects.all()

    json_xfers = {'xfers': [], 'paths': []}

    for res in reservations:
        src=get_port_dns(res.src)
        dst=get_port_dns(res.dst)
        
        json_xfer = {
            'resId': res.path_id,
            'status': res.status,
            'src': str(src),
            'dst': str(dst),
            'dst-ports': res.src_port_range,
            'src-ports': res.dst_port_range,
            'direction': res.direction,
            'start': datetime.fromtimestamp(float(res.start_time)).isoformat(' '),
            'duration': res.duration,
            'bw': res.bandwidth,
            'bw-class': res.bw_class,
            'vlan': res.vlan_id
            }
        json_xfers['xfers'].append(json_xfer)

        path = find_path_byname(src, dst)
        if not path:
            continue
        
        links = []
        hops = path.hops.all()
        for h in hops:
            # we just assume each hop is a link right now
            links.append(h.target.toRealType().id)

        rpath = {
            'resId': res.path_id,
            'src_id': str(src),
            'dst_id': str(dst),
            'link_ids': links
            }
        json_xfers['paths'].append(rpath)
        
    return HttpResponse(json.dumps(json_xfers), mimetype="application/json")

def topology_list(request):
    return render_to_response('topology/topology_list.html',
                                  { 'topologies': Topology.objects.all() },
                                  context_instance=RequestContext(request))

def topology_generic(request, topology_id=None):
    if not topology_id:
        return topology_list(request)

    try:
        topology = Topology.objects.get(pk=topology_id)
    except Topology.DoesNotExist:
        raise Http404, "No topology found with the given id."

    json_topology = get_shape_json(topology)

    return render_to_response('topology/topology_generic.html',
                              { 'json_topology': json_topology.getvalue(),
                                'topologies': Topology.objects.all() },
                              context_instance=RequestContext(request))

def topology_escps(request, topology_id=None):
    if not topology_id:
        return topology_list(request)
    
    try:
        topology = Topology.objects.get(pk=topology_id)
    except Topology.DoesNotExist:
        raise Http404, "No topology found with the given id."

    json_topology = get_shape_json(topology)
    
    return render_to_response('topology/topology_escps.html',
                              { 'json_topology': json_topology.getvalue() },
                              context_instance=RequestContext(request))

@never_cache
def topology_esnet(request, topology_id=None):
    if not topology_id:
        return topology_list(request)

    get_data = dict(request.GET)
    json_xfers = json.dumps(get_data, indent=4)

    try:
        topology = Topology.objects.get(pk=topology_id)
    except Topology.DoesNotExist:
        raise Http404, "No topology found with the given id."
    
    # Exclude some node from the graph
    exNames = ['ameslab-rt2', 'inl-rt1', 'srs-rt1', 'eqx-ash-rt1',
        'pppl-rt2', 'bnl-mr2', 'ivk-rt2', 'nstec-ivk-rt1', 'piax-pa-rt1']
    
    json_topology = get_shape_json_esnet(topology, exNames)

    return render_to_response('topology/topology_esnet.html',
                              { 'json_topology': json_topology.getvalue(),
                                'json_xfers': json_xfers },
                              context_instance=RequestContext(request))
