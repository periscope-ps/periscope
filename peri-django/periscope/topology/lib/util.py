import re

from periscope.topology.error import UnknownXMLNamespaceException,\
    UNISXMLParsingException

import xml.dom.minidom as dom
from django.db.models.manager import Manager
from django.db.models.fields import related

def find_path(src, dst):
    from periscope.topology.models import Path
    
    src_name = re.findall(r'node=(.*)', src.unis_id)
    dst_name = re.findall(r'node=(.*)', dst.unis_id)

    path_id = src_name[0] + '2' + dst_name[0]
    
    try:
        path = Path.objects.get(unis_id=path_id)
    except Path.DoesNotExist:
        return None

    return path

def make_periscope_shape_json(shape, x, y, w, h, fill, tx, ty, align):
    return '"shape":"%s","x":%s,"y":%s,"width":%s,"height":%s,"fill":"%s"'\
        ',"textXDisp":%s,"textYDisp":%s,"textAlign":"%s"' % \
        (shape, x, y, w, h, fill, tx, ty, align)


def get_shape_json_esnet(topology, excludeNodeNames=[]):
    """ Needs to be written in such way that only draws the nodes we care about.
    """
    import os
    from periscope.topology.models import PeriscopeDomainProperties,\
        PeriscopeNodeProperties, PeriscopePortProperties, Path, Hop, Node,\
        PeriscopeSavedTopology
    from cStringIO import StringIO

    # XXX: The template engine could do this, but I'm guessing here is faster
    json_topology = StringIO()

    # hack to get a saved topology
    saved_topo = PeriscopeSavedTopology.objects.all()
    if (len(saved_topo)):
        json_topology.write(saved_topo[0].topo)
        return json_topology

    json_topology.write("[")
    
    # TODO: include properties?
    domains = topology.get_domains()
    for domain in domains:
        shape_json = ''
        try:
            shape = PeriscopeDomainProperties.objects.get(parent=domain).shape
            shape_json = ',\n' + shape.toJson()
        except PeriscopeDomainProperties.DoesNotExist:
            shape_json = ',\n' + make_periscope_shape_json("rect", 0, 0, 50, 50, "moccasin", 0, 0, "middle");
        json_topology.write('{\n"id":%s,\n"type":"%s",\n"unisId":"%s",\n"name":"%s"%s\n},\n\n' % \
                                (domain.id, 'domain', domain.unis_id, 
                                 get_urn_value(domain.unis_id, 'domain'), shape_json))
    
    esnodes = domain.get_nodes()
    nodes = []
    ports = []
    links = []
    paths = Path.objects.all()
    for path in paths:
        hops = Hop.objects.filter(parent=path)
        for hop in hops:
            link = hop.target.toRealType()
            if link not in links:
                links.append(link.toRealType())
                
                sport = link.get_source().toRealType()
                dport = link.get_sink().toRealType()
                snode = sport.parent.toRealType()
                dnode = dport.parent.toRealType()
            
                if snode.type=='cloud' or snode in esnodes:                
                    if snode not in nodes:
                        nodes.append(snode)
                    if sport not in ports:
                        ports.append(sport)
            
                if dnode.type=='cloud' or dnode in esnodes:                
                    if dnode not in nodes:
                        nodes.append(dnode)
                    if dport not in ports:
                        ports.append(dport)
    

    for node in nodes:
        shape_json = ''
        try:
            shape = PeriscopeNodeProperties.objects.get(parent=node).shape
            shape_json = ',\n' + shape.toJson()
        except PeriscopeNodeProperties.DoesNotExist:
            shape_json = ',\n' + make_periscope_shape_json("circle", 0, 0, 30, 30, "lightcyan", 0, 0, "middle");
        json_topology.write('{\n"id":%s,\n"type":"%s",\n"parent":{"_reference":%s},\n'
                            '"unisId":"%s",\n"name":"%s"%s\n},\n\n' % \
                                (node.id, 'node', domain.id, node.unis_id, 
                                 get_urn_value(node.unis_id, 'node'), shape_json))
    
    for port in ports:
        unis_id = get_urn_value(port.unis_id, 'port')
        if unis_id == None:
            unis_id = port.unis_id
        port_display = 'Port ' + unis_id
        shape_json =  ',\n' + make_periscope_shape_json("circle", 0, 0, 5, 5, "aliceblue", -10, -10, "middle");
        for properties in port.properties_bag.all():
            properties = properties.toRealType()
            
            if isinstance(properties, PeriscopePortProperties):
                shape_json = ',\n' + properties.shape.toJson()
                continue
            
            prop_html = properties.toHTML()
            if prop_html:
                port_display += '<br><br>' + prop_html

        json_topology.write('{\n"id":%s,\n"type":"%s",\n"parent":{"_reference":%s},\n'
                            '"unisId":"%s",\n"name":"%s",\n"display":"%s"%s\n},\n\n' % \
                                (port.id, 'port', Node.objects.get(unis_id=port.parent).id, port.unis_id, 
                                 get_urn_value(port.unis_id, 'port'), port_display, shape_json))
    
    
                                             
   
    
    for link in links:
        json_topology.write('{\n"id":%s,\n"type":"%s",\n"unisId":"%s",\n"source":'
                           '{"_reference":%s},\n"sink":{"_reference":%s},\n"name":"%s"\n},\n\n' % \
                                (link.id, 'link', link.unis_id, link.get_end_points()[0].id,
                                link.get_end_points()[1].id, get_urn_value(link.unis_id, 'link')))
                                     
    json_topology.seek(-3, os.SEEK_END)
    json_topology.write(' ]')

    topo = PeriscopeSavedTopology(topo=json_topology.getvalue())
    topo.save()
    
    # TODO: json_topology.getvalue().replace("\n", '') for compression

    return json_topology


