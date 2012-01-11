from periscope.topology.models import *
from periscope.measurements.lib import *

ports = [
    "urn:ogf:network:domain=escps.udel.edu:node=udel01:port=eth3",
    "urn:ogf:network:domain=escps.udel.edu:node=udel02:port=eth3",
    "urn:ogf:network:domain=escps.ultralight.org:node=tera04:port=eth4",
    "urn:ogf:network:domain=escps.ultralight.org:node=tera05:port=eth4",
]

nodes = [
    "urn:ogf:network:domain=escps.udel.edu:node=udel01",
    "urn:ogf:network:domain=escps.udel.edu:node=udel02",
    "urn:ogf:network:domain=escps.ultralight.org:node=tera04",
    "urn:ogf:network:domain=escps.ultralight.org:node=tera05",
]

service = 'http://localhost:9990/perfSONAR_PS/services/SNMPMA'

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

