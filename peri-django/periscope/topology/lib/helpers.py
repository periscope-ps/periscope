"""
Unified perfSONAR data collector
"""

import logging
import socket
from urlparse import urlparse

from django.db import transaction
from django.db.models import Q

from psapi.utils.ipaddress import get_address_type

from periscope.topology.models import Address
from periscope.topology.models import Description
from periscope.topology.models import EndPointPair
from periscope.topology.models import EventType
from periscope.topology.models import NetworkObject
from periscope.topology.models import NetworkObjectDescriptions
from periscope.topology.models import NetworkObjectNames
from periscope.topology.models import Name
from periscope.topology.models import Node
from periscope.topology.models import NodeAddresses
from periscope.topology.models import Port
from periscope.topology.models import PortAddresses
from periscope.topology.models import psServicePropertiesEventTypes
from periscope.topology.models import psServiceWatchList
from periscope.topology.models import psServiceProperties
from periscope.topology.models import Service

from periscope.measurements.models import DNSCache

logger = logging.getLogger('periscope')


def reverse_dns(ipaddress, cache=True):
    """
    Reverse DNS lookup for addresses without hostnames
    
    if cache=True, lookup will use measurements.DNSCache for lookup first.
    in case of a miss, system's default DNS server will be used and the
    result will be store in the DNSCache for future lookups.
    
    see L{forward_dns}
    """
    cached = DNSCache.objects.filter(ip=ipaddress)
    if len(cached) > 0:
        return cached.values_list('hostname')[0][0]
    
    try:
        host = socket.gethostbyaddr(ipaddress)[0]
    except socket.herror:
        host = None
    logger.info("Reverse DNS lookup for %s returned '%s'" % (ipaddress, host))
    
    if cache:
        DNSCache.objects.create(hostname=host, ip=ipaddress)
    
    return host