def get_shape_json(topology):
    import os
    from periscope.topology.models import PeriscopeDomainProperties,\
        PeriscopeNodeProperties, PeriscopePortProperties
    from cStringIO import StringIO

    # XXX: The template engine could do this, but I'm guessing here is faster
    json_topology = StringIO()
    json_topology.write("[")
    
    # TODO: include properties?
    domains = topology.get_domains()
    for domain in domains:
        shape_json = ''
        try:
            shape = PeriscopeDomainProperties.objects.get(parent=domain).shape
            shape_json = ',\n' + shape.toJson()
        except PeriscopeDomainProperties.DoesNotExist:
            shape_json = ',\n' + make_periscope_shape_json("rect", 0, 0, 50, 50, "moccasin", 0, 0, "middle");
        json_topology.write('{\n"id":%s,\n"type":"%s",\n"unisId":"%s",\n"name":"%s"%s\n},\n\n' % \
                                (domain.id, 'domain', domain.unis_id, 
                                 get_urn_value(domain.unis_id, 'domain'), shape_json))

    nodes = []
    for domain in domains:
        for node in domain.get_nodes():
            shape_json = ''
            try:
                shape = PeriscopeNodeProperties.objects.get(parent=node).shape
                shape_json = ',\n' + shape.toJson()
            except PeriscopeNodeProperties.DoesNotExist:
                shape_json = ',\n' + make_periscope_shape_json("circle", 0, 0, 30, 30, "lightcyan", 0, 0, "middle");
            json_topology.write('{\n"id":%s,\n"type":"%s",\n"parent":{"_reference":%s},\n'
                                '"unisId":"%s",\n"name":"%s"%s\n},\n\n' % \
                                    (node.id, 'node', domain.id, node.unis_id, 
                                     get_urn_value(node.unis_id, 'node'), shape_json))
            nodes.append(node)
    
    ports = []
    for node in nodes:
        for port in node.get_ports():
            port_display = 'Port ' + get_urn_value(port.unis_id, 'port')
            shape_json =  ',\n' + make_periscope_shape_json("circle", 0, 0, 5, 5, "aliceblue", -10, -10, "middle");
            for properties in port.properties_bag.all():
                properties = properties.toRealType()
                
                if isinstance(properties, PeriscopePortProperties):
                    shape_json = ',\n' + properties.shape.toJson()
                    continue
                
                prop_html = properties.toHTML()
                if prop_html:
                    port_display += '<br><br>' + prop_html

            json_topology.write('{\n"id":%s,\n"type":"%s",\n"parent":{"_reference":%s},\n'
                                '"unisId":"%s",\n"name":"%s",\n"display":"%s",\n"capacity":"%s"'
                                '%s\n},\n\n' % \
                                    (port.id, 'port', node.id, port.unis_id, 
                                     get_urn_value(port.unis_id, 'port'), port_display,
                                     port.capacity, shape_json))
            ports.append(port)
    
    for domain in domains:
        for link in domain.get_links():
            json_topology.write('{\n"id":%s,\n"type":"%s",\n"unisId":"%s",\n"source":'
                                '{"_reference":%s},\n"sink":{"_reference":%s},\n"name":"%s"\n},\n\n' % \
                                    (link.id, 'link', link.unis_id, link.get_end_points()[0].id,
                                     link.get_end_points()[1].id, get_urn_value(link.unis_id, 'link')))
                        
    # TODO: There could be links inside the domain or topology
    for port in ports:
        for link in port.get_links():
            json_topology.write('{\n"id":%s,\n"type":"%s",\n"unisId":"%s",\n"source":'
                                '{"_reference":%s},\n"sink":{"_reference":%s},\n"name":"%s"\n},\n\n' % \
                                    (link.id, 'link', link.unis_id, link.get_end_points()[0].id, 
                                     link.get_end_points()[1].id, get_urn_value(link.unis_id, 'link')))

    json_topology.seek(-3, os.SEEK_END)
    json_topology.write(' ]')
    
    # TODO: json_topology.getvalue().replace("\n", '') for compression

    return json_topology

