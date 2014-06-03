"""
AH: This parser need to be improved for error checking. If wrong input is given
this parser will horribly fail!

TODO: all steps should be in transaction so if any thing fails nothing is
committed to the database
"""
import xml.dom.minidom as dom

from periscope.topology.models import Domain, Node, Port, Link, Topology, \
    BASE_NAMESPACE
from periscope.topology.lib.util import get_urn_value


TOPOLOGY_NS = "http://ogf.org/schema/network/topology/ctrlPlane/20080828/"


def process_link(link, port):
    """
    AH: Switching Capability Descriptors is NOT handled yet
    """
    linkID = get_urn_value(link.getAttribute('id'), 'link')
    capacity = link.getElementsByTagNameNS(TOPOLOGY_NS, "capacity")
    maximumReservableCapacity = link.getElementsByTagNameNS(TOPOLOGY_NS, "maximumReservableCapacity")
    minimumReservableCapacity = link.getElementsByTagNameNS(TOPOLOGY_NS, "minimumReservableCapacity")
    granularity = link.getElementsByTagNameNS(TOPOLOGY_NS, "granularity")
    trafficEngineeringMetric = link.getElementsByTagNameNS(TOPOLOGY_NS, "trafficEngineeringMetric")

    remoteLink = link.getElementsByTagNameNS(TOPOLOGY_NS, "remoteLinkId")
    
    l = Link(port=port, link=linkID, capacity=capacity[0].firstChild.data,
        maximumReservableCapacity=maximumReservableCapacity[0].firstChild.data,
        minimumReservableCapacity=minimumReservableCapacity[0].firstChild.data,
        granularity=granularity[0].firstChild.data,
        trafficEngineeringMetric=trafficEngineeringMetric[0].firstChild.data,
        remoteLink=remoteLink[0].firstChild.data,
    )
    l.save()
    

def process_port(port, node):
    portID = get_urn_value(port.getAttribute('id'), 'port')
    capacity = port.getElementsByTagNameNS(TOPOLOGY_NS, "capacity")
    maximumReservableCapacity = port.getElementsByTagNameNS(TOPOLOGY_NS, "maximumReservableCapacity")
    minimumReservableCapacity = port.getElementsByTagNameNS(TOPOLOGY_NS, "minimumReservableCapacity")
    granularity = port.getElementsByTagNameNS(TOPOLOGY_NS, "granularity")
    links = port.getElementsByTagNameNS(TOPOLOGY_NS, "link")
    
    p = Port(node=node, port=portID, capacity=capacity[0].firstChild.data,
        maximumReservableCapacity=maximumReservableCapacity[0].firstChild.data,
        minimumReservableCapacity=minimumReservableCapacity[0].firstChild.data,
        granularity=granularity[0].firstChild.data,
    )
    p.save()
    
    for l in links:
        process_link(l, p)

def process_node(node, domain):
    nodeID = get_urn_value(node.getAttribute('id'), 'node')
    address = node.getElementsByTagNameNS(TOPOLOGY_NS, "address")
    ports = node.getElementsByTagNameNS(TOPOLOGY_NS, "port")
    
    n = Node(domain=domain, node=nodeID, address=address[0].firstChild.data)
    n.save()
    
    for p in ports:
        process_port(p, n)

def process_domain(domain):
    domainID = get_urn_value(domain.getAttribute('id'), 'domain')
    node = domain.getElementsByTagNameNS(TOPOLOGY_NS, "node")
    
    d = Domain(domain=domainID)
    d.save()
    
    for n in node:
        process_node(n, d)

def process_topology(top):
    domain = top.getElementsByTagNameNS(TOPOLOGY_NS, "domain")
    for d in domain:
        process_domain(d)

def parse_dom_doc(doc):
    xml_topologies = doc.getElementsByTagNameNS(BASE_NAMESPACE, "topology")
    parsed_topologies = []
    for t in xml_topologies:
        parsed_topologies.append(Topology.parse_xml(t, None))
    return parsed_topologies

def create_from_xml_file(xml_file):
    return parse_dom_doc(dom.parse(xml_file))

def create_from_xml_string(xml_string):
    return parse_dom_doc(dom.parseString(xml_string))
    
def import_from_xml_string(xml_string):
    doc = dom.parseString(xml_string)
    topo = doc.getElementsByTagName("topology")
    
    
