"""
Unified perfSONAR data collector
"""
import datetime
import httplib
import logging
import socket
import time
from urlparse import urlparse
from bson.dbref import DBRef
from pymongo import Connection

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from psapi.client import ServiceClient
from psapi.client import ResultSet
from psapi.query import LookupQuery
from psapi.query import SNMPQuery
from psapi.query import IPerfQuery
from psapi.query import OWAMPQuery
from psapi.query import TracerouteQuery
from psapi.query import XQuery
from psapi.query import GangliaQuery
from psapi.protocol import EndPointPair as psEndPointPair
from psapi.protocol import Interface
from psapi.protocol import IPerfSubject
from psapi.protocol import Message
from psapi.protocol import Metadata as psMetadata
from psapi.protocol import NMBService
from psapi.protocol import NetDiscardSubject
from psapi.protocol import NetErrorSubject
from psapi.protocol import NetUtilSubject
from psapi.protocol import Node as psNode
from psapi.protocol import OWAMPSubject
from psapi.protocol import PsService
from psapi.protocol import PingerSubject
from psapi.protocol import SNMPSubject
from psapi.protocol import SummarySubject
from psapi.protocol import TracerouteSubject
from psapi.protocol import events

from psapi.utils.ipaddress import get_address_type

from periscope.topology.lib.helpers import create_endpoint
from periscope.topology.lib.helpers import create_port
from periscope.topology.lib.helpers import create_psservice
from periscope.topology.lib.helpers import create_node_by_address
from periscope.topology.lib.helpers import find_node_by_address
from periscope.topology.lib.helpers import find_port
from periscope.topology.lib.helpers import reverse_dns
from periscope.topology.lib.helpers import forward_dns

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
from periscope.measurements.models import Metadata


logger = logging.getLogger('periscope')

PRINT_XML_RESULTS = False
PRINT_XML_QUERIES = False


def set_print_xml(results, queries):
    """
    Triggers the printing each query and it's result to STDOUT
    """
    global PRINT_XML_QUERIES
    PRINT_XML_QUERIES = queries

    global PRINT_XML_RESULTS
    PRINT_XML_RESULTS = results


def read_root_hints(root_hints=settings.GLS_ROOT_HINTS):
    """
    Returns list of root gLS addresses from I{root_hints}.

    @param root_hints: address of root hints
    @type root_hints: URL string
    """    
    parsed = urlparse(root_hints)
    glses = None

    logger.info("Reading root hints from: %s" % root_hints)

    if parsed.scheme == 'file':
        hints_file = open(settings.GLS_ROOT_HINTS.replace('file://', ''))
        glses = hints_file.read()
        hints_file.close()
    elif parsed.scheme == 'http':
        conn = httplib.HTTPConnection(parsed.hostname, parsed.port)
        conn.request("GET", parsed.path)
        res = conn.getresponse()
        if res.status != httplib.OK:
            raise Exception("Couldn't connect to gLSes root hints server at"
                            " '%s'" % root_hints)
        glses = res.read()
        conn.close()
    else:
        raise ValueError("Couldn't read roots hints.")

    if glses is None:
        raise ValueError("Cannot read the gLS hints, please use fully "
            "qualified URLs, for example http://example.com:80/service")

    # Converts string to array 
    return glses.split()


def add_gls(gls_url):
    """
    Adds new gLS service to the periscope services database.
    
    @param gls_url: The URL for the gLS.
    @type gls_url: URL string
    
    @return: L{periscope.topology.models.Service}
    """
    logger.info("Adding root hint: %s" % gls_url)
    gls = create_psservice(gls_url, gls_url, 'gLS',
            'Root Hint', [events.SUMMARY])
    return gls


def pull_root_hints(root_hints=settings.GLS_ROOT_HINTS, print_services=False):
    """
    Saves the list of gLS roots to the topology database.
    
    @param root_hints: address of root hints
    @type root_hints: URL string
    @param print_services: if True the service names will be printed to stdout.
    @type print_services: boolean
    
    @return: List of L{periscope.topology.models.Service}
    """
    glses = read_root_hints(root_hints)
    roots = []
    for gls in glses:
        gls = add_gls(gls)
        roots.append(gls)
        if print_services:
            access_point = gls.properties_bag.get(
                    psserviceproperties__accessPoint__contains='//'
                    ).psserviceproperties.accessPoint
            print "Added gLS: '%s'." % access_point
    return roots