def get_urn_value(urn, key):
    """
    Return a value of specific key from URN
    
    Example:
    'urn:ogf:network:domain=udel.edu:node=stout'
    value for domain is udel
    value for node is stout
    """
    pairs = urn.split(':')
    for p in pairs:
        if p.startswith(key + '='):
            return p.split('=')[1]
    return None

def create_urn(domain, node=None, port=None, link=None):
    """
    Create topology URN.
    
    Example if domain is udel.edu then the URN is
    'urn:ogf:network:domain=udel.edu'
    And if domain is udel.edu and node is stout then the URN is
    'urn:ogf:network:domain=udel.edu:node=stout'
    """
    if node == None:
        return "urn:ogf:network:domain=%s"%domain
    if node != None and port == None and link == None:
        return "urn:ogf:network:domain=%s:node=%s"%(domain, node)
    if node != None and port != None and link == None:
        return "urn:ogf:network:domain=%s:node=%s:port:%s"%(domain, node, port)
    if node != None and port != None and link != None:
        return "urn:ogf:network:domain=%s:node=%s:port=%s:link=%s"%(domain, node, port, link)
    else:
        return None

# TODO: module name should be in settings
def dispatch_parse_xml(element, parent):
    from periscope.topology.models import NAMESPACE_PREFIX_MAP

    if element.namespaceURI not in NAMESPACE_PREFIX_MAP:
        raise UnknownXMLNamespaceException, \
            "Unknown namespace (" + element.namespaceURI + ")"
        
    class_name = NAMESPACE_PREFIX_MAP[element.namespaceURI] + \
                    element.localName[0].capitalize() + element.localName[1:]
    clazz = getattr(__import__('periscope').topology.models, class_name)
        
    return clazz.parse_xml(element, parent)

# As bizarre as it sounds, DOM doesn't provide a getElementsByTag
# that gets from only the immediate children.
def get_qualified_xml_elements(element, ns, name):
    elements = []
    for child in element.childNodes:
        if isinstance(child, dom.Element):
            if child.namespaceURI == ns and child.localName == name:
                elements.append(child)
    return elements

