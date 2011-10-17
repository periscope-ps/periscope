
from periscope.topology.models import *
from periscope.measurements.lib import *

ports = [
    #'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth1', 
    #'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth4',
    'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth5',
    #'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth8',
    #'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth9',
    
    #'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth4',
    'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth7',
    #'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth8',
    #'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth9',
    
    #'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth4',
    'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth5',
    #'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth8',
]

nodes = [
    'urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1',
    'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1',
    'urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2',
]

service = 'http://172.31.255.210:9990/perfSONAR_PS/services/SNMPMA'

port_events = [
    'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/2.0',
    'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/received/2.0'
]

node_events = [
    'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/received/2.0',
    'http://ggf.org/ns/nmwg/tools/ganglia/network/utilization/bytes/sent/2.0',
    'http://ggf.org/ns/nmwg/tools/ganglia/cpu/utilization/system/2.0',
    'http://ggf.org/ns/nmwg/tools/ganglia/memory/main/free/2.0',
]

for urn in nodes:
    print urn
    try:
        node = Node.objects.get(unis_id=urn)
    except:
        print "Cannot find node:", urn, "\n"
    for event in node_events:
        r = register_pull_network_object(node, event, service)

for urn in ports:
    print urn
    try:
        port = Port.objects.get(unis_id=urn)
    except:
        print "Cannot find port:", urn, "\n"
    for event in port_events:
        r = register_pull_network_object(port, event, service)