def parse_lookup_service_result(results):
    """
    Parses a lookup query result to find the different perfSONAR services
    returned in the result.
    
    @param results: Lookup (gLS/hLS) service result.
    @type results: L{psapi.client.ResultSet}
    
    @returns:  list of dict in following format {
            'service': L{psapi.protocol.PsService} ,
            'data': list of L{psapi.protocol.Data}
            'get_event_types': list of string event types}
    """
    
    meta = {}
    data = {}
    return_values = []
    
    
    # TODO update psapi to read status
    if isinstance(results.meta, psMetadata) and \
        results.meta.event_types[0].find('error.') >= 0:
        raise Exception('Service %s: %s' % (results.meta.event_types,
                results.data))
    
    # Separate metadata from data
    for meta_id in results.data:
        if isinstance(results.data[meta_id], str):
            raise Exception(results.data[meta_id])
        for datum in results.data[meta_id]:      
            if isinstance(datum, psMetadata):
                meta[datum.object_id] = datum
            else:
                if datum.ref_id in data:
                    data[datum.ref_id].append(datum)
                else:
                    data[datum.ref_id] = [datum]
    
    for metaid in meta:
        event_types = []
        tmp = {'service': meta[metaid].subject.contents,
               'data': [],
               'event_types': []}
        
        if metaid in data:
            tmp['data'] = data[metaid]
            # get all event types for all data elements
            for datum in data[metaid]:
                if isinstance(datum.event_types, list):
                    event_types.extend(datum.event_types)
                elif isinstance(datum.event_types, str):
                    event_types.append(datum.event_types)
        
        tmp['event_types'] = list(set(event_types))
        return_values.append(tmp)
    
    return return_values

def save_lookup_service_result(result_set, print_services=False):
    """
    Saves the services and their assoicated data to
    L{periscope.topology.models.psServiceWatchList}.
    
    @param result_set: Lookup (gLS/hLS) service result.
    @type result_set: L{psapi.client.ResultSet}, or raw XML
    @param print_services: if True the service names will be printed to stdout.
    @type print_services: boolean
    
    @returns: None
    """
    # first parsed the results
    services = parse_lookup_service_result(result_set)
    
    # Register perfSONAR services registered with the lookup service
    for psservice in services:
        # perfSONAR services
        if isinstance(psservice['service'], PsService):
            service_name = psservice['service'].serviceName
            access_point = psservice['service'].accessPoint
            service_type = psservice['service'].serviceType
            service_description = psservice['service'].serviceDescription
        
        #Network topology service
        elif isinstance(psservice['service'], NMBService):
            service_name = psservice['service'].name
            access_point = psservice['service'].address
            service_type = psservice['service'].type
            service_description = psservice['service'].description
            
            address_type = get_address_type(access_point)
            if  address_type != 'url':
                access_point = address_type + "://" + access_point
        else:
            raise ValueError("undefined service: %s" %
                    type(psservice['service']))
        
        if isinstance(psservice['service'], PsService):
            # Create UNIS service instance
            try:
                service = create_psservice(service_name,
                        access_point,
                        service_type,
                        service_description,
                        psservice['event_types'])
            except Exception as exp:
                logger.warn(exp)
                continue
            
            if print_services:
                print "Adding: %s, %s, %s, %s" % (service_name,
                    access_point,
                    service_type,
                    service_description)
            
            
            # Register meta data assoicated with the service
            for i in range(len(psservice['data'])):
                try:
                    net_obj = register_metadata(service,
                                    psservice['data'][i].data)
                except Exception as exp:
                    logger.warn(exp)
                    continue
                if net_obj and print_services:
                    print "Registered:", net_obj

def create_service_client(service, cert=None, key=None):
    """
    Creates a perfSONAR service client from a I{service}.
    
    A service can be
        - Full qualified URL string: U{http://example.com:9999/service}
        - L{psapi.protocol.psservice.PsService}
        - L{periscope.topology.models.Service}
        - L{psapi.client.ServiceClient}: just returns the same object
    
    @param service: service to create client from.
        
    @returns: L{psapi.client.ServiceClient}
    """
    if isinstance(service, ServiceClient):
        return service
        
    if isinstance(service, str) or isinstance(service, unicode):
        url = str(service)
    elif isinstance(service, PsService):
        url = service.accessPoint
    elif isinstance(service, Service):
        properties = psServiceProperties.objects.get(parent=service)
        url = properties.accessPoint
    else:
        raise ValueError("Cannot create service client from service"
                " of type: %s" % type(service))
    
    if cert and key:
        client = ServiceClient(url, cert, key)
    else:
        client = ServiceClient(url)
    
    return client


def query_psservice(client, query, message_type=None, parse_result=True):
    """
    Sends query to perfSONAR service and returns the result.
    
    @param client: perfSONAR service client
    @type client: L{psapi.client.ServiceClient}
    @param query: Query to be sent
    @type query: L{psapi.query.Query} or XML string, or list of them.
    @param parse_result: if B{False} results will not be parsed.
    @type parse_result: boolean
    
    @returns: L{psapi.client.ResultSet} if I{parse_result}, XML string otherwise
    """
    if not isinstance(client, ServiceClient):
        raise ValueError("Client must be of type psapi.client.ServiceClient")
    
    logger.info("Sending query to: '%s'" % client.access_point)
    
    if PRINT_XML_QUERIES:
        print "Sending query to", client.access_point, ":", PRINT_XML_QUERIES
        if isinstance(query, list):
            print client.make_aggregate_query(query, message_type).to_xml()
        else:
            print query.to_xml(message_type=message_type)
    
    parse_query_result = parse_result
    if PRINT_XML_RESULTS:
        parse_query_result = False
    
    if isinstance(query, list):
        results = client.aggregate_query(query,
                    message_type=message_type, parse_result=parse_query_result)
    else:        
        results = client.query(query,
                    message_type=message_type, parse_result=parse_query_result)
    
    if PRINT_XML_RESULTS:
        print "Received result from", client.access_point, ":"
        print results
    
    if parse_result and not parse_query_result:
        results = ResultSet.parse_result(results)
    
    logger.info("Received result from: '%s'" % client.access_point)
    return results