def get_unique_xml_child(element, ns, name):
    # XXX: Maybe namespace could be None?
    assert element != None and ns != None and name != None
    
    children = get_qualified_xml_elements(element, ns, name)
    if len(children) > 1:
        raise Exception, element.localName + ": has more than one " + \
                         name + " element!"
    
    if len(children) == 1:
        return children[0]
    return None
   

def parse_xml_unique_text_element(xmlparent, ns, name):
    child_element = get_unique_xml_child(xmlparent, ns, name)
    # Ignore if empty capacity element (e.g. <unis:capacity/>)
    if child_element and child_element.firstChild:
        if not isinstance(child_element.firstChild, dom.Text):
            raise UNISXMLParsingException, \
                xmlparent.localName + ":" + name + " element must have text content!"
        return child_element.firstChild.data.strip()
    return None  

def parse_xml_unique_element(xmlparent, parent, ns, name, clazz):
    xmlchild_element = get_unique_xml_child(xmlparent, ns, name)
    if xmlchild_element:
        return clazz.parse_xml(xmlchild_element, parent)
    return None

def parse_xml_multiple_element(xmlparent, parent, ns, name, clazz):
    parsed_children = []
    xmlchild_elements = get_qualified_xml_elements(xmlparent, ns, name)
    for xmlchild in xmlchild_elements:
        parsed_children.append(clazz.parse_xml(xmlchild, parent))
    return parsed_children

def parse_xml_properties_bag(element, ns, type, parent):
    parsed_properties = []
    properties_bag_element = get_unique_xml_child(element, ns, type+'PropertiesBag')
                                              
    if properties_bag_element:
        for properties_element in properties_bag_element.childNodes:
            if not isinstance(properties_element, dom.Element):
                continue
            
            if not properties_element.localName == type + 'Properties':
                raise UNISXMLParsingException, \
                    type + "PropertiesBag's children must be " + type + "Properties!"
            try:
                parsed_properties.append(
                        dispatch_parse_xml(properties_element, parent))
            except UnknownXMLNamespaceException:
                # TODO: create an UnknownNSProperties or something
                pass
    
    return parsed_properties

def assert_xml_element(element, ns, name):
    # Note that we currently don't support extensions of the base elements
    assert isinstance(element, dom.Element) and \
            element.namespaceURI == ns and \
            element.localName == name, \
            name.capitalize() + ".parse_xml called on wrong element?"

def save_m2m_through_table(m2m_field, source, target):
    m2mtable = m2m_field.through()
    setattr(m2mtable, m2m_field.source_field_name, source)
    setattr(m2mtable, m2m_field.target_field_name, target)
    m2mtable.save()    
    
