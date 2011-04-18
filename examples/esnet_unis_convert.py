#!/bin/usr/python

"""Imports the current version of ESNet topology and produce new UNIS xml file.

This script does DNS and reverse DNS lookups to make sure it catches all addresses.
"""

import logging
import socket
from lxml import etree

# TODO(AH): Read file names from command line
# Input file name
ESNET_TOPOLOGY = 'esnet_topology.xml'
# output file name
ESNET_UNIS = 'esnet_topology_unis.xml'

# Enable/Disable Reverse DNS lookups for speed
REVERSE_DNS = True

# if set to true this script will import the control plan topology as well
IMPORT_CTRLPLAN = False

# Defined Namespaces
NMTOPO = 'http://ogf.org/schema/network/topology/base/20070828/'
NMTB = 'http://ogf.org/schema/network/topology/base/20070828/'
UNIS = 'http://ogf.org/schema/network/topology/unis/20100528/'
NMTL2 = 'http://ogf.org/schema/network/topology/l2/20070828/'
NMTL3 = 'http://ogf.org/schema/network/topology/l3/20070828/'
CTRL ="http://ogf.org/schema/network/topology/ctrlPlane/20080828/"
NSMAP = {'unis': UNIS, 'nmtl3': NMTL3, 'ctrlplane': CTRL}

# setup the logger
logger = logging.getLogger('periscope')


def get_host_by_addr(ip):
    """Reverse DNS lookup for addresses without hostnames
    
    If the global variable REVERSE_DNS is set to False, this function
    always returns None
    """
    if REVERSE_DNS == False:
		return None
		
    try:
        host = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        host = None
    logger.info("Reverse DNS lookup for %s returned '%s'" % (ip, host))
    return host



def create_topology(node, nparent=None):
    """Reads NMTB topology node and produce UNIS topology
    """
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'topology'), nsmap=NSMAP)
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'topology'))
    
    # TODO: must come with a better solution for none define IDes
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Topology's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating topology with id '%s'" % child.get('id'))
   
    # Iterate and convert all children
    for c in node.getchildren():
        create_element(c, child)
    
    return child