def create_lookup_query(get_data=True, get_event_types=True):
    """
    Creates perfSONAR lookup query.
    
    @param get_data: returns I{nmwg:data} elements associated with each metadata.
    @type get_data: boolean
    @param get_event_types: returns event types for each metadata
    @type get_event_types: boolean
    
    @returns: L{psapi.query.Query}
    """

    if not get_data and get_event_types:
        # Faster query just get the metadata and event_types
        xquery_string = """
            declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
            declare namespace perfsonar="http://ggf.org/ns/nmwg/tools/org/perfsonar/1.0/";
            declare namespace psservice="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/";
            declare namespace summary="http://ggf.org/ns/nmwg/tools/org/perfsonar/service/lookup/summarization/2.0/";
            
            for $metadata in /nmwg:store[@type="LSStore"]/nmwg:metadata
                let $metadata_id := $metadata/@id 
                let $data := /nmwg:store[@type="LSStore"]/nmwg:data[@metadataIdRef=$metadata_id]
                
                return 
                    element {"nmwg:metadata"} {
                        attribute id {$metadata_id},
                        $metadata/perfsonar:subject,
                        for $event in distinct-values($data/nmwg:metadata/nmwg:eventType)
                            return
                                element {"nmwg:eventType"} {
                                    $event
                                }
                    }
        """
        return XQuery(xquery_string)

    elif not get_data and not get_event_types:
        # Faster query just get the metadata
        return LookupQuery()

    else:
        # default query (get eveything, really slow!!!!)
        xquery_string = """
          declare namespace nmwg="http://ggf.org/ns/nmwg/base/2.0/";
          /nmwg:store[@type="LSStore"]/*
        """
        return XQuery(xquery_string)


def register_metadata(service, meta):
    """
    Registers that a I{service} holds information about certain I{metadata}.
    
    @param service: services to register the metadata with
    @type service: L{periscope.topology.models.Service}
    @param meta: metadata instance to be registered
    @type meta: L{psapi.protocol.Metadata}
    
    @returns: L{periscope.topology.models.NetworkObject} instance
    """
    if isinstance(meta.subject, SNMPSubject):
        return register_snmp_meta(service, meta)
    
    elif isinstance(meta.subject, OWAMPSubject) or \
        isinstance(meta.subject, PingerSubject) or \
        isinstance(meta.subject, IPerfSubject) or \
        isinstance(meta.subject, TracerouteSubject):
        
        return register_endpoints_meta(service, meta)
    elif isinstance(meta.subject, SummarySubject):
        logger.info("SummarySubject encountered.")
        
    else:
        error = "Couldn't register metadata with subject of type '%s'" % \
                type(meta.subject)
        logger.warning(error)
        return None


def register_snmp_meta(service, meta):
    """
    Registers that a service holds information about SNMP data.
    
    see L{register_metadata}.
    """
    if not isinstance(meta, psMetadata):
        raise ValueError("meta must be of type psapi.protocol.psMetadata")

    if not isinstance(meta.subject, SNMPSubject):
        raise ValueError("subject must be of type psapi.protocol.SNMPSubject")

    subject = meta.subject
    event_types = meta.event_types
    port = interface_to_port(subject.contents)

    if isinstance(event_types, list):
        events_parsed = event_types
    else:
        events_parsed = [event_types]

    # Adding custome events to figure out which 'in' and which is 'out'
    if isinstance(subject, NetUtilSubject):
        sent = events.NET_UTILIZATION_SENT
        recv = events.NET_UTILIZATION_RECV
    if isinstance(subject, NetErrorSubject):
        sent = events.NET_ERROR_SENT
        recv = events.NET_ERROR_RECV
    if isinstance(subject, NetDiscardSubject):
        sent = events.NET_DISCARD_SENT
        recv = events.NET_DISCARD_RECV
    
    if subject.direction.lower() == 'in':
        events_parsed.append(recv)
    elif subject.direction.lower() == 'out':
        events_parsed.append(sent)
    else:
        events_parsed.append(sent)
        events_parsed.append(recv)
    
    # Register the service
    register_service_watch_list(service, port, events_parsed)

    return port


