#!/usr/bin/env python

import radix
import netaddr

from django.conf import settings
from periscope.topology.models import *
from periscope.measurements.lib.CollectLib import *
from periscope.measurements.lib.TracerouteQuery import *
from django.contrib.contenttypes.models import ContentType


def create_cloud_node(domain, name, CIDR):
    """ Creates a special node of type cloud.
    Cloud node is node used to represent a netblock, rather than just single node.
    """
    cloud = Node.objects.get_or_create(unis_id="urn:ogf:network:domain=%s:node=%s" % (domain, name))[0]
    cloud.type = 'cloud'
    cloud.save()
    
    result = CloudNodeProperties.objects.get_or_create(parent=cloud, CIDR=CIDR)
    props = result[0]
    if result[1]  == True:
        props.parent = cloud
        props.CIDR = CIDR
        cloud.properties_bag.add(props)
        cloud.save()
        props.save()
    
    return cloud


def cloud_traceroute(cloud, portaddresses=[]):
    """Define the traceroute port for the netblock.
    This trace route port will be used to define the route to other cloud
    nodes.
    """
    for portaddress in portaddresses:
        tracePort = Port.objects.get(addresses__value=portaddress)
        props = CloudNodeProperties.objects.get(parent=cloud, CIDR__contains='.')
        props.traceroute.add(tracePort)
        props.save()


def cloud_bwctl(cloud, portaddresses=[]):
    """Define the bwctl( port for the netblock.
    This bwctl( route port will be used to define the route to other cloud
    nodes.
    """
    for portaddress in portaddresses:
        bwctlPort = Port.objects.get(addresses__value=portaddress)
        props = CloudNodeProperties.objects.get(parent=cloud, CIDR__contains='.')
        props.bwctl.add(bwctlPort)
        props.save()

def cloud_owamp(cloud, portaddresses=[]):
    for portaddress in portaddresses:
        owampPort = Port.objects.get(addresses__value=portaddress)
        props = CloudNodeProperties.objects.get(parent=cloud, CIDR__contains='.')
        props.owamp.add(owampPort)
        props.save()


def find_traceroute(srccloud, dstcloud):
    """Find the trace route between the clouds' trace route ports, 
    from Traceroute MA.
    """
    srctraces = CloudNodeProperties.objects.get(parent=srccloud, CIDR__contains='.').traceroute.all()
    dsttraces = CloudNodeProperties.objects.get(parent=dstcloud, CIDR__contains='.').traceroute.all()
    if srctraces is None or srctraces is None:
        raise Exception("Either source/distination trace routes port is not defined.")
    
    trace = EventType.objects.get(value__contains='http://ggf.org/ns/nmwg/tools/traceroute/2.0')
    
    src = None
    dst = None
    
    if len(srctraces.filter(unis_id__contains='owamp')) and len(dsttraces.filter(unis_id__contains='owamp')):
        src = [srctraces.filter(unis_id__contains='owamp')[0]]
        dst = [dsttraces.filter(unis_id__contains='owamp')[0]]
    elif len(srctraces.filter(unis_id__contains='pt1')) and len(dsttraces.filter(unis_id__contains='pt1')):
        src = [srctraces.filter(unis_id__contains='pt1')[0]]
        dst = [dsttraces.filter(unis_id__contains='pt1')[0]]
    else:
        src = srctraces
        dst = srctraces
    
    for sport in src:
        srcAddresses = []
        for a in sport.addresses.all():
            srcAddresses.append(a.value)
        for dport in dst:
            dstAddresses = [] 
            endpoint = EndPointPair.objects.get(src__unis_id=sport.unis_id, dst__unis_id=dport.unis_id)
            objectType = ContentType.objects.get_for_model(endpoint)
            ma = psServiceWatchList.objects.filter(objectID=endpoint.id, objectType=objectType, eventType=trace)
            if len(ma) == 0:
                continue
            else:
                ma = ma[0].service
            accessPoint = ma.properties_bag.all()[0].psserviceproperties.accessPoint
            for a in dport.addresses.all():
                dstAddresses.append(a.value)
            for s in srcAddresses:
                for d in dstAddresses:
                    result = query_traceroute(accessPoint, s, d)
                if result is not None:
                    return result
    return None


def find_best_match_port(node, ip):
    l3ports = node.get_ports().filter(properties_bag__l3portproperties__netmask__contains='.')
    rtree = radix.Radix()
    for p in l3ports:
        props = L3PortProperties.objects.get(parent=p)
        ipAddress = p.addresses.get(type='ipv4').value
        net = netaddr.IPNetwork("%s/%s" % (ipAddress, props.netmask))
        rnode = rtree.add(str(net.cidr))
        rnode.data['port'] = p
    
    rnode = rtree.search_best(ip)
    if rnode is None:
        return None
    else:
        l2port = Relation.objects.get(parent=rnode.data['port'], type='over').targets.all()[0].toRealType()
        return l2port