@transaction.commit_manually
def forward_dns(host, cache=True):
    """
    Returns list of IP addresses for a given host.
    
    see: L{reverse_dns} for caching information
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
            ips.append(i[4][0])
            if cache:
                dns_cache = DNSCache(hostname=host, ip=i[4][0])
                dns_cache.save()
    transaction.commit()
    return ips


def create_node_by_address(address, dns_lookup=True):
    """
    Creates new node by it's address.
    
    See L{find_node_by_address} to make sure that there is no duplicates.
    
    @param address: IP address, hostname, DNS.
    @param dns_lookup: perform forward DNS and/or reverse DNS lookup.
    @type dns_lookup: boolean.
    
    @returns: L{periscope.topology.models.Node}
    """
    
    address_type = get_address_type(address)
    
    if address_type in ['ipv4', 'ipv6']:
        hostname = None
        ips = [address]        
    elif address_type in ['hostname', 'dns']:
        hostname = address
        ips = []
    else:
        raise ValueError('Address should be valid IP, DNS, or '
                'hostname, not %s' % address)
    
    if dns_lookup and not hostname:
        hostname = reverse_dns(address, True)
    
    if dns_lookup and not ips:
        ips = forward_dns(address, True)
    
    # if the address cannot be mapped to DNS name use '*' as domain 
    if hostname is None:
        node_n = ips[0]
        domain_n = '*'
    else:
        node_n = hostname.split('.')[0]
        domain_n = hostname.replace(hostname.split('.')[0] + '.', '')
    
    unis_id = "urn:ogf:network:domain=%s:node=%s" % (domain_n, node_n)
    node = Node.objects.create(unis_id=unis_id)
    
    if hostname:
        name = Name.objects.create(value=hostname, type='hostname')
        net_name = NetworkObjectNames(name=name, networkobject=node)
        net_name.save()
    
        addr = Address.objects.create(value=hostname,
                    type=get_address_type(hostname))
        net_addr = NodeAddresses(node=node, address=addr)
        net_addr.save()

    for ip_addr in ips:
        port = Port.objects.create(parent=node,
                unis_id=node.unis_id + ":port=%s" % ip_addr)
        addr = Address.objects.create(value=ip_addr,
                type=get_address_type(ip_addr))
        port_addr = PortAddresses(port=port, address=addr)
        port_addr.save()
        
        if dns_lookup:
            dns = reverse_dns(ip_addr)
            if dns:
                addr = Address.objects.create(value=dns, type='dns')
                port_addr = PortAddresses(port=port, address=addr)
                port_addr.save()
    
    logger.info("New node '%s' is created" % node.unis_id)
    return node


def find_node_by_address(address, dns_lookup=True):
    """
    Deep search for the node address or one of it's port and it does
    DNS lookup and reverse DNS lookup as well.
    
    @param address: IP address, hostname, DNS
    @param dns_lookup: perform forward DNS and/or reverse DNS lookup
    @type dns_lookup: boolean
    
    @returns: L{periscope.topology.models.Node}
    """
    
    address_type = get_address_type(address)
    
    if not dns_lookup:
        alter_addresses = []
    elif address_type == 'ipv4' or address_type == 'ipv6':
        hostname = reverse_dns(address)
        if hostname:
            alter_addresses = [hostname]
        else:
            alter_addresses = []
    else:
        alter_addresses = forward_dns(address)
    
    address_filter = Q(addresses__value=address)
    
    for alter_address in alter_addresses:
        address_filter |= Q(addresses__value=alter_address)
    
    nodes = Node.objects.filter(address_filter)
    
    if len(nodes) > 0:
        return nodes[0] 
    
    else: # Try with ports
        ports = Port.objects.filter(address_filter)
        if len(ports) == 0:
            return None
        else:
            return ports[0].parent.toRealType()


def create_port(node, address=None, address_type=None, ifaddress=None,
            ifname=None, unis_id=None):
    """
    Creates new UNIS Port instance
    
    @param node: Node object
    @param address: valid ipv4, ipv6, DNS (only if it has one IP address)
    @param address_type: optional srting ipv4,ipv6, DNS, URL, or hostname
    @param ifaddress: address with special schema for internal interface addressing
    @param ifname: port name
    @param unis_id: unique URN, otherwise it will generated based on node's unis_id
    
    @returns: Port instance
    """
    
    if not isinstance(node, NetworkObject):
        raise ValueError("node is not is instance of "
                    "NetworkObject: %s" % type(node))
    
    if get_address_type(address) == 'hostname':
        raise ValueError("Port cannot accept hostname address "
                    "unless it has only one IP address.")
    elif get_address_type(address) == 'dns':
        ips = forward_dns(address)
        if len(ips) != 1:
            raise ValueError("Port cannot accept DNS address "
                        "unless it has only one IP address.")
    
    if not unis_id:
        # Create new unis id
        unis_id = node.unis_id
        if ifname:
            unis_id += ":port=%s" % ifname
        elif ifaddress:
            unis_id += ":port=%s" % ifaddress
        elif address:
            unis_id += ":port=%s" % address
    
    # Create port and save it   
    port = Port.objects.create(parent=node, unis_id=unis_id)
    
    # Assign name to the port
    if ifname:
        NetworkObjectNames.objects.create(
            name=Name.objects.create(value=ifname, type='ifname'),
            networkobject=port)
        
    # save address
    if address:
        if address_type is None:
            address_type = get_address_type(address)
            address = Address.objects.create(value=address, type=address_type)
            PortAddresses.objects.create(port=port, address=address)
        if address_type == 'dns':
            ip_addr = forward_dns(address)[0]
            ip_type = get_address_type(ip_addr)
            address = Address.objects.create(value=ip_addr, type=ip_type)
            PortAddresses.objects.create(port=port, address=address)
    
    # Interface special address
    if ifaddress:
        ifaddress_type = 'ifaddress'
        address = Address.objects.create(value=ifaddress, type=ifaddress_type)
        PortAddresses.objects.create(port=port, address=address)
    
    logger.info("Port '%s' is created" % port.unis_id)
    
    return port


def find_port(address=None, hostname=None, ifaddress=None, ifname=None):
    """
    Finds port by combination of different parameters.
    
    If I{find_port} is invoked with I{ifaddress} and I{ifname},
    I{hostname} must be provided since I{ifaddress} and I{ifname}
    are not globally unique.
    
    @param address: First choice to use IP address or DNS
    @param hostname: trys to find Node by hostname and then find port within the node's ports
    @param ifaddress: if a port has address scheme different than IP or DNS (hostname must be used)
    @param ifname: port name (hostname must be used)
    
    @returns: None, or L{periscope.topology.models.Port}
    """
    
    if not address and not (hostname and (ifaddress or ifname)):
        error = "address or hostname with ifaddress or ifname must be defined"
        raise ValueError(error)
    
    if address:
        ports = Port.objects.filter(addresses__value=address)
    else:
        ports = Port.objects.all()
    
    if hostname:
        ports = ports.filter(parent__names__value=hostname)
    
    if ifname:
        ports = ports.filter(names__value=ifname)
    if ifaddress:
        ports = ports.filter(addresses__value=ifaddress)
    
    if ports.count() == 1:
        return ports[0]
    elif ports.count() > 1:
        raise ValueError("Multiple ports were found: %s" % ports)
    elif ports.count() == 0:
        return None


def create_endpoint(src, dst):
    """
    Creates L{periscope.topology.models.EndPointPair} from source
    and destination addresses.
    
    This function creates endpoints between two ports only. UNIS allow
    endpoints between two nodes as well, but using two ports will give
    more accurate results.
    
    See L{find_endpoint} to avoid duplicates.
    
    @returns L{periscope.topology.models.EndPointPair}
    """
    
    sport = find_port(src)
    # if src port was not found, try to create it
    if not sport:
        snode = find_node_by_address(src)
        if not snode:
            snode = create_node_by_address(src)
        sport = find_port(src)
    
    dport = find_port(dst)
    # if dst port was not found, try to create it
    if not dport:
        dnode = find_node_by_address(dst)
        if not dnode:
            dnode = create_node_by_address(dst)
        dport = find_port(dst)
    
    if not sport:
        raise ValueError("Source port '%s' was not found, "
                    "check if src has valid IP address" % src)
    if not dport:
        raise ValueError("Destination port '%s' was not found, "
                    "check if dst has valid IP address" % dst)
    
    # creates endpoint unis identifier
    src_node_unis_id = sport.unis_id.split(':port=')[0]
    src_port_id = sport.unis_id.split(':port=')[1]
    dst_port_id = dport.unis_id.split(':port=')[1]
    unis_id = src_node_unis_id + ':endpoint=' + src_port_id + '-' + dst_port_id
    
    endpoint = EndPointPair.objects.create(unis_id=unis_id,
                    src=sport, dst=dport)
    logger.info("Endpoint: '%s' was created." % (unis_id))
    
    return endpoint


def find_endpoint(src, dst, dns_lookup=True):
    src_address_type = get_address_type(src)
    dst_address_type = get_address_type(dst)
    
    if not dns_lookup:
        src_alter_addresses = []
        dst_alter_addresses = []
    else:        
        if src_address_type == 'ipv4' or src_address_type == 'ipv6':
            src_alter_addresses = [reverse_dns(src)]
        else:
            src_alter_addresses = forward_dns(src)
        
        if dst_address_type == 'ipv4' or dst_address_type == 'ipv6':
            dst_alter_addresses = [reverse_dns(dst)]
        else:
            dst_alter_addresses = forward_dns(dst)
    
    src_address_filter = Q(addresses__value=src)
    dst_address_filter = Q(addresses__value=dst)
    
    for src_alter_address in src_alter_addresses:
        src_address_filter |= Q(addresses__value=src_alter_address)
    
    for dst_alter_address in dst_alter_addresses:
        dst_address_filter |= Q(addresses__value=dst_alter_address)
    
    
    src_ports = Port.objects.filter(src_address_filter)
    dst_ports = Port.objects.filter(dst_address_filter)
    
    if len(src_ports) == 0 or len(dst_ports) == 0:
        return None
    
    endpoints = []
    for src_port in src_ports:
        for dst_port in dst_ports:            
            try:
                endpoint = EndPointPair.objects.get(src=src_port, dst=dst_port)
                if endpoint not in endpoints:
                    endpoints.append(endpoint)
            except EndPointPair.DoesNotExist:        
                pass
    if len(endpoints) == 0:
        return None
    elif len(endpoints) == 1:
        return endpoints[0]
    else:
        raise ValueError("Multiple endpoints found: %s" % endpoints)
    

def create_psservice(service_name, access_point, service_type,
        service_description=None, event_types=[]):
    """
    Creates new UNIS Service object with
    L{periscope.topology.models.psServiceProperties} properties bag.
    If a service with the same I{access_point} exists, this method will
    return a reference to the existing object.
    
    @param service_name: the name of the service
    @type service_name: str
    @param access_point: full URL address.
    @type access_point: URL str
    @param service_description: optional description of the service
    @type service_description: str
    @param service_type: service type
    @type service_type: 'gLS', 'hLS', 'MA', 'MP'
    @param event_types: dict or list of supported event types by the service
    
    @returns: L{periscope.topology.models.Service}
    """
    
    # Check if the service already exists
    filter_q = Q(properties_bag__psserviceproperties__accessPoint=access_point)
    services = Service.objects.filter(filter_q)
    if len(services) > 0:
        return services[0]
    
    # Creating new service is needed
    parse = urlparse(access_point)
    node = find_node_by_address(parse.hostname)
    if not node:
        node = create_node_by_address(parse.hostname)
    unis_id = "%s:port=%s:service=%s" % (node.unis_id, parse.port, parse.path)
    service = Service.objects.create(unis_id=unis_id, parent=node)
    
    net_name = NetworkObjectNames.objects.create(networkobject=service,
            name=Name.objects.create(value=service_name))
    net_name.save()
    
    if service_description:
        serv_desc = NetworkObjectDescriptions.objects.create(
            networkobject=service,
            description=Description.objects.create(value=service_description))
    
    # Creates a ps service properites bag for a service
    props = psServiceProperties(serviceName=service_name,
                accessPoint=access_point,
                serviceType=service_type,
                serviceDescription=service_description)
    service.properties_bag.add(props)
    
    # Set the list of supported event types for a given psserviceproperties.
    for event_type in event_types:
        eresult = EventType.objects.get_or_create(value=event_type)
        if eresult[1] == True:
            eresult[0].save()
        
        event = eresult[0]
        psServicePropertiesEventTypes.objects.create(psServiceProperties=props,
            eventtype=event)
    
    logger.info("New service '%s' is created" % service)
    service.save()
    return service


def find_service_watch(network_obj, event_types=None):
    """
    Finds services that have data of event types about network_object
    
    @param network_obj: network object to find service watch for.
    @type network_obj: L{periscope.topology.models.NetworkObject}
    @param event_types: list of string event types or
                        L{periscope.topology.models.EventTypes}
    
    @returns: list of L{periscope.topology.models.Service}
    """
    events_parsed = []
    
    if event_types is None:
        events_parsed = []
    elif isinstance(event_types, list):
        for event in event_types:
            if isinstance(event, EventType):
                events_parsed.append(event.value)
            else:
                events_parsed.append(event)
    else:
        if isinstance(event_types, EventType):
            events_parsed.append(event_types.value)
        else:
            events_parsed.append(event_types)
    
    if len(events_parsed) > 0:
        events_query = Q(event_type__value=events_parsed[0])
        for i in range(1, len(events_parsed)):
            events_query |= Q(event_type__value=events_parsed[i])
        
        watch_list = psServiceWatchList.objects.filter(events_query,
                    network_object=network_obj)
    
    else:
        watch_list = psServiceWatchList.objects.filter(network_object=network_obj)
        
    services = []
    for watch in watch_list:
        if watch.service not in services:
            services.append(watch.service)
    if services:
        return services
    else:
        return None