def register_endpoints_meta(service, meta):
    """
    Registers that a service holds information about EndPointPair data.
    for example IPerf, OWAMP, Pinger

    see L{register_metadata}.
    """
    if not isinstance(meta, psMetadata):
        raise ValueError("meta must be of type psapi.protocol.Metadata")

    if not isinstance(meta.subject.contents, psEndPointPair):
        raise ValueError("metadata subject must be of type "
            "psapi.protocol.EndPointPair, not %s" % type(meta.subject.contents))

    src = meta.subject.src
    dst = meta.subject.dst

    endpoints = create_endpoint(src, dst)
    register_service_watch_list(service, endpoints, meta.event_types)

    return endpoints


def interface_to_port(interface, create_new=True):
    """
    Creates a UNIS port from L{psapi.protocol.Interface} object.

    if the a Port already exists for the Interface, it just going to
    return the port instance without creating new Port object.

    see L{port_to_interface}.

    @param interface: L{psapi.protocol.Interface} object   

    @returns: L{topology.models.Port}
    """
    if not isinstance(interface, Interface):
        raise ValueError("interface must be of type psapi.protocol.Interface, "
                        "not %s" % type(interface))

    ipaddress = interface.ipAddress
    ifaddress = interface.ifAddress
    hostname =  interface.hostName
    ifname =  interface.ifName
    # TODO read URN from interface (need updating psapi)

    if hostname is None:
        hostname = interface.ifHostName

    port = find_port(ipaddress, hostname, ifaddress, ifname)

    if not port and create_new:
        try:
            node = Node.objects.get(names__value=hostname)
        except MultipleObjectsReturned:
            raise ValueError("Hostname is not unique")
        except ObjectDoesNotExist:
            node = find_node_by_address(hostname)
            if not node:
                node = create_node_by_address(hostname)

        port = create_port(node, ifaddress=ifaddress, ifname=ifname)

    return port


def port_to_interface(port):
    """
    Makes L{psapi.protocol.Interface} out of L{periscope.topology.models.Port}

    see L{interface_to_port}
    """

    if not isinstance(port, Port):
        raise ValueError("port must be of type periscope.topology.models.Port")

    ifnames = port.names.filter(type='ifName')
    ifaddresses = port.addresses.filter(type='ifAddress')
    ipaddresses = port.addresses.filter(Q(type='ipv4') | Q(type='ipv4'))
    hostnames = port.parent.names.all()

    if ifnames:
        ifname = ifnames[0].value
    else:
        ifname = None

    if ifaddresses:
        ifaddress = ifaddresses[0].value
    else:
        ifaddress = None

    if ipaddresses:
        ipaddress = ipaddresses[0].value
    else:
        ipaddress = None

    if hostnames:
        hostname = hostnames[0].value
    else:
        hostname = None

    interface = Interface(ifName=ifname, ifAddress=ifaddress,
                        ipAddress=ipaddress, hostName=hostname)

    return interface


def register_service_watch_list(service, networkobject, event_types):
    """
    Registers a 'service' has information of 'event_types' about
    'networkobject'

   
    @param service: periscope.topology.models.Service instance
    @param networkobject: periscope.topology.models.NetworkObject instance
    @param event_types: list of str, or periscope.topology.models.EventType

    @returns: None
    """
    if not isinstance(service, Service):
        raise ValueError("service must of type "
                    "periscope.topology.models.Service")

    if not isinstance(networkobject, NetworkObject):
        raise ValueError("networkobject must of type "
                    "periscope.topology.models.NetworkObject")

    if not event_types:
        raise ValueError("event_types cannot be empty or None.")

    if not isinstance(event_types, list):
        event_types = [event_types]

    for event in event_types:
        if isinstance(event, EventType):
            event_type = event
        else:
            # AH: slows down the performance because it creates a transaction
            event_type_result = EventType.objects.get_or_create(value=event)
            event_type = event_type_result[0]
            if event_type_result[1]:
                event_type.save()

        # AH: slows down the performance because it creates a transaction
        watch = psServiceWatchList.objects.get_or_create(service=service,
                event_type=event_type,
                network_object=networkobject)
        if watch[1] == 1:
            watch[0].watchedObject = networkobject
            watch[0].save()


