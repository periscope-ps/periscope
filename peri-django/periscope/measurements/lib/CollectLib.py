#!/usr/bin/env python

# TODO(AH): MARK FOR REMOVAL
# TODO(AH): Some functions better placed at the topology app lib

"""Auxilary functions for collection services from deployed perfsonar cloud.
"""

import logging
import httplib
import socket
import radix
from urlparse import urlparse

from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from periscope.topology.models import Address
from periscope.topology.models import CloudNodeProperties
from periscope.topology.models import Description
from periscope.topology.models import EventType
from periscope.topology.models import EndPointPair
from periscope.topology.models import Name
from periscope.topology.models import NetworkObjectNames
from periscope.topology.models import NetworkObjectDescriptions
from periscope.topology.models import Node
from periscope.topology.models import NodeAddresses
from periscope.topology.models import Service
from periscope.topology.models import Port
from periscope.topology.models import PortAddresses
from periscope.topology.models import psServiceProperties
from periscope.topology.models import psServicePropertiesEventTypes
from periscope.topology.models import psServiceWatchList

from periscope.measurements.lib.SimpleClient import SimpleClient
from periscope.measurements.models import DNSCache

logger = logging.getLogger('periscope')

# Cache to save lookup times
get_host_by_addr_cache = {}
def get_host_by_addr(ip, cache=False):
    """Reverse DNS lookup for addresses without hostnames
    """
    cache = DNSCache.objects.filter(ip=ip)
    if len(cache) > 0:
        return cache.values_list('hostname')[0][0]
        
    try:
        host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host = None
    logger.info("Reverse DNS lookup for %s returned '%s'" % (ip, host))
    
    d = DNSCache(hostname=host, ip=ip)
    d.save()
        
    return host


get_host_ips_cache = {}
def get_host_ips(host, cache=True):
    """Get a list of IP addresses for a given host.
    """
    ips = DNSCache.objects.filter(hostname=host)
    if len(ips) > 0:
        ret = []
        for i in ips:
            ret.append(i.ip)
        return ret
    
    try:
        info = socket.getaddrinfo(host, None)
    except socket.gaierror:
        logger.warning("Hostname %s doesn't have an IP address" % host)
        info = []
    
    ips = []
    for i in info:
        if i[4][0] not in ips:
            # Ignore IPv6
            if len(i[4][0]) > 16:
                continue
            ips.append(i[4][0])
            d = DNSCache(hostname=host, ip=i[4][0])
            d.save()
    
    return ips


def validIP4(address):
    """Return True if the input is a valid IP4 address
    """
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        try:
            if not 0 <= int(item) <= 255:
                return False
        except:
            return False
    return True


def find_node_by_address(address):
    """Deep search for the node address or one of it's port and it does
    DNS lookup and reverse DNS lookup as well
    """
    # Does the address exists at all
    addresses = Address.objects.filter(value=address)
    
    # ok if not find DNS or Reverse DNS
    if len(addresses) == 0:
        if validIP4(address):
            alter_addresses = [get_host_by_addr(address)]
        else:
            alter_addresses = get_host_ips(address)
        
        # Try find again
        while len(alter_addresses) > 0 and len(addresses) == 0:
            addresses = Address.objects.filter(value=alter_addresses.pop())
    
    # The address is not known, return None
    if len(addresses) == 0:
        return None
     
    for i in range(len(addresses)):
        addr = addresses[i]
        # Attemp 1 direct node address
        nodes = addr.node_set.all()
        if len(nodes) > 0:
            return nodes[0]
            
        # Attemp 2 direct a port address
        ports = addr.port_set.all()
        if len(ports) > 0:
            node = ports[0].parent.toRealType()
            if isinstance(node, Node):
                return node
        
    # failed to find node with the same address return None
    return None