def create_domain(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'domain'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'domain'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Domain's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating domain with id '%s'" % child.get('id'))
    
    for c in node.getchildren():
        create_element(c, child)
    
    return child


def create_node(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'node'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'node'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Node's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating node with id '%s'" % child.get('id'))
        
    
    get_text_children(node, child, "{%s}%s" % (NMTB, 'name'), "{%s}%s" % (UNIS, 'name'))
    get_text_children(node, child, "{%s}%s" % (NMTB, 'description'), "{%s}%s" % (UNIS, 'description'))
    for n in node.findall("{%s}%s" % (NMTB, 'hostName')):
        address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
        hostname = n.text
        address.text = hostname
        address.set('type', 'hostname')
    
    if node.find("{%s}%s" % (NMTB, 'latitude')) is not None:
        location = etree.SubElement(child, "{%s}%s" % (UNIS, 'location'))
        get_text_children(node, location, "{%s}%s" % (NMTB, 'latitude'), "{%s}%s" % (UNIS, 'latitude'))
        get_text_children(node, location, "{%s}%s" % (NMTB, 'longitude'), "{%s}%s" % (UNIS, 'longitude'))
        
        
    for c in node.getchildren():
        create_element(c, child)
    
    return child


def create_l2port(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'port'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'port'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("L2Port's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creatingl2 port with id '%s'" % child.get('id'))
    
    get_text_children(node, child, "{%s}%s" % (NMTL2, 'ifName'), "{%s}%s" % (UNIS, 'name'))
    get_text_children(node, child, "{%s}%s" % (NMTL2, 'ifDescription'), "{%s}%s" % (UNIS, 'description'))
    get_text_children(node, child, "{%s}%s" % (NMTL2, 'capacity'), "{%s}%s" % (UNIS, 'capacity'))
    
    for c in node.getchildren():
        create_element(c, child)
    
    return child
    

def create_l3port(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'port'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'port'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("L3Port's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating l3 port with id '%s'" % child.get('id'))
    
    
    get_text_children(node, child, "{%s}%s" % (NMTL3, 'capacity'), "{%s}%s" % (UNIS, 'capacity'))
        
    for n in node.findall("{%s}%s" % (NMTL3, 'ipAddress')):
        address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
        address.text = n.text
        address.set('type', n.get('type').lower())
        # reterive the full dns name if any!
        if n.get('type').lower() == 'ipv4' or n.get('type').lower() == 'ipv6':
            host = get_host_by_addr(n.text)
            if host is not None:
                address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
                address.text = host
                address.set('type', 'hostname')
            
    
    for n in node.findall("{%s}%s" % (NMTB, 'relation')):
        idref = n.find("{%s}%s" % (NMTB, 'idRef')).text
        if not idref.split(':').pop().startswith('port='):
            print "Error a relation to None port in L3 port, (%s)" % idref
            continue
        relation = etree.SubElement(child, "{%s}%s" % (UNIS, 'relation'))
        relation.set('type', n.get('type'))
        portid = etree.SubElement(relation, "{%s}%s" % (UNIS, 'portIdRef'))
        portid.text = idref
        
    netmask = node.findall("{%s}%s" % (NMTL3, 'netmask'))
    
    if netmask is not None:
        bag = etree.SubElement(child, "{%s}%s" % (UNIS, 'portPropertiesBag'))
        portprops = etree.SubElement(bag, "{%s}%s" % (NMTL3, 'portProperties'))
        for n in netmask:
            net = etree.SubElement(portprops, "{%s}%s" % (NMTL3, 'netmask'))
            net.text = n.text
            
        
    for c in node.getchildren():
        create_element(c, child)
    
    # Sometimes L2 port is directly defined as ifName or as a relation of
    # type 'over'. To make things uniform all L2 interfaces are defined
    # by a relation of type 'over'
    ifName = node.findall("{%s}%s" % (NMTL3, 'ifName'))
    
    for ifn in ifName:
        if child.xpath("*//unis:relation[unis:portIdRef=\"%s\"]" % ifn.text, namespaces={'unis' : UNIS}) is None:
            relation = etree.SubElement(child, "{%s}%s" % (UNIS, 'relation'))
            relation.set('type', 'over')
            portid = etree.SubElement(relation, "{%s}%s" % (UNIS, 'portIdRef'))
            portid.text = ifn.text
            
                    
    return child

def create_l2link(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'link'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'link'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("L2Link's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating l2 link with id '%s'" % child.get('id'))
    
    child.set('directed', 'false')
    if 'type' in node.attrib:
        if node.attrib['type'] == 'unidirectional':
            child.set('directed', 'true')
        else:
            child.set('directed', 'false')
    
    # TODO add another name to the bag because of type
    get_text_children(node, child, "{%s}%s" % (NMTL2, 'name'), "{%s}%s" % (UNIS, 'name'))
    
    for n in node.findall("{%s}%s" % (NMTB, 'relation')):
        idref = n.find("{%s}%s" % (NMTB, 'idRef')).text
        if not idref.split(':').pop().startswith('link='):
            logger.error("Error a relation to non link in L2 port, (%s)" % idref)
            continue
        
        if node.getparent().tag == "{%s}%s" % (NMTL2, 'port'):
            relation = etree.SubElement(child, "{%s}%s" % (UNIS, 'relation'))
            relation.set('type', 'source')
            portid = etree.SubElement(relation, "{%s}%s" % (UNIS, 'portIdRef'))
            portid.text = node.getparent().get('id')
            
            root = node.getroottree()
            sink = root.find("//{%s}%s[@id='%s']" % (NMTL2, 'link', idref)).getparent()
            relation = etree.SubElement(child, "{%s}%s" % (UNIS, 'relation'))
            relation.set('type', 'sink')
            portid = etree.SubElement(relation, "{%s}%s" % (UNIS, 'portIdRef'))
            portid.text = sink.get('id')
        else:
            logger.error("Link parent is not a port but it is %s" % node.getparent().tag)
            
        relation = etree.SubElement(child, "{%s}%s" % (UNIS, 'relation'))
        t = n.get('type')
        if t == 'sibling':
            relation.set('type', 'pair')
        else:
            relation.set('type', t)
            
        linkid = etree.SubElement(relation, "{%s}%s" % (UNIS, 'linkIdRef'))
        linkid.text = idref
        
    for c in node.getchildren():
        create_element(c, child)
    
    return child
    


def get_text_children(oldnode, newnode, oldname, newname):
    for n in oldnode.findall(oldname):
        if n.text is not None:
            child = etree.SubElement(newnode, newname)
            child.text = n.text
            for attr in n.attrib:
                child.set(attr, n.attrib[attr])


def create_ctrl_domain(node, nparent):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'domain'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'domain'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Control Plane Domain's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating control plane domain with id '%s'" % child.get('id'))
    
    for c in node.getchildren():
        create_element(c, child)
    
    return child
    

def create_ctrl_node(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'node'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'node'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Control Plane Node's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating control plane node with id '%s'" % child.get('id'))
        
    for n in node.findall("{%s}%s" % (CTRL, 'address')):
        address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
        address.text = n.text
        address.set('type', 'ipv4')
        
        host = get_host_by_addr(n.text)
        if host is not None:
            address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
            address.text = host
            address.set('type', 'hostname')
                
    for c in node.getchildren():
        create_element(c, child)
    
    return child

def create_ctrl_port(node, nparent=None):
    if nparent == None:
        child = etree.Element("{%s}%s"% (UNIS, 'port'))
    else:
        child = etree.SubElement(nparent, "{%s}%s" % (UNIS, 'port'))
    
    if node.get('id') is None:
        child.set('id', 'NOTDEFINED')
        logger.warning("Control Plane Port's %s id is not define using 'NOTDEFINED'" % node)
    else:
        child.set('id', node.get('id'))
        
    logger.info("Creating control plane port with id '%s'" % child.get('id'))
    
    
    get_text_children(node, child, "{%s}%s" % (CTRL, 'capacity'), "{%s}%s" % (UNIS, 'capacity'))
    
    for n in node.findall("{%s}%s" % (CTRL, 'address')):
        address = etree.SubElement(child, "{%s}%s" % (UNIS, 'address'))
        address.text = n.text
        address.set('type', 'ipv4')
        # TODO Remove this line
        logger.info("A control plane port with address %s" % n.text)
        
    capacity = node.find("{%s}%s" % (CTRL, 'capacity'))
    max = node.find("{%s}%s" % (CTRL, 'maximumReservableCapacity'))
    min = node.find("{%s}%s" % (CTRL, 'minimumReservableCapacity'))
    granularity = node.find("{%s}%s" % (CTRL, 'granularity'))
    
    if capacity is not None or max is not None or min is not None or granularity is not None:
        bag = etree.SubElement(child, "{%s}%s" % (UNIS, 'portPropertiesBag'))
        portprops = etree.SubElement(bag, "{%s}%s" % (CTRL, 'portProperties'))
            
        if capacity is not None:
            c = etree.SubElement(portprops, "{%s}%s" % (CTRL, 'capacity'))
            c.text = capacity.text
            
        if max is not None:
            t = etree.SubElement(portprops, "{%s}%s" % (CTRL, 'maximumReservableCapacity'))
            t.text = max.text
            
        if min is not None:
            t = etree.SubElement(portprops, "{%s}%s" % (CTRL, 'minimumReservableCapacity'))
            t.text = min.text
            
        if granularity is not None:
            t = etree.SubElement(portprops, "{%s}%s" % (CTRL, 'granularity'))
            t.text = granularity.text
            
    for c in node.getchildren():
        create_element(c, child)
    
    return child


def create_ctrl_link (node, nparent=None):
    # TODO
    pass
    

def create_element(node, nparent):
    """ Creates new UNIS element from node and add as child to the new parent 'nparent'
    from the new tree.
    """
    
    if node.tag == "{%s}%s" % (NMTB, 'topology'):
        create_topology(node, nparent)
    elif node.tag == "{%s}%s" % (NMTB, 'domain'):
        create_domain(node, nparent)
    elif node.tag == ("{%s}%s" % (NMTB, 'node')):
        create_node(node, nparent)
    elif node.tag == "{%s}%s" % (NMTL2, 'port'):
        create_l2port(node, nparent)
    elif node.tag == "{%s}%s" % (NMTL3, 'port'):
        create_l3port(node, nparent)
    elif node.tag == "{%s}%s" % (NMTL2, 'link'):
        create_l2link(node, nparent)
    elif IMPORT_CTRLPLAN == True and node.tag == "{%s}%s" % (CTRL, 'domain'):
        create_ctrl_domain(node, nparent)
    elif IMPORT_CTRLPLAN == True and node.tag == ("{%s}%s" % (CTRL, 'node')):
        create_ctrl_node(node, nparent)
    elif IMPORT_CTRLPLAN == True and node.tag == ("{%s}%s" % (CTRL, 'port')):
        create_ctrl_port(node, nparent)
    else:
        pass


if __name__ == '__main__':
    hdlr = logging.FileHandler('/tmp/periscope.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    esnet_file = open(ESNET_TOPOLOGY)
    otree = etree.parse(esnet_file)
    ntree =  create_topology(otree.getroot())
    f = open(ESNET_UNIS, 'w')
    f.write(etree.tostring(ntree, pretty_print=True))
    f.close()