def make_query_by_key(key, event_type, start_time=None, end_time=None):
    """
    Makes query for a metadata key with event_type.

    @param key: string metadata key
    @param event_type: event from L{psapi.protocol.events}
    @param start_time:
    @param end_time:

    @returns: L{psapi.query.Query}.
    """
    discard_events = [events.NET_DISCARD,
            events.NET_DISCARD_SENT,
            events.NET_DISCARD_RECV]
    error_events = [events.NET_ERROR_SENT,
            events.NET_ERROR_RECV,
            events.NET_ERROR]
    utilization_events = [events.NET_UTILIZATION_SENT,
            events.NET_UTILIZATION_RECV,
            events.NET_UTILIZATION]
    snmp_events = discard_events + error_events + utilization_events
    
    iperf_events = [events.IPERF2]
    owamp_events = [events.OWAMP]
    traceroute_events = [events.TRACEROUTE]
    
    all_events = snmp_events + iperf_events + owamp_events + traceroute_events

    if not (isinstance(key, str) or isinstance(key, unicode)):
        raise ValueError("key must be str.")

    if event_type.find('ganglia') > 0:
        query = GangliaQuery(maKey=key, event=event_type,
                start_time=start_time, end_time=end_time)
    elif event_type in discard_events:
        query = SNMPQuery(maKey=key, event=events.NET_DISCARD,
                start_time=start_time, end_time=end_time)
    elif event_type in error_events:
        query = SNMPQuery(maKey=key, event=events.NET_ERROR,
                start_time=start_time, end_time=end_time)
    elif event_type in utilization_events:
        query = SNMPQuery(maKey=key, event=events.NET_UTILIZATION,
                start_time=start_time, end_time=end_time)
    elif event_type in iperf_events:
        query = IPerfQuery(maKey=key, start_time=start_time, end_time=end_time)
    elif event_type in owamp_events:
        query = OWAMPQuery(maKey=key, start_time=start_time, end_time=end_time)
    elif event_type in traceroute_events:
        query = TracerouteQuery(maKey=key, start_time=start_time,
                end_time=end_time)

    return query
    

def make_snmp_query(port, event_types):
    """
    Makes query for a port with event_types.

    @param port: L{periscope.topology.models.Port} or
                 L{psapi.protocol.Interface}.
    @param event_types: list of events from L{psapi.protocol.events}.

    @returns: list of {psapi.query.Query}.
    """
    snmp_sent_events = [events.NET_DISCARD_SENT,
            events.NET_ERROR_SENT,
            events.NET_UTILIZATION_SENT]
    snmp_recv_events = [events.NET_DISCARD_RECV,
            events.NET_ERROR_RECV,
            events.NET_UTILIZATION_RECV]

    if not isinstance(port, Port) and not isinstance(port, Interface):
        raise ValueError("Each element of ports must be of type "
                "periscope.topology.models.Port or "
                "psapi.protocol.Interface.")

    if not isinstance(event_types, list):
        event_types = [event_types]

    if isinstance(port, Interface):
        interface = port
    else:
        interface = port_to_interface(port)

    queries = []
    for event_type in event_types:
        if not (event_type in snmp_sent_events or \
                event_type in snmp_recv_events):
            raise ValueError("Unrecognized event type "+ event_type)

        if event_type in snmp_sent_events:
            interface.direction = 'out'
        elif event_type in snmp_recv_events:
            interface.direction = 'in'

        if event_type in [events.NET_DISCARD_SENT, events.NET_DISCARD_RECV]:
            query = SNMPQuery(interface=interface, event=events.NET_DISCARD)
        elif event_type in [events.NET_ERROR_SENT, events.NET_ERROR_RECV]:
            query = SNMPQuery(interface=interface, event=events.NET_ERROR)
        elif event_type in [events.NET_UTILIZATION_SENT, events.NET_UTILIZATION_RECV]:
            query = SNMPQuery(interface=interface, event=events.NET_UTILIZATION)
        queries.append(query)
    
    return queries


def make_endpoint_query(endpoint, event_types):
    """
    Makes query for an endpoint with event_type.

    @param endpoint: L{periscope.topology.models.EndPointPair} or 
                     L{psapi.protocol.EndPointPair}
    @param event_types: list of events from L{psapi.protocol.events}

    @returns: list of L{psapi.query.Query}.
    """
    if not isinstance(endpoint, EndPointPair) and not isinstance(endpoint, psEndPointPair):
        raise ValueError("Each element of endpoints must be of type "
        "periscope.topology.models.EndPointPair or "
        "psapi.protocol.EndPointPair.")
    
    if not isinstance(event_types, list):
        event_types = [event_types]
    
    endpoint_queries = []
    if isinstance(endpoint, psEndPointPair):
        subjects = [endpoint]
    else:
        subjects = []    
        src_addresses = endpoint.src.toRealType().addresses.all()
        dst_addresses = endpoint.dst.toRealType().addresses.all()
        for src_address in src_addresses:
            for dst_address in dst_addresses:
                src = src_address.value
                dst = dst_address.value
                endpoints = psEndPointPair(src=src, dst=dst)
                # it's safer to set this to None
                endpoints.src_type = None
                endpoints.dst_type = None
                subjects.append(endpoints)

    for event_type in event_types:
        for subject in subjects:
            query = None
            if event_type == events.IPERF2:
                query = IPerfQuery(endpointpair=subject)
            elif event_type == events.OWAMP:
                query = OWAMPQuery(endpointpair=subject)
            elif event_type == events.TRACEROUTE:
                query = TracerouteQuery(endpointpair=subject)
            else:
                logger.warn("Cannot make query of event type " + event_type)
            if query:
                endpoint_queries.append(query)

    return endpoint_queries