@transaction.commit_on_success
def create_node_by_address(address):
    """ Creates new node with the given address.
    Return a refence to the node object if the node already exists.
    
    If the node has IP address, a port is created with the ip address
    """
    node = find_node_by_address(address)
    if node is not None:
        return node
        
    # creating new node is needed
    if validIP4(address):
        hostname = get_host_by_addr(address, False)
        ips = [address]
    else:
        hostname = address
        ips = get_host_ips(address, False)
    
    node = Node()
    
    # if the address cannot be mapped to DNS name use '*' as domain 
    if hostname is None:
        nodeName = ips[0]
        domainName = '*'
    else:
        nodeName = hostname.split('.')[0]
        domainName = hostname.replace(hostname.split('.')[0] + '.', '')
        
    node.unis_id = "urn:ogf:network:domain=%s:node=%s" % (domainName, nodeName)
    node.save()
    
    if hostname is None:
        hostname = ips[0]
    name = NetworkObjectNames.objects.create(name = Name.objects.create(value=hostname), networkobject=node)
    name.save()
    
    host = NodeAddresses.objects.create(node=node, address = Address.objects.create(value=hostname,type='hostname'))
    host.save()
    for ip in  ips:
        port = Port(parent=node, unis_id=node.unis_id+":port:%s" % ip)
        port.parent = node
        port.save()
        portAddress = PortAddresses.objects.create(port=port, address = Address.objects.create(value=ip,type='ipv4'))
        portAddress.save()
        dns = get_host_by_addr(ip)
        if dns is not None:
            portAddress = PortAddresses.objects.create(port=port, address = Address.objects.create(value=dns,type='hostname'))
            portAddress.save()
        
    
    logger.info("New node '%s' is created" % node)
    return node
    

def get_service_accesspoint(service):
    """Return the accesspoint for a given service
    """
    return service.properties_bag.get(psserviceproperties__accessPoint__contains='//').psserviceproperties.accessPoint



@transaction.commit_on_success
def create_psservice(serviceName, accessPoint, serviceType, serviceDescription, eventTypes):
    """Create new service object in the topology model.
    If a service with the same accessPoint exists, this method will
    return a reference to the existing object.
    
    Arguments:
        serviceName: string name of the service
        accessPoint: string accessPoint of the service, must start with http: or https://
        serviceDescription:
        serviceType: e.g gLS, hLS, MA, MP
        eventTypes: dict or list of supported event types by the service
    """
    
    # Check if the service already exists
    services = Service.objects.filter(properties_bag__psserviceproperties__accessPoint=accessPoint)
    if len(services) > 0:
        return services[0]
    
    # Creating new service is needed
    g = urlparse(accessPoint)
    node = create_node_by_address(g.hostname)
    unis_id = "%s:port=%s:service=%s" % (node.unis_id, g.port, g.path)
    sresult = Service.objects.get_or_create(unis_id=unis_id)
    
    #service already exists but with different address
    if sresult[1] == False:
        return sresult[0]
    else:
        sresult[0].parent = node
        sresult[0].save()
        service = sresult[0]
        
    name = NetworkObjectNames.objects.create(name = Name.objects.create(value=accessPoint), networkobject=service)
    name.save()
    
    if serviceDescription is not None:
        desc = NetworkObjectDescriptions.objects.create(description = Description.objects.create(value=serviceDescription), networkobject=service)
        desc.save()
    
    
    # Creates a ps service properites bag for a service
    props = psServiceProperties()
    props.serviceName =  serviceName
    props.accessPoint =  accessPoint
    props.serviceType =  serviceType
    props.serviceDescription =  serviceDescription
    service.properties_bag.add(props)
    
    # Set the list of supported event types for a given psserviceproperties.
    for e in eventTypes:
        eresult = EventType.objects.get_or_create(value=e)
        if e[1] == True:
            eresult[0].save()
        eventprop = psServicePropertiesEventTypes.objects.create(psServiceProperties=props, eventtype=eresult[0])
        eventprop.save()
    
    logger.info("New service '%s' is created" % service)
    service.save()
    return service


def delete_services_by_type(serviceType):
    services = Service.objects.filter(properties_bag__psserviceproperties__serviceType=serviceType)
    for s in services:
        s.delete()


def delete_services_by_accesspoint(accessPoint):
    services = Service.objects.filter(properties_bag__psserviceproperties__accessPoint=accessPoint)
    for s in services:
        s.delete()


def create_endpoint(src, src_type, dst, dst_type):
    snode = create_node_by_address(src)
    dnode = create_node_by_address(dst)
    
    sport = snode.get_ports().filter(addresses__value=src)
    dport = dnode.get_ports().filter(addresses__value=dst)
    
    if len(sport) > 0:
        sport = sport[0]
    else: # No port is defined use the node as source
        raise Exception("Source port '%s' was not found" % src)
        sport = snode
        
    if len(dport) > 0:
        dport = dport[0]
    else: # No port is defined use the node as source
        raise Exception("Distination port '%s' was not found" % dst)
        dport = dnode
        
    
    eresult = EndPointPair.objects.get_or_create(src=sport, dst=dport)
    endpoint = eresult[0]
    
    if eresult[0] == True:
        logger.info("Creating Endpoint from '%s' to '%s'" % (src, dst))
        endpoint.src = sport
        endpoint.dst = dport
        endpoint.save()
        
    return endpoint