def create_path(unis_id, src_cloud, dst_cloud, routes):
    """Takes an array of ip addresses from the trace route and creates
    a path with unis_id
    """
    hopnum = len(routes)
    path = Path(unis_id=unis_id)
    path.save()
    
    counter = range(1, len(routes))
    counter.reverse()
    for r in counter:
        if r == len(routes) -1:
            props = CloudNodeProperties.objects.get(parent=dst_cloud)
            result = Port.objects.get_or_create(parent=dst_cloud, addresses__value=props.CIDR)
            #result = Port.objects.get_or_create(parent=dst_cloud, unis_id="%s:port=%s" % (dst_cloud.unis_id, routes[r]))
            sink = result[0]
            if result[1] == True:
                #sink.unis_id = "%s:port=%s" % (dst_cloud.unis_id, routes[r])
                sink.unis_id = "%s:port=%s" % (dst_cloud.unis_id, props.CIDR)
                sink.parent = dst_cloud
                sink.save()
                addr = Address.objects.create(value=props.CIDR, type='CIDR')
                addr.save()
                PortAddresses.objects.create(port=sink, address=addr).save()
        elif r == 1:
            source_node = Port.objects.get(addresses__value=routes[r-1]).parent.toRealType()
            sink = find_best_match_port(source_node, routes[r-1])
        else:
            sink = Port.objects.get(addresses__value=routes[r])
        
        if r == len(routes) -1:
            source_node = Port.objects.get(addresses__value=routes[r-1]).parent.toRealType()
            source = find_best_match_port(source_node, routes[r])
        elif r == 1:
            props = CloudNodeProperties.objects.get(parent=src_cloud)
            result = Port.objects.get_or_create(parent=src_cloud, addresses__value=props.CIDR)
            #result = Port.objects.get_or_create(parent=src_cloud, unis_id="%s:port=%sto%s" % (src_cloud.unis_id, routes[0], routes[1]))
            source = result[0]
            if result[1] == True:
                #source.unis_id = "%s:port=%sto%s" % (src_cloud.unis_id, routes[0], routes[1])
                source.unis_id = "%s:port=%s" % (src_cloud.unis_id, props.CIDR)
                source.parent = src_cloud
                source.save()
                addr = Address.objects.create(value=props.CIDR, type='CIDR')
                addr.save()
                PortAddresses.objects.create(port=source, address=addr).save()
        else:
            source = Port.objects.get(addresses__value=routes[r-1])
        
        l2drelation = Relation.objects.filter(parent=sink, type='over')
        if len(l2drelation) > 0:
            sink = l2drelation[0].targets.all()[0].toRealType()
        
        l2srelation = Relation.objects.filter(parent=source, type='over')
        if len(l2srelation) > 0:
            source = l2srelation[0].targets.all()[0].toRealType()
        
        links = []
        sinkrelation = Relation.objects.filter(targets=sink, type='sink')
        for relation in sinkrelation:
            links.append(relation.parent.toRealType())
        
        link = None
        for l in links:
            if l.get_source().parent == source.parent:
                link = l
                break
        
        # new link needs to be created
        if link is None:
            #print "creating link: unis_id=%s<->%s" % (source.unis_id, sink.unis_id)
            result = Link.objects.get_or_create(unis_id="%s<->%s" % (source.unis_id, sink.unis_id))
            link = result[0]
            if result[1] == True:
                link.parent = source
                link.save()
            
            result = Relation.objects.get_or_create(parent=link, type='source')
            relation = result[0]
            if result[1] == True:
                relation.parent = link
                relation.save()
                relation.targets.add(source)
                relation.save()
            
            result = Relation.objects.get_or_create(parent=link, type='sink')
            relation = result[0]
            if result[1] == True:
                relation.parent = link
                relation.save()
                relation.targets.add(sink)
                relation.save()
        
        result = Hop.objects.get_or_create(parent=path, target=link)
        hop = result[0]
        if result[1] == True:
            hop.unis_id = "%sto%s" % (routes[r-1], routes[r])
            hop.parent = path
            hop.target = link
            hop.save()
            
            props = psHopProperties(parent=hop, number=hopnum)
            props.save()
        hopnum-=1
    return path



