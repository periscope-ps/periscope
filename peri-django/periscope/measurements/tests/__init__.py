"""
Data collector unit testing
"""

import os

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.test import TestCase

from psapi.client import ResultSet
from psapi.client import ServiceClient
from psapi.query import Query
from psapi.query import LookupQuery
from psapi.query import XQuery
from psapi.protocol import PsService
from psapi.protocol import Interface
from psapi.protocol import Metadata
from psapi.protocol import NetDiscardSubject
from psapi.protocol import NetErrorSubject
from psapi.protocol import NetUtilSubject
from psapi.protocol import events

from periscope.measurements.models import DNSCache


from periscope.measurements.lib import add_gls
from periscope.measurements.lib import create_lookup_query
from periscope.measurements.lib import create_service_client


from periscope.measurements.lib import create_psservice

from periscope.measurements.lib import find_port
from periscope.measurements.lib import reverse_dns
from periscope.measurements.lib import forward_dns
from periscope.measurements.lib import interface_to_port
from periscope.measurements.lib import parse_lookup_service_result
from periscope.measurements.lib import pull_root_hints
from periscope.measurements.lib import read_root_hints
from periscope.measurements.lib import register_endpoints_meta
from periscope.measurements.lib import register_metadata
from periscope.measurements.lib import register_service_watch_list
from periscope.measurements.lib import register_snmp_meta


from periscope.topology.models import Address
from periscope.topology.models import EventType
from periscope.topology.models import Name
from periscope.topology.models import NetworkObjectNames
from periscope.topology.models import Node
from periscope.topology.models import Port
from periscope.topology.models import psServiceWatchList
from periscope.topology.models import Service


class MeasurementsLibTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.EXAMPLE_HOST = 'example.com'
        cls.EXAMPLE_IP = ['192.0.43.10', '2001:500:88:200::10']
        cls.EXAMPLE_REVERSE = '43-10.any.icann.org'
        
        cls.PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
        cls.TEST_HOSTNAME = 'testcreateportNode'
        cls.NODE_ID = 'urn:ogf:network:domain=example.com:node=%s' % cls.TEST_HOSTNAME
        cls.PORT_IP = '127.0.0.1'
        cls.TEST_NODE = Node.objects.create(unis_id=cls.NODE_ID)
        
        name = Name.objects.create(value=cls.TEST_HOSTNAME)
        name.save()
        network_name = NetworkObjectNames.objects.create(name=name,
                        networkobject=cls.TEST_NODE)
        network_name.save()
        
        cls.TEST_PORTS_DATA = [
            {
                'node': cls.TEST_NODE, 
                'address': cls.PORT_IP,
                'address_type': 'ipv4',
                'ifaddress': None,
                'ifname': None,
                'unis_id': None,
             },
             {
                'node': cls.TEST_NODE, 
                'address': None,
                'address_type': None,
                'ifaddress': None,
                'ifname': 'testIFname2',
                'unis_id': None,
             },
             {
                'node': cls.TEST_NODE, 
                'address': None,
                'address_type': None,
                'ifaddress': 'testifaddress3',
                'ifname': 'testIFname3',
                'unis_id': None,
             },
             {
                'node': cls.TEST_NODE,
                'address': None,
                'address_type': None,
                'ifaddress': 'testifaddress4',
                'ifname': 'testIFname4',
                'unis_id': cls.NODE_ID + ':port=testport4',
             },
        ]

    
    
    def test_get_gls_list(self):    
        gls_list = read_root_hints()
        self.assertIsInstance(gls_list, list)
    
    def test_add_gls(self):
        gls_url = 'http://example.com:9999/service/gLS'
        service = add_gls(gls_url)
        self.assertIsInstance(service, Service)
        url = service.properties_bag.all()[0].psserviceproperties.accessPoint
        self.assertEqual(url, gls_url)
    
    def tes_pull_root_hints(self):
        roots = pull_root_hints()
        self.assertEqual(type(roots), list)
    
    def test_create_lookup_query(self):
        query = create_lookup_query()
        self.assertIsInstance(query, Query)
        
        query = create_lookup_query(get_data=True)
        self.assertIsInstance(query, Query)
        
        query = create_lookup_query(get_event_types=True)
        self.assertIsInstance(query, Query)
        
        query = create_lookup_query(get_data=True, get_event_types=True)
        self.assertIsInstance(query, Query)
    
    
    def test_create_service_client(self):
        CLIENT_URL = 'http://wwww.example.com:9999/service'
        TEST_DATA = [
            CLIENT_URL,
            PsService(accessPoint=CLIENT_URL),
            ServiceClient(CLIENT_URL),
        ]
        
        for test in TEST_DATA:
            client = create_service_client(test)
            self.assertIsInstance(client, ServiceClient)
            self.assertEqual(client.access_point, CLIENT_URL)
    
    
        
        
    def test_parse_lookup_service_result(self):
        results = open(self.PATH + 'hls_snmp.xml').read()
        results_set = ResultSet.parse_result(results)
        services = parse_lookup_service_result(results_set)
        
        self.assertEqual(len(services), 2)
        self.assertEqual(len(services[0]['data']), 8)
        self.assertEqual(len(services[1]['data']), 5)
        
        event_types = [ events.NET_ERROR,
            events.NET_DISCARD,
            events.NET_UTILIZATION
        ]
        
        for service in services:
            for data in service['data']:
                self.assertIsNotNone(data)
            for event in event_types:
                self.assertTrue(event in service['event_types'])
                
    def test_save_lookup_service_result(self):
        pass # TODO(AH) test save_lookup_service_result
    
    def test_interface_to_port(self):
        # TODO test with create port is False
        results = open(self.PATH + 'hls_snmp.xml').read()
        results_set = ResultSet.parse_result(results)
        services = parse_lookup_service_result(results_set)
        
        for psservice in services:
            for data in psservice['data']:
                port = interface_to_port(data.subject.contents)
                self.assertIsInstance(port, Port)
                
    def test_port_to_interface(self):
        pass # TODO test port_to_interface
                
                
    def test_register_service_watch_list(self):
        service = Service.objects.create(
                unis_id=self.NODE_ID +':service=testservice')
        
        neterr_event = EventType.objects.create(value=events.NET_ERROR)
        
        TEST_DATA = [
            [ neterr_event, events.NET_DISCARD, events.NET_UTILIZATION ],
            [ neterr_event ],
            neterr_event ,
            events.NET_DISCARD
        ]
        
        for event_types in TEST_DATA:
            register_service_watch_list(service, self.TEST_NODE, event_types)
            
            if isinstance(event_types, list):
                events_list = event_types
            else:
                events_list = [event_types]
            
            for event in events_list:
                if isinstance(event, EventType):
                    e = event.value
                else:
                    e = event
                
                watch_list = psServiceWatchList.objects.filter(
                            service=service,
                            network_object=self.TEST_NODE,
                            event_type__value=e)
                
                self.assertEqual(watch_list.count(), 1)
                
    def test_register_metadata(self):
        # TODO more testing is needed
        results = open(self.PATH + 'hls_snmp.xml').read()
        results_set = ResultSet.parse_result(results)
        services = parse_lookup_service_result(results_set)
        
        self.assertEqual(len(services), 2)
        self.assertEqual(len(services[0]['data']), 8)
        self.assertEqual(len(services[1]['data']), 5)
        
        for psservice in services:
            serviceType = psservice['service'].serviceType
            serviceName = psservice['service'].serviceName
            accessPoint = psservice['service'].accessPoint
            serviceDescription = psservice['service'].serviceDescription
            
            service = create_psservice(serviceName,
                    accessPoint,
                    serviceType,
                    serviceDescription,
                    psservice['event_types'])
            
            for data in psservice['data']:
                obj = register_metadata(service, data.data)
                # check if all data elements were registered
                watch = psServiceWatchList.objects.filter(service=service, network_object=obj)
                self.assertTrue(watch.count() > 0)
    
    
    def test_register_snmp_meta(self):
        # Create SNMP Metadata objects
        util_params = {'supportedEventType': [events.NET_UTILIZATION, events.SNMP]}
        err_params = {'supportedEventType': [events.NET_ERROR, events.SNMP]}
        disc_params = {'supportedEventType': [events.NET_DISCARD, events.SNMP]}
        
        # Create interfaces
        interfaces = []
        for i in range(4):
            interface = Interface(hostName='testhostname',
                ifName='testinterface%d' % i,
                capacity=1000000,
                direction='in')
            interfaces.append(interface)
        
        interfaces[1].direction = 'out'
        
        # Different SNMP subject types
        netutil_subject1 = NetUtilSubject(interface=interfaces[0])
        netutil_subject2 = NetUtilSubject(interface=interfaces[1])
        neterr_subject = NetErrorSubject(interface=interfaces[2])
        netdisc_subject = NetDiscardSubject(interface=interfaces[3])
        
        util_meta1 = Metadata(subject=netutil_subject1,
                        event_types=[events.NET_UTILIZATION, events.SNMP],
                        parameters=util_params)
        
        util_meta2 = Metadata(subject=netutil_subject2,
                        event_types=[events.NET_UTILIZATION, events.SNMP],
                        parameters=util_params)
        
        err_meta = Metadata(subject=neterr_subject,
                        event_types=[events.NET_ERROR, events.SNMP],
                        parameters=err_params)
        
        disc_meta = Metadata(subject=netdisc_subject,
                        event_types=[events.NET_DISCARD, events.SNMP],
                        parameters=disc_params)
        
        serviceType = 'MA'
        serviceName = 'testservice'
        accessPoint = 'http://example.com:9999/services/snmp'
        serviceDescription = 'test description'
                
        service = create_psservice(serviceName,
                accessPoint,
                serviceType,
                serviceDescription,
                [events.SNMP, events.NET_UTILIZATION, events.NET_ERROR, events.NET_DISCARD])
        
        # register the meta data
        util_port1 = register_snmp_meta(service, util_meta1)
        util_port2 = register_snmp_meta(service, util_meta2)
        err_port = register_snmp_meta(service, err_meta)
        disc_port = register_snmp_meta(service, disc_meta)
        
        # Assert all ports belong to the same Node
        self.assertEqual(util_port1.parent, util_port2.parent)
        self.assertEqual(util_port1.parent, err_port.parent)
        self.assertEqual(util_port1.parent, disc_port.parent)
        
        
        # Assert correct SNMP event types have been added
        self.assertIsNotNone(psServiceWatchList.objects.get(
                    service=service,
                    network_object=util_port1,
                    event_type__value=events.NET_UTILIZATION_RECV
        ))
        
        self.assertIsNotNone(psServiceWatchList.objects.get(
                    service=service,
                    network_object=util_port2,
                    event_type__value=events.NET_UTILIZATION_SENT
        ))
    
    def test_register_endpoints_meta(self):
        pass # TODO (AH): unit testing for register_endpoints_meta