# TODO: break this monster down into smaller functions
def save_parsed_elements(root):
    from periscope.topology.models import Relation, Network, Hop, NetworkObject
    from collections import deque
    # We save networks, relations and hops for last (they use idRefs)
    # TODO: include EndPointPair when ready
    unisid_object_map = {}
    networks = set()
    relations = set()
    hops = set()
    
    worklist = deque()
    worklist.append(root)
    while worklist:
        obj = worklist.pop()
        # XXX: *Very* ugly way of avoiding duplicates in worklist
        try:
            while True:
                worklist.remove(obj)
        except ValueError:
            pass
        
        if isinstance(obj, Network):
            networks.add(obj)
        if isinstance(obj, Relation):
            relations.add(obj)
        if isinstance(obj, Hop):
            hops.add(obj)
        
        local_worklist = []
        local_field_names = []
        for field in obj._meta.fields:
            local_field_names.append(field.name)
            if not (isinstance(field, related.ForeignKey) or \
                    isinstance(field, related.OneToOneField)):
                continue
            
            # Automatic fields added by Django for inheritance
            if field.name.endswith('_ptr'):
                continue
               
            fvalue = getattr(obj, field.name)
            if fvalue == None:
                continue 
                
            # There's a bug (?) in Django that it doesn't save the related
            # key if the field was set before the object was saved
            if fvalue.id:
                setattr(obj, field.name, fvalue)
                # object already saved
                continue
            
            # We depend on this object to be saved first
            local_worklist.append(fvalue)
        
        # If we have unsaved dependencies, add to worklist and restart
        if local_worklist:
            worklist.append(obj)
            worklist.extend(local_worklist)
            continue
        
        # Save ourselves if needed so our children can use the 
        # saved object as the parent. We also update the map.
        if not obj.id:
            obj.save()
            # We will use this later for resolving idRefs
            if isinstance(obj, NetworkObject):
                if obj.unis_id:
                    if obj.unis_id in unisid_object_map:
                        raise UNISXMLParsingException, \
                            "UNIS ids must be unique; offending id: " + obj.unis_id
               
                    unisid_object_map[obj.unis_id] = obj
                
                elif obj.unis_idref:
                    if obj.unis_idref in unisid_object_map:
                        raise UNISXMLParsingException, \
                            "UNIS idRefs must be unique; offending idRef: " + \
                            obj.unis_idref
                
                    unisid_object_map[obj.unis_idref] = obj
            
        
        def get_unsaved_parsed_children(obj, fname):
            unsaved_children = []
            
            if not hasattr(obj, 'parsed_'+fname):
                return unsaved_children 
            
            fvalue = getattr(obj, 'parsed_' + fname)
            if not fvalue:
                return unsaved_children 
            
            # XXX: For now we only use dicts for idRefs 
            if isinstance(fvalue, dict):
                return unsaved_children
            
            for child in fvalue:
                if not child.id:
                    unsaved_children.append(child)
            return unsaved_children
        
        
        for field in obj._meta.many_to_many:
            local_field_names.append(field.name)
            local_worklist.extend(get_unsaved_parsed_children(obj, field.name))
            
        # We also need to get the related children
        for fname in obj._meta.get_all_field_names():
            if fname in local_field_names:
                continue
            if not hasattr(obj, fname):
                continue
            
            fvalue = getattr(obj, fname)
            if not isinstance(fvalue, Manager):
                continue
            
            local_worklist.extend(get_unsaved_parsed_children(obj, fname))
        
        # At this point we need to save many_to_many relationships, but
        # we can only do it after all the other instances have been saved
        if local_worklist:
            worklist.append(obj)
            worklist.extend(local_worklist)
            continue
        
        # Now we must create all the m2m table entries
        for field in obj._meta.many_to_many:
            if not hasattr(obj, 'parsed_'+field.name):
                continue 
            
            fvalue = getattr(obj, 'parsed_'+field.name)
            # XXX: For now we only use dicts for idRefs, 
            #   which get resolved only at the end
            if not fvalue or isinstance(fvalue, dict):
                continue 
            
            # The M2M field doesn't have the attributes we need,
            # so we fetch the manager instead.
            field = getattr(obj, field.name)
            for child in fvalue:
                assert child.id
                save_m2m_through_table(field, obj, child)
    
    def get_create_reference(idref, unisid_object_map, root):
        reference = unisid_object_map.get(idref, None)
        # If we haven't saved this object yet, it might be external.
        # We need to create a place holder for it (note the use of idRef).
        if reference == None:
            reference = type()
            reference.parent = root
            reference.unis_idref = idref
            reference.save()
            unisid_object_map[idref] = reference
        return reference
    
    # Now all that's left is resolving idRefs
    # TODO: right now this is very specific to the classes, it could be 
    #   generalized later (e.g. special naming for parsed field of idRefs)
    for network in networks:
        for (type, idrefs) in network.parsed_idrefs.items():
            for idref in idrefs:
                reference = get_create_reference(idref, unisid_object_map, root)
                field = getattr(network, type.__name__.lower()+"s")
                save_m2m_through_table(field, network, reference)
    
    for relation in relations:
        for (type, idrefs) in relation.parsed_targets.items():
            for idref in idrefs:
                reference = get_create_reference(idref, unisid_object_map, root)
                relation.targets.add(reference)
    
    # TODO: Hops, EndPointPairs
        
        