def preset_cloudnodes():
    """Hard code some of the cloud node for different gridFTP locations.
    """
    clouds = {}
    clouds['anl'] = {'node': create_cloud_node('anl.gov', 'anl', '140.221.0.0/16')}
    clouds['nersc'] = {'node': create_cloud_node('nersc.gov', 'nersc', '128.55.0.0/16')}
    clouds['uchicago'] = {'node': create_cloud_node('ci.uchicago.edu','uchicago', '128.135.0.0/16')}
    clouds['ncsa'] = {'node': create_cloud_node('ncsa.illinois.edu', 'ncsa', '141.142.0.0/16')}
    clouds['iu'] = {'node': create_cloud_node('iu.edu', 'iu', '129.79.0.0/16')}
    clouds['ucar'] = {'node': create_cloud_node('ucar.edu', 'ucar', '128.117.0.0/16')}
    clouds['tacc'] = {'node': create_cloud_node('tacc.utexas.edu', 'tacc', '129.114.0.0/17')}
    clouds['psc'] = {'node': create_cloud_node('psc.edu', 'psc', '128.182.0.0/16')}
    clouds['purdue'] = {'node': create_cloud_node('purdue.edu', 'purdue', '128.211.0.0/16')}
    clouds['vpac'] = {'node': create_cloud_node('vpac.org', 'vpac', '202.158.218.0/24')}
    
    clouds['ivec'] = {'node': create_cloud_node('ivec.org', 'ivec', '192.65.130.0/24')}
    clouds['lbl'] = {'node': create_cloud_node('lbl.gov', 'lbl', '131.243.0.0/16')}
    clouds['olemiss'] = {'node': create_cloud_node('olemiss.edu', 'olemiss', '130.74.0.0/16')}
    clouds['ornl'] = {'node': create_cloud_node('ornl.gov', 'ornl', '160.91.0.0/16')}
    clouds['loni'] = {'node': create_cloud_node('loni.org', 'loni', '208.100.64.0/18')}
    clouds['unh'] = {'node': create_cloud_node('unh.edu', 'unh', '132.177.0.0/16')}
    
    ################## Trace Route Ports ############################
    clouds['anl']['tracePort'] = ['anl-owamp.es.net', 'anl-pt1.es.net']
    clouds['nersc']['tracePort'] = ['nersc-owamp.es.net', 'nersc-pt1.es.net']
    clouds['uchicago']['tracePort'] = ['anl-owamp.es.net', 'anl-pt1.es.net']
    clouds['ncsa']['tracePort'] = ['star-owamp.es.net', 'star-pt1.es.net']
    clouds['iu']['tracePort'] = ['chic-owamp.es.net', 'chic-pt1.es.net']
    clouds['tacc']['tracePort'] = ['chic-owamp.es.net', 'chic-pt1.es.net']
    clouds['ucar']['tracePort'] = ['denv-owamp.es.net', 'denv-pt1.es.net']
    clouds['psc']['tracePort'] = ['aofa-owamp.es.net', 'aofa-pt1.es.net']
    clouds['purdue']['tracePort'] = ['star-owamp.es.net', 'star-pt1.es.net']
    clouds['vpac']['tracePort'] = ['pnwg-owamp.es.net', 'pnwg-pt1.es.net']
    
    clouds['ivec']['tracePort'] = ['pnwg-owamp.es.net', 'pnwg-pt1.es.net']
    clouds['lbl']['tracePort'] = ['lbl-pt1.es.net']
    clouds['olemiss']['tracePort'] = ['chic-owamp.es.net', 'chic-pt1.es.net']
    clouds['ornl']['tracePort'] = ['nash-owamp.es.net', 'nash-pt1.es.net']
    clouds['loni']['tracePort'] = ['chic-owamp.es.net', 'chic-pt1.es.net']
    clouds['unh']['tracePort'] = ['bost-owamp.es.net', 'bost-pt1.es.net']
    
    ################## BWCTL Ports ####################################
    clouds['anl']['bwctlPort'] = ['anl-pt1.es.net']
    clouds['nersc']['bwctlPort'] = ['nersc-pt1.es.net']
    clouds['uchicago']['bwctlPort'] = ['anl-pt1.es.net']
    clouds['ncsa']['bwctlPort'] = ['star-pt1.es.net']
    clouds['iu']['bwctlPort'] = ['chic-pt1.es.net']
    clouds['tacc']['bwctlPort'] = ['chic-pt1.es.net']
    clouds['ucar']['bwctlPort'] = ['denv-pt1.es.net']
    clouds['psc']['bwctlPort'] = ['aofa-pt1.es.net']
    clouds['purdue']['bwctlPort'] = ['star-pt1.es.net']
    clouds['vpac']['bwctlPort'] = ['pnwg-pt1.es.net']
    
    clouds['ivec']['bwctlPort'] = ['pnwg-pt1.es.net']
    clouds['lbl']['bwctlPort'] = ['lbl-pt1.es.net']
    clouds['olemiss']['bwctlPort'] = ['chic-pt1.es.net']
    clouds['ornl']['bwctlPort'] = ['nash-pt1.es.net']
    clouds['loni']['bwctlPort'] = ['chic-pt1.es.net']
    clouds['unh']['bwctlPort'] = ['bost-pt1.es.net']
    
    ################## OWAMP Ports ####################################
    clouds['anl']['owampPort'] = ['anl-owamp.es.net']
    clouds['nersc']['owampPort'] = ['nersc-owamp.es.net']
    clouds['uchicago']['owampPort'] = []
    clouds['ncsa']['owampPort'] = ['star-owamp.es.net']
    clouds['iu']['owampPort'] = []
    clouds['tacc']['owampPort'] = []
    clouds['ucar']['owampPort'] = ['denv-owamp.es.net']
    clouds['psc']['owampPort'] = ['aofa-owamp.es.net']
    clouds['purdue']['owampPort'] = ['star-owamp.es.net']
    clouds['vpac']['owampPort'] = ['pnwg-owamp.es.net']
    
    clouds['ivec']['owampPort'] = ['pnwg-owamp.es.net']
    clouds['lbl']['owampPort'] = ['lbl-diskpt1.es.net']
    clouds['olemiss']['owampPort'] = ['chic-owamp.es.net']
    clouds['ornl']['owampPort'] = ['nash-owamp.es.net']
    clouds['loni']['owampPort'] = ['chic-owamp.es.net']
    clouds['unh']['owampPort'] = ['bost-owamp.es.net']
    
    
    for c in clouds:
        cloud_traceroute(clouds[c]['node'], clouds[c]['tracePort'])
        cloud_bwctl(clouds[c]['node'], clouds[c]['bwctlPort'])
        cloud_owamp(clouds[c]['node'], clouds[c]['owampPort'])
         
    return clouds