def find_endpoint_with_exact_src(src, eventType=None):
    """Find an endpoint with the exact sre address
    optional eventType will filter the endpoints based if there is a
    service that watchs this endpoint with the same eventType
    """
    node = find_node_by_address(src)
    endpoints = []
    if node is not None:
        endpoints = EndPointPair.objects.filter(src=node.networkobject_ptr)
        if eventType is None:
            return endpoints
        else:
            new_ends = []
            for e in endpoints:
                if isinstance(eventType, EventType):
                    event = eventType
                else:
                    event = EventType.objects.get(value=eventType)
                ctype = ContentType.objects.get_for_model(e)
                watchers = psServiceWatchList.objects.filter(objectID=e.id, objectType=ctype, eventType=event)
                if len(watchers) > 0:
                    new_ends.append(e)
            return new_ends
    else:
        return []


def find_endpoint_with_src(src, eventType=None):
    endpoints = find_endpoint_with_exact_src(src)
    if len(endpoints) > 0:
        return endpoints
     
    if validIP4(src) == True:
        host = get_host_by_addr(src)
        #ips = [src]
        ips = get_host_ips(host, cache=False)
        if src not in ips:
            ips.append(src)
    else:
        host = src
        ips = get_host_ips(src, cache=False)
    
    addresses = []
    # first try
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:3]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_src(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    # Second try with more ip range    
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:2]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_src(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    
    # Third try with more ip range    
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:1]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_src(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    return None
    


def find_endpoint_with_exact_dst(dst, eventType=None):
    """Find an endpoint with the exact dst address
    optional eventType will filter the endpoints based if there is a
    service that watchs this endpoint with the same eventType
    """
    node = find_node_by_address(dst)
    endpoints = []
    if node is not None:
        endpoints = EndPointPair.objects.filter(dst=node.networkobject_ptr)
        if eventType is None:
            return endpoints
        else:
            new_ends = []
            for e in endpoints:
                if isinstance(eventType, EventType):
                    event = eventType
                else:
                    event = EventType.objects.get(value=eventType)
                ctype = ContentType.objects.get_for_model(e)
                watchers = psServiceWatchList.objects.filter(objectID=e.id, objectType=ctype, eventType=event)
                if len(watchers) > 0:
                    new_ends.append(e)
            return new_ends
    else:
        return []


def find_endpoint_with_dst(dst, eventType=None):
    endpoints = find_endpoint_with_exact_dst(dst)
    if len(endpoints) > 0:
        return endpoints
     
    if validIP4(dst) == True:
        host = get_host_by_addr(dst)
        #ips = [src]
        ips = get_host_ips(host, cache=False)
        if dst not in ips:
            ips.append(dst)
    else:
        host = dst
        ips = get_host_ips(dst, cache=False)
    
    addresses = []
    # first try
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:3]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_dst(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    # Second try with more ip range    
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:2]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_dst(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    
    # Third try with more ip range    
    for ip in ips:
        addresses = Address.objects.filter(value__startswith='.'.join(ip.split('.')[0:1]))
    
    for a in addresses:
        ends = find_endpoint_with_exact_dst(a.value, eventType)
        for e in ends:
            endpoints.append(e)
    
    # found endpoint no more is needed        
    if len(endpoints) > 0:
        return endpoints
    
    return None



def find_endpoints(src, dst, eventType=None):
    srcs = find_endpoint_with_src(src, eventType)
    dsts = find_endpoint_with_dst(dst, eventType)
    
    result = {}
    result['endpoints'] = None
    if srcs is None:
        result['status'] = 'fail'
        result['msg'] = "src is not found %s" % src
        return result
        
    if dsts is None:
        result['status'] = 'fail'
        result['msg'] = "dst is not found %s" % src
        return result
        
    ends = []
    for s in srcs:
        for d in dsts:
            if s == d:
                ends.append(s)
                break
    
    if len(ends) > 0:
        result['status'] = 'success'
        result['msg'] = "found endpoints with one hop" 
        result['endpoints'] = ends
        return result
    else:
        result['status'] = 'fail'
        result['msg'] = "no match endpoints found" 
        result['endpoints'] = None
        return result
        
    # try 2 hops
    for s in srcs:
        for d in dsts:
            if s.dst == d.src:
                ends.append((s,d))
                break
    
    if len(ends) == 0:
        result['status'] = 'fail'
        result['msg'] = "no match endpoints found" 
        result['endpoints'] = None
        return result
    else:
        result['status'] = 'success'
        result['msg'] = "found endpoints with two hops" 
        result['endpoints'] = ends
        return result


def find_cloud(ip):
    """Returnd the cloud node that this port belongs to.
    """
    clouds = Node.objects.filter(type='cloud')
    rtree = radix.Radix()
    for cloud in clouds:
        cidr = CloudNodeProperties.objects.get(parent=cloud).CIDR
        rnode = rtree.add(cidr)
        rnode.data['node'] = cloud
    result = rtree.search_best(ip)
    if result is None:
        return None
    else:
        return result.data['node']


def get_events(sports, dports):
    """Helper function to get all supported events between two ports.
    """
    events = {}
    for sport in sports:
        for dport in dports:
            ends = EndPointPair.objects.filter(src__unis_id=sport.unis_id, dst__unis_id=dport.unis_id)
            
            if len(ends) > 0:
                e = ends[0]
                ctype = ContentType.objects.get_for_model(e)
                watchers = psServiceWatchList.objects.filter(objectID=e.id, objectType=ctype, service__properties_bag__psserviceproperties__serviceType='MA')
                for w in watchers:
                    if w.eventType.value not in events:
                        events[w.eventType.value] = {'endpoints': e, 'accessPoints':[]}
                    accessPoint = psServiceProperties.objects.get(parent=w.service).accessPoint
                    
                    if accessPoint not in events[w.eventType.value]['accessPoints']:
                        events[w.eventType.value]['accessPoints'].append(accessPoint)
    return events


def get_endpoints_info(src, dst, sports=None, dports=None):
    
    # first convert all addresses to ips
    if validIP4(src):
        src = src
    else:
        src = get_host_ips(src)[0]
    
    if validIP4(dst):
        dst = dst
    else:
        dst = get_host_ips(dst)[0]
    
    
    scloud = find_cloud(src)
    dcloud = find_cloud(dst)
    status = 'OK'
    msg = ''
    if scloud is None:
        status = 'FAIL'
        msg = "Source node's is not found"
    
    if dcloud is None:
        status = 'FAIL'
        msg = "Destination node's is not found"
    
    result = {'status':status, 'msg':msg}
    if status != 'OK':
        return results
    
    sprops = CloudNodeProperties.objects.get(parent=scloud)
    dprops = CloudNodeProperties.objects.get(parent=dcloud)
    if sports is None:
        sports = []
        if len(sprops.traceroute.all()) > 0 :
            sports += list(sprops.traceroute.all())
        if len(sprops.bwctl.all()) > 0 :
            sports += list(sprops.bwctl.all())
        if len(sprops.pinger.all()) > 0 :
            sports += list(sprops.pinger.all())
        #if len(sprops.owamp.all()) > 0 :
        #    sports += list(sprops.owamp.all())
    
    if dports is None:
        dports = []
        if len(dprops.traceroute.all()) > 0 :
            dports += list(dprops.traceroute.all())
        if len(dprops.bwctl.all()) > 0 :
            dports += list(dprops.bwctl.all())
        if len(dprops.pinger.all()) > 0 :
            dports += list(dprops.pinger.all())
        #if len(sprops.owamp.all()) > 0 :
        #    dports += list(sprops.owamp.all())
    
    events = get_events(sports, dports)
    # change endpoints from Objects to pair of endpoints
    for event in events:
        endpoint = events[event]['endpoints']
        src = endpoint.src.toRealType()
        srcAddress= src.addresses.filter(type='hostname')
        if len(srcAddress) == 0:
            srcAddress= src.addresses.filter(type='ipv4')
        srcAddress = srcAddress[0]
        
        dst = endpoint.dst.toRealType()
        dstAddress= dst.addresses.filter(type='hostname')
        if len(dstAddress) == 0:
            dstAddress= dst.addresses.filter(type='ipv4')
        dstAddress = dstAddress[0]
        events[event]['endpoints'] = [srcAddress.value, dstAddress.value]
    
    result = {'status':status, 'msg':msg, 'services':events}
    return result
                




# TODO: we need to merege it with the other 10 different versions!
def query_psservice(service, message, cert=None, key=None, useSSL=False):
    accessPoint = get_service_accesspoint(service)
    parse = urlparse(accessPoint)
    
    if cert is None and key is None:
        client = SimpleClient(host=parse.hostname, port=parse.port, uri=parse.path)
    else:
        client = SimpleClient(host=parse.hostname, port=parse.port, uri=parse.path,
                              cert=settings.SSL_CERT_FILE, key=settings.SSL_KEY_FILE)
        
    logger.info("Send query to: '%s'" % accessPoint) 
    response = client.send_request(message, useSSL=useSSL)
    logger.info("Received result from: '%s'" % accessPoint) 
    
    return response