def node_to_psnode(node):
    return psNode(hostName=node.names.all()[0])

def make_ganglia_query(network_object, event_type, start_time=None, end_time=None):
    if isinstance(network_object, Port):
        subject = port_to_interface(network_object)
    elif isinstance(network_object, Interface) or isinstance(network_object, psNode):
        subject = network_object
    elif isinstance(network_object, Node):
        subject = node_to_psnode(network_object)
    
    return GangliaQuery(event=event_type, subject=subject, start_time=start_time, end_time=end_time, consolidation_function='AVERAGE', resolution=30)
    
    
def get_meta_keys(service, network_objects, event_type):
    """
    Querys service for the metadata keys of all network objects with event_type.
    
    
    @param service: L{periscope.topology.models.Service}
    @param network_objects: list of L{periscope.topology.models.NetworkObjects}
                            or L{psapi.protocol.Interface}
                            or L{psapi.protocol.EndPointPair}
    @param event_type: one of the events in L{psapi.protocol.events}
    
    @returns: dictionary indexed by network_objects and the value is {'key', 'meta'}
    """
    if isinstance(network_objects, list):
        objects = network_objects
    else:
        objects = [network_objects]
        
    
    queries = []
    objects_index = {}
    result_keys = {}
    
    # the object index is used to find the related metakey from the results
    # because some services doesn't relate the metadataIdRef with the 
    # original metadata ID.
    for obj in objects:
        if event_type.find('ganglia') > 0:
            query = [make_ganglia_query(obj, event_type)]
            if isinstance(obj, Port):
                interface = port_to_interface(obj)
                index = (interface.hostName,
                        interface.ifName,
                        interface.ipAddress,
                        interface.ifAddress)
                objects_index[index] = obj
            elif isinstance(obj, Node):
                psnode = node_to_psnode(obj)
                index = (psnode.hostName)
                objects_index[index] = obj
        elif isinstance(obj, Port):
            query = make_snmp_query(obj, event_type)
            interface = port_to_interface(obj)
            index = (interface.hostName,
                    interface.ifName,
                    interface.ipAddress,
                    interface.ifAddress)
            objects_index[index] = obj
        elif isinstance(obj, Interface):
            query = make_snmp_query(obj, event_type)
            index = (obj.hostName, obj.ifName, obj.ipAddress, obj.ifAddress)
            objects_index[index] = obj
        elif isinstance(obj, EndPointPair):
            query = make_endpoint_query(obj, event_type)
            src_addresses = obj.src.toRealType().addresses.all()
            dst_addresses = obj.dst.toRealType().addresses.all()
            for src_address in src_addresses:
                for dst_address in dst_addresses:
                    src = src_address.value
                    dst = dst_address.value
                    objects_index[(src, dst)] = obj
        elif isinstance(obj, psEndPointPair):
            query = make_endpoint_query(obj, event_type)
            objects_index[(obj.src, obj.dst)] = obj
        else:
            raise ValueError("Unkown Network object of type: %s" % type(obj))
        queries.extend(query)
    
    
    client = create_service_client(service)
    result = query_psservice(client, queries, Message.METADATA_KEY_REQUEST)

    if not isinstance(result.meta, dict):
        meta_result = {result.meta.object_id: result.meta}
        data_result = {result.meta.object_id: result.data}
    else:
        meta_result = result.meta
        data_result = result.data

    for meta_id in meta_result:
        meta = meta_result[meta_id]
        data = data_result[meta_id]

        event_types = ";".join(meta.event_types)
        if event_types.find('error.') >= 0:
            continue

        if isinstance(meta.subject.contents, psEndPointPair):
            ends = (meta.subject.src, meta.subject.dst)
            obj = objects_index[ends]
            result_keys[obj] = {'key': data, 'meta': meta_result[meta_id]}
        elif isinstance(obj, Node):
            index = obj.names.all()[0]
            obj = objects_index[index]
            result_keys[obj] = data
            result_keys[obj] = {'key': data, 'meta': meta_result[meta_id]}
        elif isinstance(meta.subject.contents, Interface):
            interface = meta.subject.contents
            index = (interface.hostName,
                    interface.ifName,
                    interface.ipAddress,
                    interface.ifAddress)
            obj = objects_index[index]
            result_keys[obj] = data
            result_keys[obj] = {'key': data, 'meta': meta_result[meta_id]}
    
    return result_keys


def get_mongodb():
    """
    Returns a mongodb connection for measurements.
    """
    connection = Connection(host=settings.MEASUREMENTS_DATABASE['HOST'],
            port=settings.MEASUREMENTS_DATABASE['PORT'],
            **settings.MEASUREMENTS_DATABASE['OPTIONS'])
    
    mongodb = connection[settings.MEASUREMENTS_DATABASE['NAME']]
    
    mongodb.metadata.ensure_index([('unis_id', 1), ('event_type', 1)],
                                    unique=True)
    #mongodb.metadata.ensure_index([('meta_key', 1)], unique=True)
    
    return mongodb