def compute_routes(clouds):
    """Find all traceroutes between cloud nodes.
    
    clouds should be in the form
        clouds['node']= Node Object of Type cloud
    """
    for s in clouds:
        clouds[s]['routes'] = {}
        print "clouds[%s]['routes'] = {}" % s
        for d in clouds:
            if s != d:
                try:
                    path = find_traceroute(clouds[s]['node'], clouds[d]['node'])
                    clouds[s]['routes'][d] = path
                    print "clouds['%s']['routes']['%s'] = %s" % (s, d, path)
                except Exception, ex:
                    print "clouds['%s']['routes']['%s'] = %s # couldn't find: %s" % (s, d, None, ex)
    return clouds


def preset_cloudroutes(clouds):
    """
    output of a prerun of compute_routes(clouds) to save time
    """
    clouds['loni']['routes'] = {}
    clouds['loni']['routes']['ivec'] = None
    clouds['loni']['routes']['vpac'] = None
    clouds['loni']['routes']['psc'] = None
    clouds['loni']['routes']['purdue'] = None
    clouds['loni']['routes']['anl'] = None
    clouds['loni']['routes']['nersc'] = None
    clouds['loni']['routes']['uchicago'] = None
    clouds['loni']['routes']['iu'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['loni']['routes']['lbl'] = None
    clouds['loni']['routes']['ornl'] = None
    clouds['loni']['routes']['ucar'] = None
    clouds['loni']['routes']['unh'] = None
    clouds['loni']['routes']['olemiss'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['loni']['routes']['tacc'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['loni']['routes']['ncsa'] = None
    clouds['ivec']['routes'] = {}
    clouds['ivec']['routes']['loni'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ivec']['routes']['vpac'] = None
    clouds['ivec']['routes']['psc'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['ivec']['routes']['purdue'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['ivec']['routes']['anl'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['ivec']['routes']['nersc'] = ['198.129.254.53', '134.55.221.45', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['ivec']['routes']['uchicago'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['ivec']['routes']['iu'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ivec']['routes']['lbl'] = None
    clouds['ivec']['routes']['ornl'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.219.137', '198.124.252.146']
    clouds['ivec']['routes']['ucar'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '198.129.252.45']
    clouds['ivec']['routes']['unh'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['ivec']['routes']['olemiss'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ivec']['routes']['tacc'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ivec']['routes']['ncsa'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['vpac']['routes'] = {}
    clouds['vpac']['routes']['loni'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['vpac']['routes']['ivec'] = ['198.129.254.53', '198.129.254.54'] 
    clouds['vpac']['routes']['psc'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['vpac']['routes']['purdue'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['vpac']['routes']['anl'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['vpac']['routes']['nersc'] = ['198.129.254.53', '134.55.221.45', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['vpac']['routes']['uchicago'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['vpac']['routes']['iu'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['vpac']['routes']['lbl'] = None
    clouds['vpac']['routes']['ornl'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.219.137', '198.124.252.146']
    clouds['vpac']['routes']['ucar'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '198.129.252.45']
    clouds['vpac']['routes']['unh'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['vpac']['routes']['olemiss'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['vpac']['routes']['tacc'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['vpac']['routes']['ncsa'] = ['198.129.254.53', '134.55.220.61', '134.55.40.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['psc']['routes'] = {}
    clouds['psc']['routes']['loni'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['psc']['routes']['ivec'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['psc']['routes']['vpac'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['psc']['routes']['purdue'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.207.34', '198.124.252.106']
    clouds['psc']['routes']['anl'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.220.38', '198.124.252.97']
    clouds['psc']['routes']['nersc'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['psc']['routes']['uchicago'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.220.38', '198.124.252.97']
    clouds['psc']['routes']['iu'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['psc']['routes']['lbl'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['psc']['routes']['ornl'] = ['198.124.238.61', '134.55.218.77', '134.55.221.5', '134.55.220.46', '198.124.252.146']
    clouds['psc']['routes']['ucar'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['psc']['routes']['unh'] = ['198.124.238.61', '134.55.41.121', '198.124.238.58']
    clouds['psc']['routes']['olemiss'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['psc']['routes']['tacc'] = ['198.124.238.61', '134.55.41.121', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['psc']['routes']['ncsa'] = None # couldn't find: 
    clouds['purdue']['routes'] = {}
    clouds['purdue']['routes']['loni'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['purdue']['routes']['ivec'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['purdue']['routes']['vpac'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['purdue']['routes']['psc'] = ['198.124.252.105', '134.55.207.33', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['purdue']['routes']['anl'] = ['198.124.252.105', '134.55.219.53', '198.124.252.97']
    clouds['purdue']['routes']['nersc'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['purdue']['routes']['uchicago'] = ['198.124.252.105', '134.55.219.53', '198.124.252.97']
    clouds['purdue']['routes']['iu'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['purdue']['routes']['lbl'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['purdue']['routes']['ornl'] = ['198.124.252.105', '134.55.207.33', '134.55.219.137', '198.124.252.146']
    clouds['purdue']['routes']['ucar'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['purdue']['routes']['unh'] = ['198.124.252.105', '134.55.207.33', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['purdue']['routes']['olemiss'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['purdue']['routes']['tacc'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['purdue']['routes']['ncsa'] = ['198.124.252.105', '198.124.252.106']
    clouds['anl']['routes'] = {}
    clouds['anl']['routes']['loni'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['anl']['routes']['ivec'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['anl']['routes']['vpac'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['anl']['routes']['psc'] = ['198.124.252.98', '134.55.220.37', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['anl']['routes']['purdue'] = ['198.124.252.98', '134.55.219.54', '198.124.252.106']
    clouds['anl']['routes']['nersc'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['anl']['routes']['uchicago'] = ['198.124.252.98', '198.124.252.97']
    clouds['anl']['routes']['iu'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['anl']['routes']['lbl'] = None
    clouds['anl']['routes']['ornl'] = ['198.124.252.98', '134.55.220.37', '134.55.219.137', '198.124.252.146']
    clouds['anl']['routes']['ucar'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['anl']['routes']['unh'] = ['198.124.252.98', '134.55.220.37', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['anl']['routes']['olemiss'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['anl']['routes']['tacc'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['anl']['routes']['ncsa'] = ['198.124.252.98', '134.55.219.54', '198.124.252.106']
    clouds['nersc']['routes'] = {}
    clouds['nersc']['routes']['loni'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['nersc']['routes']['ivec'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.221.46', '198.129.254.54']
    clouds['nersc']['routes']['vpac'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.221.46', '198.129.254.54']
    clouds['nersc']['routes']['psc'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['nersc']['routes']['purdue'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['nersc']['routes']['anl'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['nersc']['routes']['uchicago'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['nersc']['routes']['iu'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['nersc']['routes']['lbl'] = None
    clouds['nersc']['routes']['ornl'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.38.185', '134.55.220.150', '134.55.39.106', '134.55.220.46', '198.124.252.146']
    clouds['nersc']['routes']['ucar'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '198.129.252.45']
    clouds['nersc']['routes']['unh'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['nersc']['routes']['olemiss'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['nersc']['routes']['tacc'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['nersc']['routes']['ncsa'] = ['198.129.254.33', '134.55.217.21', '134.55.219.78', '134.55.217.18', '134.55.217.10', '134.55.220.49', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['uchicago']['routes'] = {}
    clouds['uchicago']['routes']['loni'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['uchicago']['routes']['ivec'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['uchicago']['routes']['vpac'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['uchicago']['routes']['psc'] = ['198.124.252.98', '134.55.220.37', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['uchicago']['routes']['purdue'] = ['198.124.252.98', '134.55.219.54', '198.124.252.106']
    clouds['uchicago']['routes']['anl'] = ['198.124.252.98', '198.124.252.97']
    clouds['uchicago']['routes']['nersc'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['uchicago']['routes']['iu'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['uchicago']['routes']['lbl'] = None
    clouds['uchicago']['routes']['ornl'] = ['198.124.252.98', '134.55.220.37', '134.55.219.137', '198.124.252.146']
    clouds['uchicago']['routes']['ucar'] = ['198.124.252.98', '134.55.220.37', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['uchicago']['routes']['unh'] = ['198.124.252.98', '134.55.220.37', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['uchicago']['routes']['olemiss'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['uchicago']['routes']['tacc'] = ['198.124.252.98', '134.55.220.37', '198.124.252.154']
    clouds['uchicago']['routes']['ncsa'] = ['198.124.252.98', '134.55.219.54', '198.124.252.106']
    clouds['iu']['routes'] = {}
    clouds['iu']['routes']['loni'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['iu']['routes']['ivec'] = None
    clouds['iu']['routes']['vpac'] = None
    clouds['iu']['routes']['psc'] = None
    clouds['iu']['routes']['purdue'] = None
    clouds['iu']['routes']['anl'] = None
    clouds['iu']['routes']['nersc'] = None
    clouds['iu']['routes']['uchicago'] = None
    clouds['iu']['routes']['lbl'] = None
    clouds['iu']['routes']['ornl'] = None
    clouds['iu']['routes']['ucar'] = None
    clouds['iu']['routes']['unh'] = None
    clouds['iu']['routes']['olemiss'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['iu']['routes']['tacc'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['iu']['routes']['ncsa'] = None
    clouds['lbl']['routes'] = {}
    clouds['lbl']['routes']['loni'] = None
    clouds['lbl']['routes']['ivec'] = None
    clouds['lbl']['routes']['vpac'] = None
    clouds['lbl']['routes']['psc'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['lbl']['routes']['purdue'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['lbl']['routes']['anl'] = None
    clouds['lbl']['routes']['nersc'] = None
    clouds['lbl']['routes']['uchicago'] = None
    clouds['lbl']['routes']['iu'] = None
    clouds['lbl']['routes']['ornl'] = None
    clouds['lbl']['routes']['ucar'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['lbl']['routes']['unh'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['lbl']['routes']['olemiss'] = None
    clouds['lbl']['routes']['tacc'] = None
    clouds['lbl']['routes']['ncsa'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['ornl']['routes'] = {}
    clouds['ornl']['routes']['loni'] = ['134.55.215.81', '134.55.219.138', '198.124.252.154']
    clouds['ornl']['routes']['ivec'] = ['134.55.215.81', '134.55.219.138', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ornl']['routes']['vpac'] = ['134.55.215.81', '134.55.219.138', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ornl']['routes']['psc'] = ['134.55.215.81', '134.55.220.45', '134.55.221.6', '134.55.218.78', '198.124.238.62']
    clouds['ornl']['routes']['purdue'] = ['134.55.215.81', '134.55.219.138', '134.55.207.34', '198.124.252.106']
    clouds['ornl']['routes']['anl'] = ['134.55.215.81', '134.55.219.138', '134.55.220.38', '198.124.252.97']
    clouds['ornl']['routes']['nersc'] = ['134.55.215.81', '134.55.220.45', '134.55.39.105', '134.55.220.149', '134.55.38.186', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['ornl']['routes']['uchicago'] = ['134.55.215.81', '134.55.219.138', '134.55.220.38', '198.124.252.97']
    clouds['ornl']['routes']['iu'] = ['134.55.215.81', '134.55.219.138', '198.124.252.154']
    clouds['ornl']['routes']['lbl'] = None
    clouds['ornl']['routes']['ucar'] = ['134.55.215.81', '134.55.219.138', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['ornl']['routes']['unh'] = ['134.55.215.81', '134.55.220.45', '134.55.221.6', '134.55.218.78', '134.55.41.121', '198.124.238.58']
    clouds['ornl']['routes']['olemiss'] = ['134.55.215.81', '134.55.219.138', '198.124.252.154']
    clouds['ornl']['routes']['tacc'] = ['134.55.215.81', '134.55.219.138', '198.124.252.154']
    clouds['ornl']['routes']['ncsa'] = ['134.55.215.81', '134.55.219.138', '134.55.207.34', '198.124.252.106']
    clouds['ucar']['routes'] = {}
    clouds['ucar']['routes']['loni'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ucar']['routes']['ivec'] = ['198.129.252.46', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ucar']['routes']['vpac'] = ['198.129.252.46', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ucar']['routes']['psc'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['ucar']['routes']['purdue'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['ucar']['routes']['anl'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['ucar']['routes']['nersc'] = ['198.129.252.46', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['ucar']['routes']['uchicago'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.220.38', '198.124.252.97']
    clouds['ucar']['routes']['iu'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ucar']['routes']['lbl'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['ucar']['routes']['ornl'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.219.137', '198.124.252.146']
    clouds['ucar']['routes']['unh'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['ucar']['routes']['olemiss'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ucar']['routes']['tacc'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '198.124.252.154']
    clouds['ucar']['routes']['ncsa'] = ['198.129.252.46', '134.55.209.46', '134.55.221.58', '134.55.207.34', '198.124.252.106']
    clouds['unh']['routes'] = {}
    clouds['unh']['routes']['loni'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['unh']['routes']['ivec'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['unh']['routes']['vpac'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['unh']['routes']['psc'] = ['198.124.238.57', '134.55.41.122', '198.124.238.62']
    clouds['unh']['routes']['purdue'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.207.34', '198.124.252.106']
    clouds['unh']['routes']['anl'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.220.38', '198.124.252.97']
    clouds['unh']['routes']['nersc'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['unh']['routes']['uchicago'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.220.38', '198.124.252.97']
    clouds['unh']['routes']['iu'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['unh']['routes']['lbl'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['unh']['routes']['ornl'] = ['198.124.238.57', '134.55.41.122', '134.55.218.77', '134.55.221.5', '134.55.220.46', '198.124.252.146']
    clouds['unh']['routes']['ucar'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['unh']['routes']['olemiss'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['unh']['routes']['tacc'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '198.124.252.154']
    clouds['unh']['routes']['ncsa'] = ['198.124.238.57', '134.55.41.145', '134.55.217.54', '134.55.207.34', '198.124.252.106']
    clouds['olemiss']['routes'] = {}
    clouds['olemiss']['routes']['loni'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['olemiss']['routes']['ivec'] = None
    clouds['olemiss']['routes']['vpac'] = None
    clouds['olemiss']['routes']['psc'] = None
    clouds['olemiss']['routes']['purdue'] = None
    clouds['olemiss']['routes']['anl'] = None
    clouds['olemiss']['routes']['nersc'] = None
    clouds['olemiss']['routes']['uchicago'] = None
    clouds['olemiss']['routes']['iu'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['olemiss']['routes']['lbl'] = None
    clouds['olemiss']['routes']['ornl'] = None
    clouds['olemiss']['routes']['ucar'] = None
    clouds['olemiss']['routes']['unh'] = None
    clouds['olemiss']['routes']['tacc'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['olemiss']['routes']['ncsa'] = None
    clouds['tacc']['routes'] = {}
    clouds['tacc']['routes']['loni'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['tacc']['routes']['ivec'] = None
    clouds['tacc']['routes']['vpac'] = None
    clouds['tacc']['routes']['psc'] = None
    clouds['tacc']['routes']['purdue'] = None
    clouds['tacc']['routes']['anl'] = None
    clouds['tacc']['routes']['nersc'] = None
    clouds['tacc']['routes']['uchicago'] = None
    clouds['tacc']['routes']['iu'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['tacc']['routes']['lbl'] = None
    clouds['tacc']['routes']['ornl'] = None
    clouds['tacc']['routes']['ucar'] = None
    clouds['tacc']['routes']['unh'] = None
    clouds['tacc']['routes']['olemiss'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['tacc']['routes']['ncsa'] = None
    clouds['ncsa']['routes'] = {}
    clouds['ncsa']['routes']['loni'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['ncsa']['routes']['ivec'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ncsa']['routes']['vpac'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.40.45', '134.55.220.62', '198.129.254.54']
    clouds['ncsa']['routes']['psc'] = ['198.124.252.105', '134.55.207.33', '134.55.217.53', '134.55.41.146', '134.55.41.122', '198.124.238.62']
    clouds['ncsa']['routes']['purdue'] = None
    clouds['ncsa']['routes']['anl'] = ['198.124.252.105', '134.55.219.53', '198.124.252.97']
    clouds['ncsa']['routes']['nersc'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '134.55.220.50', '134.55.217.9', '134.55.217.17', '134.55.219.77', '134.55.217.22', '198.129.254.34']
    clouds['ncsa']['routes']['uchicago'] = ['198.124.252.105', '134.55.219.53', '198.124.252.97']
    clouds['ncsa']['routes']['iu'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['ncsa']['routes']['lbl'] = None # couldn't find: EndPointPair matching query does not exist.
    clouds['ncsa']['routes']['ornl'] = ['198.124.252.105', '134.55.207.33', '134.55.219.137', '198.124.252.146']
    clouds['ncsa']['routes']['ucar'] = ['198.124.252.105', '134.55.207.33', '134.55.221.57', '134.55.209.45', '198.129.252.45']
    clouds['ncsa']['routes']['unh'] = ['198.124.252.105', '134.55.207.33', '134.55.217.53', '134.55.41.146', '198.124.238.58']
    clouds['ncsa']['routes']['olemiss'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    clouds['ncsa']['routes']['tacc'] = ['198.124.252.105', '134.55.207.33', '198.124.252.154']
    
    return clouds

def create_ep_node(endpoint):
    """ Creates a special node of type endpoint.
    """
    parts = endpoints.split('.', 1)
    name = parts[0]
    domain = parts[1]
    
    ep = Node.objects.get_or_create(unis_id="urn:ogf:network:domain=%s:node=%s" % (domain, name))[0]
    ep.type = 'endpoint'
    ep.save()
    return cloud
    

def preset_endpoints():
    endpoints[0] = {'node': create_ep_node('arcs-df.ivec.org')}
    endpoints[1] = {'node': create_ep_node('arcs-df.vpac.org')}
    endpoints[2] = {'node': create_ep_node('coltrane.lbl.gov')}
    endpoints[3] = {'node': create_ep_node('dragon.cs.olemiss.edu')}
    endpoints[4] = {'node': create_ep_node('dtn01.ccs.ornl.gov')}
    endpoints[5] = {'node': create_ep_node('dtn01.nersc.gov')}
    endpoints[6] = {'node': create_ep_node('endpoint1.tutorial.globus.org')}
    endpoints[7] = {'node': create_ep_node('endpoint1.tutorial.globusonline.org')}
    endpoints[8] = {'node': create_ep_node('endpoint2.tutorial.globus.org')}
    endpoints[9] = {'node': create_ep_node('endpoint2.tutorial.globusonline.org')}
    endpoints[10] = {'node': create_ep_node('gridftp-qb.loni-lsu.teragrid.org')}
    endpoints[11] = {'node': create_ep_node('gridftp-test.ivec.org')}
    endpoints[12] = {'node': create_ep_node('gridftp.bigred.iu.teragrid.org')}
    endpoints[13] = {'node': create_ep_node('gridftp.frost.ncar.teragrid.org')}
    endpoints[14] = {'node': create_ep_node('gridftp.lonestar.tacc.teragrid.org')}
    endpoints[15] = {'node': create_ep_node('gridftp.nics.teragrid.org')}
    endpoints[16] = {'node': create_ep_node('gridftp.pads.ci.uchicago.edu')}
    endpoints[17] = {'node': create_ep_node('gridftp.ranger.tacc.teragrid.org')}
    endpoints[18] = {'node': create_ep_node('gs1.intrepid.alcf.anl.gov')}
    endpoints[19] = {'node': create_ep_node('gs2.intrepid.alcf.anl.gov')}
    endpoints[20] = {'node': create_ep_node('mss.ncsa.teragrid.org')}
    endpoints[21] = {'node': create_ep_node('never-1.ci.uchicago.edu')}
    endpoints[22] = {'node': create_ep_node('rebel.cs.unh.edu')}
    endpoints[23] = {'node': create_ep_node('tg-gridftp.lonestar.tacc.teragrid.org')}
    endpoints[24] = {'node': create_ep_node('vetswebdev.ucar.edu')}
    endpoints[25] = {'node': create_ep_node('vm-125-67.ci.uchicago.edu')}
    endpoints[26] = {'node': create_ep_node('xen-d.vpac.org')}
    return endpoints

def create_paths(clouds):
    """ Create UINS paths for the routes
    """
    for src in clouds:
        clouds[src]['paths'] = {}
        for dst in clouds[src]['routes']:
            if clouds[src]['routes'][dst] is not None:
                clouds[src]['paths'][dst] = create_path("%s2%s" % (src, dst), clouds[src]['node'], clouds[dst]['node'], clouds[src]['routes'][dst])
            else:
                clouds[src]['paths'][dst] = None
    return clouds

def clean_ep_nodes():
    Node.objects.filter(type='endpoint').delete()

def clean_cloud_nodes():
    Node.objects.filter(type='cloud').delete()
    Path.objects.filter().delete()
    Link.objects.filter(unis_id__contains='->').delete()

# Load the basic information for SC10 demo
clean_cloud_nodes()
clouds = preset_cloudnodes()
clouds = preset_cloudroutes(clouds)
clouds = create_paths(clouds)

#clean_ep_nodes()
#eps = preset_endpoints()

