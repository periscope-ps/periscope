from django.test import TestCase

from psapi.protocol import events

from periscope.topology.models import EventType
from periscope.topology.models import psServiceWatchList

from periscope.topology.lib.helpers import create_endpoint
from periscope.topology.lib.helpers import create_port
from periscope.topology.lib.helpers import create_psservice
from periscope.topology.lib.helpers import create_node_by_address
from periscope.topology.lib.helpers import reverse_dns
from periscope.topology.lib.helpers import forward_dns
from periscope.topology.lib.helpers import find_endpoint
from periscope.topology.lib.helpers import find_node_by_address
from periscope.topology.lib.helpers import find_port
from periscope.topology.lib.helpers import find_service_watch

from periscope.measurements.models import DNSCache

class TopologyLibTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.EXAMPLE_HOST = 'example.com'
        cls.EXAMPLE_IP = ['192.0.43.10', '2001:500:88:200::10']
        cls.EXAMPLE_REVERSE = '43-10.any.icann.org'
    
    def test_reverse_dns(self):
        example_host = reverse_dns(self.EXAMPLE_IP[0], cache=False)
        self.assertEqual(example_host, self.EXAMPLE_REVERSE)
        
        for ip in self.EXAMPLE_IP:
            self.assertRaises(DNSCache.DoesNotExist,
                    DNSCache.objects.get,
                    ip=ip)
        
        example_host = reverse_dns(self.EXAMPLE_IP[0], cache=True)
        self.assertEqual(example_host, self.EXAMPLE_REVERSE)
        
        dns_cache = DNSCache.objects.get(ip=self.EXAMPLE_IP[0])
        self.assertEqual(dns_cache.hostname, self.EXAMPLE_REVERSE)
    
    def test_forward_dns(self):
        result = forward_dns(self.EXAMPLE_HOST, cache=False)
        self.assertEqual(result, self.EXAMPLE_IP)
        
        self.assertRaises(DNSCache.DoesNotExist,
                DNSCache.objects.get,
                hostname=self.EXAMPLE_HOST)
        
        example_ip_cached = forward_dns(self.EXAMPLE_HOST, cache=True)
        self.assertEqual(example_ip_cached, self.EXAMPLE_IP)
        
        dns_cache = DNSCache.objects.filter(hostname=self.EXAMPLE_HOST)
        self.assertEqual(dns_cache.count(), 2)
        
        test1 = DNSCache.objects.create(hostname='testhost.com', ip='1.1.1.1')
        test2 = DNSCache.objects.create(hostname='testhost.com', ip='2.2.2.2')
        test_ip_cached = forward_dns('testhost.com', cache=True)
        self.assertEqual(test_ip_cached, [test1.ip, test2.ip])
    
    def test_create_node_by_address(self):
        node = create_node_by_address(self.EXAMPLE_HOST, False)
        # no port should be created because there is no ip addresses
        self.assertEquals(node.get_ports().count(), 0)
        
        self.assertEquals(node.names.filter(
                        value=self.EXAMPLE_HOST).count(), 1)
        self.assertEquals(node.addresses.filter(
                        value=self.EXAMPLE_HOST).count(), 1)
        node.addresses.all().delete()
        node.names.all().delete()
        node.delete()
        
        node = create_node_by_address(self.EXAMPLE_HOST, True)
        self.assertEquals(node.get_ports().count(), 2)
        self.assertEquals(node.names.filter(
                        value=self.EXAMPLE_HOST).count(), 1)
        node.addresses.all().delete()
        node.names.all().delete()
        node.delete()
        
        node = create_node_by_address(self.EXAMPLE_IP[0], False)
        self.assertEquals(node.get_ports().count(), 1)
        self.assertEquals(node.names.all().count(), 0)
        self.assertEquals(node.addresses.all().count(), 0)
        node.delete()
        
        node = create_node_by_address(self.EXAMPLE_IP[0], True)
        self.assertEquals(node.get_ports().count(), 1)
        self.assertEquals(node.names.all().count(), 1)
        self.assertEquals(node.addresses.all().count(), 1)

    def test_find_node_by_address(self):
        node1 = create_node_by_address(self.EXAMPLE_IP[0], False)
        find_node1 = find_node_by_address(self.EXAMPLE_IP[0])
        self.assertEqual(node1, find_node1)
        node1.delete()
        
        node2 = create_node_by_address(self.EXAMPLE_IP[0], True)
        find_node2 = find_node_by_address(self.EXAMPLE_IP[0])
        self.assertEqual(node2, find_node2)
        
        find_node2 = find_node_by_address(self.EXAMPLE_REVERSE)
        self.assertEqual(node2, find_node2)
        node2.delete()
        
        node3 = create_node_by_address(self.EXAMPLE_HOST, False)
        find_node3 = find_node_by_address(self.EXAMPLE_HOST)
        self.assertEqual(node3, find_node3)
        node3.delete()
        
        node4 = create_node_by_address(self.EXAMPLE_HOST, True)
        find_node4 = find_node_by_address(self.EXAMPLE_HOST)
        self.assertEqual(node4, find_node4)
        
        find_node4 = find_node_by_address(self.EXAMPLE_IP[0])
        self.assertEqual(node4, find_node4)
        
        find_node4 = find_node_by_address(self.EXAMPLE_IP[1])
        self.assertEqual(node4, find_node4)
        node4.delete()

    def test_create_port(self):
        hostname = 'testhostname'
        ifname = 'testname'
        ifaddress = 'testinterface'
        node = create_node_by_address(hostname)
        
        port1 = create_port(node, self.EXAMPLE_IP[0])
        addresses1 = port1.addresses.filter(value=self.EXAMPLE_IP[0])
        self.assertEqual(addresses1.count(), 1)
        self.assertEqual(port1.parent, node)
        
        port2 = create_port(node, ifaddress=ifaddress)
        addresses2 = port2.addresses.filter(value=ifaddress)
        self.assertEqual(addresses2.count(), 1)
        self.assertEqual(port2.parent, node)
        
        port3 = create_port(node, self.EXAMPLE_IP[1], ifname=ifname)
        addresses3 = port3.addresses.filter(value=self.EXAMPLE_IP[1])
        self.assertEqual(addresses3.count(), 1)
        names3 = port3.names.filter(value=ifname)
        self.assertEqual(names3.count(), 1)
        self.assertEqual(port3.parent, node)
    
    def test_find_port(self):
        hostname = 'testhostname'
        ifname = 'testname'
        ifaddress = 'testinterface'
        node = create_node_by_address(hostname)
        
        port1 = create_port(node, self.EXAMPLE_IP[0])
        port1_find = find_port(self.EXAMPLE_IP[0])
        self.assertEqual(port1, port1_find)
        
        port2 = create_port(node, ifaddress='testinterface')
        port2_find = find_port(hostname=hostname, ifaddress=ifaddress)
        self.assertEqual(port2, port2_find)
        
        port3 = create_port(node, self.EXAMPLE_IP[1], ifname=ifname)
        port3_find = find_port(self.EXAMPLE_IP[1])
        self.assertEqual(port3, port3_find)
        
        port3_find = find_port(hostname=hostname, ifname=ifname)
        self.assertEqual(port3, port3_find)
        
        self.assertIsNone(find_port(address='www.exmaple.com'))
        self.assertIsNone(find_port(hostname='tmp', ifaddress='address'))
        self.assertIsNone(find_port(hostname='tmp', ifname='name'))
        
        self.assertRaises(ValueError, find_port, None)
        self.assertRaises(ValueError, find_port, ifaddress='address')
        self.assertRaises(ValueError, find_port, ifname='address')
    
    def test_create_endpoint(self):
        end1 = create_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[0])
        src1 = end1.src
        dst1 = end1.dst
        self.assertEqual(src1, dst1)
        end1.delete()
        
        end2 = create_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[1])
        self.assertEqual(src1, end2.src)
        self.assertNotEqual(dst1, end2.dst)
        end2.delete()
    
    
    def test_find_endpoint(self):
        self.assertIsNone(find_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[0]))
        
        end1 = create_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[0])
        end1_find = find_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[0])
        self.assertEqual(end1, end1_find)
        
        self.assertIsNone(find_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[1]))
        end2 = create_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[1])
        end2_find = find_endpoint(self.EXAMPLE_IP[0], self.EXAMPLE_IP[1])
        self.assertEqual(end2, end2_find)
        
        self.assertIsNone(find_endpoint(self.EXAMPLE_IP[1], self.EXAMPLE_IP[0]))
        
    def test_create_psservice(self):
        service_name = 'test service'
        service_type = 'test'
        service_description = 'this is a test service'
        event_types = [events.SUMMARY, events.ECHO ]
        service_accesspoint = "http://%s:9995/test" % self.EXAMPLE_IP[0]
        
        service = create_psservice(service_name, service_accesspoint,
                    service_type, service_description, event_types)
        
        node = find_node_by_address(self.EXAMPLE_IP[0])
        self.assertEqual(service.parent, node)
        
        self.assertEqual(service.names.get(value=service_name).value,
                        service_name)
        
        props = service.properties_bag.all()[0].psserviceproperties
        self.assertEqual(props.serviceName, service_name)
        self.assertEqual(props.accessPoint, service_accesspoint)
        self.assertEqual(props.serviceType, service_type)
        self.assertEqual(props.serviceDescription, service_description)
        
        for event in event_types:
            self.assertEqual(props.eventTypes.filter(value=event).count(), 1)
    
        service.delete()
        service2 = create_psservice(service_name, service_accesspoint,
                    service_type, service_description, event_types)
        
        # should be the same node
        self.assertEqual(service2.parent, node)
        
        
    def test_find_service_watch(self):
        service_name = 'test service'
        service_type = 'test'
        service_description = 'this is a test service'
        service_accesspoint = "http://%s:9995/test" % self.EXAMPLE_IP[0]
        event = EventType.objects.create(value=events.NET_UTILIZATION)
        
        service = create_psservice(service_name, service_accesspoint,
                    service_type, service_description)
        
        node = find_node_by_address(self.EXAMPLE_IP[0])
        
        self.assertIsNone(find_service_watch(node, events.NET_UTILIZATION))
        
        watch = psServiceWatchList.objects.create(service=service,
                    event_type=event,  network_object=node)
                    
        services_find = find_service_watch(node, events.NET_UTILIZATION)
        self.assertEqual(len(services_find), 1)
        self.assertEqual(services_find[0], service)