def save_metadata(service, unis_id, meta_key,
                event_type, parameters, pull=True, **kargs):
    """
    Saves the metadata to mongodb.
    """
    mongodb = get_mongodb()
    keys = {'unis_id': unis_id, 'event_type': event_type}
    meta_document = {'service': service,
                    'meta_key': meta_key,
                    'pull': pull,
                    'parameters': parameters}
    if kargs:
        meta_document.update(kargs)
    
    metadata = mongodb.metadata.find_and_modify(keys,
                        {'$set': meta_document}, upsert=True, new=True)
    return metadata


def get_all_meta_keys(query_filter=None):
    """
    Pulls all metakeys for all subjects with pulling enabled and key is null.
    
    Also saves the metadata to the measurements database.
    
    @param  query_filter: Query applied to filter subset of 
            mongodb measurements collection
    @type  query_filter: dict
    
    @returns: None
    """
    mongodb = get_mongodb()
    if not query_filter:
        query_filter = {}
    
    query_filter['pull'] = True
    query_filter['meta_key'] = None
    
    # Group metadata by service and event type
    #metadata_group = mongodb.metadata.group(['service', 'event_type'],
    #        query_filter,
    #        {'list': []}, 'function(obj, prev) {prev.list.push(obj)}')
    
    metadata_group = list(mongodb.metadata.find())

    for group in metadata_group:
        service = group['service']
        event_type = group['event_type']
        network_objects = []
        
        # Get UNIS network objects
        #for meta in group['list']:
        #    obj = NetworkObject.objects.get(
        #                        unis_id=meta['unis_id']).toRealType()
        #    network_objects.append(obj)
        
        obj = NetworkObject.objects.get(                                                                                                                          
            unis_id=group['unis_id']).toRealType()                                                                                                 
        network_objects.append(obj)        

        results = get_meta_keys(service, network_objects, event_type)
        
        for obj in results:
            key = results[obj]['key']
            parameters = results[obj]['meta'].parameters.parameters
            
            save_metadata(service, obj.unis_id, key,
                          event_type, parameters, True)


def get_measurements_data(service, meta_keys, event_type, \
        start_time=None, end_time=None):
    """
    Queries the perfSONAR service for all meta keys for data of event_type

    
    @param service: L{periscope.topology.models.Service}
    @param meta_keys: list of metadata keys strings
    @param event_type: one of the events in L{psapi.protocol.events}

    @returns: dict of meta_keys associated with the returend data
    """
    if not isinstance(meta_keys, list):
        meta_keys = [meta_keys]

    queries = []
    meta_index = {}
    return_dict = {}
    
    # Get metadata indexes
    for key in meta_keys:
        query = make_query_by_key(key, event_type, start_time, end_time)
        queries.append(query)
        return_dict[key] = None
        
        # Need to keep this list because for errors metakey
        # might not be returned
        meta_objs = query.get_psobjects()['meta']
        if isinstance(meta_objs, psMetadata):
            meta_index[meta_objs.object_id] = key
        else:
            meta_index[meta_objs[-1].object_id] = key

    client = create_service_client(service)
    result = query_psservice(client, queries, Message.SETUP_DATA_REQUEST)

    for meta_id in result.meta:
        try:
            key = result.meta[meta_id].maKey.parameters.maKey
            return_dict[key] = result.data[meta_id]
        except:
            ref_id = result.meta[meta_id].ref_id
            if ref_id in meta_index and meta_id in  result.data:
                key = meta_index[ref_id]
                return_dict[key] = result.data[meta_id]
    
    return return_dict

def to_datetime(time_type, time_value):
    """
    Converts unix and iso time to python's datetime object.
    """
    return_date = None
    if time_type == 'unix':
        return_date = datetime.datetime.fromtimestamp(int(time_value))
    elif time_type == 'iso':
        # Doing it in two steps because python doesn't have
        # microseconds formatter
        time_array = time_value.split('.')
        time_no_micro = time_array[0] + " " + " ".join(time_array[1].split()[1:])
        micro = int(time_array[1].split()[0])
        return_date = datetime.datetime.strptime(time_no_micro,
                                                "%a %b %d %H:%M:%S %Z %Y")
        return_date = return_date + datetime.timedelta(microseconds=micro)
    return return_date

def save_measurements_data(meta_ref, data):
    """
    Saves the measurements
    """
    mongodb = get_mongodb()
    
    for datum in data:
        fdatum = datum
        fdatum['meta_ref'] = meta_ref
        if 'value' in datum:
            if datum['value'] =='nan':
                continue
        if 'timeType' in datum:
            time_type = fdatum.pop('timeType')
            if 'timeValue' in datum:
                time_value = fdatum.pop('timeValue')
                fdatum['time'] = to_datetime(time_type, time_value)
                
            if 'startTime' in datum:
                time_value = fdatum.pop('startTime')
                fdatum['start_time'] = to_datetime(time_type, time_value)
                
            if 'endTime' in datum:
                time_value = fdatum.pop('endTime')
                fdatum['end_time'] = to_datetime(time_type, time_value)
        
        if 'valueUnits' in datum:
            units = fdatum.pop('valueUnits')
            fdatum['units'] = units
        
        # trys to convert strings to numerical values
        for item in datum:
            try:
                datum[item] = float(datum[item]) if '.' in datum[item] else int(datum[item])
            except:
                pass
        
        mongodb.measurements.insert(fdatum)


def pull_all_data(query_filter=None, start_time=None, end_time=None):
    """
    Pulls data for all metadata in Metadata table.
    
    @param  query_filter:  Query applied to filter subset of 
            L{periscope.measurements.models.Metadata}
    @type  query_filter: L{django.db.models.query_utils.Q}
    
    @returns: None
    """
    mongodb = get_mongodb()
    if not query_filter:
        query_filter = {}
    
    query_filter['pull'] = True
    query_filter['meta_key'] =  {'$not': {'$type': 10}}
    
    # Group metadata by service and event type
    #metadata_group = mongodb.metadata.group(['service', 'event_type'],
    #        query_filter,
    #        {'list': []}, 'function(obj, prev) {prev.list.push(obj)}')
    
    metadata_group = list(mongodb.metadata.find())

    for group in metadata_group:
        service = group['service']
        event_type = group['event_type']
        
        meta_keys = []
        meta_index = {}
        
        #for meta in group['list']:
        #    meta_keys.append(meta['meta_key'])
        #    meta_index[meta['meta_key']] = DBRef('metadata', meta['_id'])
        
        meta_keys.append(group['meta_key'])                                                                                                    
        meta_index[group['meta_key']] = DBRef('metadata', group['_id'])                  

        if not start_time:
            last_measurement = mongodb.measurements.find(
                        {'meta_ref':
                            {'$in': meta_index.values()}}
                        ).sort([('time', -1)]).limit(1)
            
            if last_measurement.count() > 0:
                last_measurement = last_measurement.next()
                start_time = int(time.mktime(
                                last_measurement['time'].timetuple()))
            else:
                start_time = int(time.time()) - 1000
        
        if not end_time:
            end_time = int(time.time())
        
        results = get_measurements_data(service, meta_keys,
                        event_type, start_time, end_time)
        
        for key, value in results.items():
            if isinstance(value, list):
                save_measurements_data(meta_index[key], value)
            elif not value:
                pass
            else:
                logger.warn("Couldn't save data for maKey: %s, event:%s, value: %s" % (key, event_type, value))


def register_pull_network_object(network_object, event_type, service):
    """
    Registers a network object for data pulling.
    """
    meta = save_metadata(service, network_object.unis_id, None, event_type,
            None, pull=True)
    return meta

def unregister_pull_network_object(network_object, event_type):
    """
    Registers a network object to pulled by perfSONAR pulling script
    """
    mongodb = get_mongodb()
    mongodb.metadata.update({'unis_id': network_object.unis_id,
                        'event_type': event_type},
                    {'$set': {'pull': False}})

def get_metadata_by_key(meta_key):
    """
    Gets mongodb metadata dict by meta_key
    """
    mongodb = get_mongodb()
    meta = mongodb.metadata.find_one({'meta_key': meta_key})
    return meta



def query_measurements(unis_ids, event_types, meta_filter=None, data_filter=None):
    """
    Queries mongodb for measurements data by unis_id, and event_types
    """
    
    if not meta_filter:
        meta_filter = {}
    if not data_filter:
        data_filter = {}
    
    if not isinstance(meta_filter, dict):
        raise ValueError("meta_filter should be dict.")
    
    if not isinstance(data_filter, dict):
        raise ValueError("data_filter should be dict.")
    
    if not isinstance(event_types, list):
        event_types = [event_types]
    if not isinstance(unis_ids, list):
        unis_ids = [unis_ids]
    
    mongodb = get_mongodb()
    results = {'meta': {}, 'data': {}}
    
    meta_filter['unis_id'] = {'$in': unis_ids}
    meta_filter['event_type']= {'$in': event_types}
    
    metas = mongodb.metadata.find(meta_filter)
    results['meta'] = dict([(str(v['_id']), v) for v in metas])
    meta_refs = [DBRef('metadata', v.pop('_id')) for v in results['meta'].values()]
    results['data'] = dict([(meta_id, []) for meta_id in results['meta'].keys()])
    
    data_filter['meta_ref'] = {'$in': meta_refs}
    data = mongodb.measurements.find(data_filter, {'_id': 0})
    del meta_refs
    
    for datum in data:
        meta_ref = str(datum.pop('meta_ref').id)
        results['data'][meta_ref].append(datum)
    
    return results


def reset_meta_keys():
	db = get_mongodb()
	db.metadata.update({}, {'$set' : {'meta_key': None}}, upsert=False, multi=True)

