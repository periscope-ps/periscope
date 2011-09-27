import time
from datetime import datetime, timedelta
import xml.dom.minidom as dom

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from periscope.topology.lib.util import create_urn, get_unique_xml_child, \
    parse_xml_properties_bag, parse_xml_multiple_element, assert_xml_element, \
    parse_xml_unique_text_element, parse_xml_unique_element, \
    get_qualified_xml_elements

from periscope.topology.error import UNISXMLParsingException, \
    UnknownXMLNamespaceException


###############################################################################
# UNIS Base
#
# TODO: Figure out if some elements can be freewheeling, or are all
#   xml elements going to be enclosed in a UNSI topology element?
# 
# TODO: Can a Topology contain TopologyS, can Domain contain DomainS?
# TODO: Description and Comment are missing from all elements
#
# XXX: Right now, for the most part, we just ignore if there are extra 
#   elements/attributes (propertiesBag are an exception, they must contain
#   only elements with local name <type>Properties)
#
# XXX: The way the model is defined, any NetworkObject can be contained in
#   any other NetworkObject (i.e. a node could be inside a link). Restrictions
#   to avoid this should be enforced on the save() methods of each class.
#   See the xml_parse() method for an example.
#
# XXX: Some basic elements are mapped directly as CharField instead
#   of their own class (e.g. type, capacity, etc).
#
# XXX: Maybe Properties should inherit from an abstract UNISProperties.
#
###############################################################################

BASE_NAMESPACE = "http://ogf.org/schema/network/topology/unis/20100528/" 


class Lifetime(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.begin + ' -> ' + self.end
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'lifetime')
        
        # XXX: we only accept unix type for time elements, and ms for duration  
        lifetime = Lifetime()
        
        start_element = get_unique_xml_child(element, BASE_NAMESPACE, 'start')
        if start_element == None:
            raise UNISXMLParsingException, \
                "lifetime element must contain start element!"
        if not start_element.hasAttribute('type'):
            raise UNISXMLParsingException, \
                "lifetime:start element must have type attribute!"
        if start_element.getAttribute('type') != "unix":
            raise UNISXMLParsingException, \
                "lifetime:start element has unknown type (must be unix)"
        if not isinstance(start_element.firstChild, dom.Text):
            raise UNISXMLParsingException, \
                "lifetime:start element must have text content!"
        # Everything is fine, create start datetime
        lifetime.start = datetime.utcfromtimestamp(start_element.firstChild
                                                   .data.strip())
        
        end_element = get_unique_xml_child(element, BASE_NAMESPACE, 'end')
        if end_element:
            if not end_element.hasAttribute('type'):
                raise UNISXMLParsingException, \
                    "lifetime:end element must have type attribute!"
            if end_element.getAttribute('type') != "unix":
                raise UNISXMLParsingException, \
                    "lifetime:end element has unknown type (must be unix)"
            if not isinstance(end_element.firstChild, dom.Text):
                raise UNISXMLParsingException, \
                    "lifetime:end element must have text content!"
            # Everything is fine, create end datetime
            lifetime.end = datetime.utcfromtimestamp(end_element.firstChild
                                                     .data.strip())
        
        duration_element = get_unique_xml_child(element, BASE_NAMESPACE, 'duration')
        if duration_element:
            if end_element:
                raise UNISXMLParsingException, \
                    "lifetime element must contain *either* duration *or* end element!"
            if not duration_element.hasAttribute('type'):
                raise UNISXMLParsingException, \
                    "lifetime:end element must have type attribute!"
            if duration_element.getAttribute('type') != "ms":
                raise UNISXMLParsingException, \
                    "lifetime:end element has unknown type (must be ms)"
            if not isinstance(end_element.firstChild, dom.Text):
                raise UNISXMLParsingException, \
                    "lifetime:end element must have text content!"
            # Everything is fine, create end datetime
            lifetime.end = lifetime.start + timedelta(milliseconds=int(
                                            duration_element.firstChild.data.strip()))
        
        lifetime.parsed_parent = parent
        return lifetime

# TODO: GFR: These are probably not useful having _everything_ optional.
#   Maybe check on save for specific subsets that should exist together. 
class Location(models.Model):
    continent = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    institution = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    street_address = models.CharField(max_length=255, null=True)
    floor = models.CharField(max_length=255, null=True)
    room = models.CharField(max_length=255, null=True)
    cage = models.CharField(max_length=255, null=True)
    rack = models.CharField(max_length=255, null=True)
    shelf = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    
    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'location')
        
        location = Location()
        
        elements = {}
        elements['continent'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'continent')
        elements['country'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'country')
        elements['zipcode'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'zipcode')
        elements['state'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'state')
        elements['institution'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'institution')
        elements['city'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'city')
        elements['street_address'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'street_address')
        elements['floor'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'floor')
        elements['room'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'room')
        elements['cage'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'cage')
        elements['rack'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'rack')
        elements['shelf'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'shelf')
        elements['latitude'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'latitude')
        elements['longitude'] =  get_unique_xml_child(element, BASE_NAMESPACE, 'longitude')
        
        
        for e in elements:        
            if elements[e] is None:
                pass
            elif isinstance(elements[e].firstChild, dom.Text):
                setattr(location, e, elements[e].firstChild.data.strip())
            else:
                raise UNISXMLParsingException, "%s element must have text content!" % (e)
            
        
        return location
        
# TODO: Same here (see Location).
class Contact(models.Model):
    parent = models.ForeignKey('Node', related_name="contacts")
    priority = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    administrator = models.CharField(max_length=255, null=True)
    institution = models.CharField(max_length=255, null=True)
    
    class Meta:
        app_label = 'topology'
        
class Role(models.Model):
    value = models.CharField(max_length=255)
    
    class Meta:
        app_label = 'topology'
        
    def __unicode__(self):
        return self.value

class Address(models.Model):
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.value
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'address')
        
        address = Address()
        
        if not isinstance(element.firstChild, dom.Text):
            raise UNISXMLParsingException, "address element must have text content!"
        
        address.value = element.firstChild.data.strip()
        if element.hasAttribute('type'):
            address.type = element.getAttribute('type')
            
        return address

    
class Name(models.Model):
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.value

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'name')
        
        name = Name()
        
        if not isinstance(element.firstChild, dom.Text):
            raise UNISXMLParsingException, "name element must have text content!"
        
        name.value = element.firstChild.data.strip()
        if element.hasAttribute('type'):
            name.type = element.getAttribute('type')
            
        return name

class Description(models.Model):
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'topology'

    def __unicode__(self):
        return self.value

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'description')

        description = Description()

        if not isinstance(element.firstChild, dom.Text):
            raise UNISXMLParsingException, "description element must have text content!"

        description.value = element.firstChild.data.strip()
        if element.hasAttribute('type'):
            description.type = element.getAttribute('type')

        return description

def check_valid_parent(parent, valid_classes=(), optional=False, error_msg=''):
    if optional and parent == None:
        return
    if parent.__class__ not in valid_classes:
        raise UNISXMLParsingException, error_msg
     

class NetworkObject(models.Model):
    parent = models.ForeignKey('self', null=True, related_name='children')
    unis_id = models.CharField(max_length=255, unique=True, null=True)
    unis_idref = models.CharField(max_length=255, null=True)
    lifetime = models.OneToOneField(Lifetime, null=True, related_name='parent')
    type = models.CharField(max_length=255, null=True)
    # This solves the reuse of Name without having to specialize it
    names = models.ManyToManyField(Name, through='NetworkObjectNames')
    descriptions = models.ManyToManyField(Description, through='NetworkObjectDescriptions')
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.unis_id or self.unis_idref or ''

    def save(self, *args, **kwargs):
        # NetworkObject must be instantiated as a subclass
        if self.pk == None and (self.__class__ == NetworkObject or 
                                not issubclass(self.__class__, NetworkObject)):
            raise UNISXMLParsingException, "NetworkObject must be subclassed."
        super(NetworkObject, self).save(*args, **kwargs)
    
    def toRealType(self):
        if hasattr(self, 'port'):
            return self.port
        elif hasattr(self, 'node'):
            return self.node
        elif hasattr(self, 'link'):
            return self.link
        elif hasattr(self, 'topology'):
            return self.topology
        elif hasattr(self, 'domain'):
            return self.domain
        elif hasattr(self, 'service'):
            return self.service
        elif hasattr(self, 'path'):
            return self.path
        elif hasattr(self, 'endpointpair'):
            return self.endpointpair
        else:
            raise UNISXMLParsingException, "NetworkObject is not a known subclass."

    # Each class is responsible for parsing its own element. This includes
    # parsing all its children (or asking them when appropriate). Whenever
    # there is a set of elements (e.g. names), the parsed children of that
    # type will be stored in parsed_<relatedname> (e.g. parsed_names) as
    # a list (i.e. parsed_names = [Name, Name, Name, etc]). 
    @classmethod
    def parse_xml(cls, element, parent):
        # Note that we currently don't support extensions of the base elements
        if not (isinstance(element, dom.Element) and \
                element.namespaceURI == BASE_NAMESPACE):
            raise UNISXMLParsingException, \
                "NetworkObject.parse_xml called on non-UNIS base!"
        
        networkobj = cls()
        networkobj.parent = parent
        
        # Parse attributes id, idRef
        networkobj.unis_id = element.getAttribute('id').strip() or None
        networkobj.unis_idref = element.getAttribute('idRef').strip() or None
        
        if not (networkobj.unis_id or networkobj.unis_idref):
            raise UNISXMLParsingException, \
                "UNIS network object must have either id or idRef!"
                
        if networkobj.unis_id and networkobj.unis_idref:
            raise UNISXMLParsingException, \
                "UNIS network object cannot have both id and idRef!"
                
        # Parse type
        networkobj.type = parse_xml_unique_text_element(element, BASE_NAMESPACE, 'type')
        
        networkobj.lifetime = parse_xml_unique_element(element, networkobj, 
                                                       BASE_NAMESPACE, 'lifetime',
                                                       Lifetime)
        
        networkobj.parsed_names = parse_xml_multiple_element(element, networkobj,
                                                             BASE_NAMESPACE, 'name',
                                                             Name)
        networkobj.parsed_descriptions = parse_xml_multiple_element(element, networkobj,
                                                             BASE_NAMESPACE, 'description',
                                                             Description)        
        # Parse relations (they are general enough to be done here)
        networkobj.parsed_relations = parse_xml_multiple_element(element, networkobj,
                                                             BASE_NAMESPACE, 'relation',
                                                             Relation)
        return networkobj

class NetworkObjectNames(models.Model):
    name = models.ForeignKey(Name, unique=True, related_name='parent')
    networkobject = models.ForeignKey(NetworkObject)
    
class NetworkObjectDescriptions(models.Model):
    description = models.ForeignKey(Description, unique=True, related_name='parent')
    networkobject = models.ForeignKey(NetworkObject)

def parse_xml_base_idrefs(element, include=(), exclude=()):
    parsed_refs_map = {}
    # Parse each idRef type in turn, knowing the type helps us later on
    for (type, typename) in BASETYPE_NAME_PAIRS:
        # TODO: should exclusions error?
        if include and typename not in include:
            continue
        if typename in exclude:
            continue
        
        parsed_idrefs = []
        
        idref_elements = get_qualified_xml_elements(element, BASE_NAMESPACE, 
                                                    typename + "IdRef")
        for idref_element in idref_elements:
            if not isinstance(idref_element.firstChild, dom.Text):
                raise UNISXMLParsingException, \
                    typename + "IdRef element must have text content!"
            parsed_idrefs.append(idref_element.firstChild.data.strip())
        
        if len(parsed_idrefs) > 0:
            parsed_refs_map[type] = parsed_idrefs
    
    return parsed_refs_map
            
            
# XXX: Relation parsed_targets is a map indexed by NetworkObject Type
class Relation(models.Model):
    parent = models.ForeignKey(NetworkObject, related_name='relations')
    type = models.CharField(max_length=255)
    targets = models.ManyToManyField(NetworkObject, related_name='relations_target')
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return '%s: %s -> %s' % (self.type, self.parent.unis_id, self.targets.all())

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'relation')
        check_valid_parent(parent, valid_classes=[t[0] for t in BASETYPE_NAME_PAIRS])
        
        relation = Relation()
        relation.parent = parent
        
        if not element.hasAttribute('type'):
            raise UNISXMLParsingException, "relation element must have type attribute!"
        
        relation.type = element.getAttribute('type')
        
        relation.parsed_targets = parse_xml_base_idrefs(element)
        relation.parsed_properties_bag = \
                parse_xml_properties_bag(element, BASE_NAMESPACE, 'relation', relation)
        relation.parsed = True
        return relation


def parse_xml_unis_properties(cls, element, parent, bag_prefix, valid_parent_classes=()):
    check_valid_parent(parent, valid_classes=valid_parent_classes,
        error_msg=element.localName + " outside " + bag_prefix + "PropertiesBag?")
    assert_xml_element(element.parentNode, BASE_NAMESPACE, bag_prefix+'PropertiesBag')
    
    properties = cls()
    properties.parent = parent
    
    return properties  


class RelationProperty(models.Model):
    parent = models.ForeignKey(Relation, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.type + ': ' + self.target
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'relation', (Relation,))


def parse_xml_base_children(element, parent, include=(), exclude=()):
    parent.parsed_children = []
    # Parse all possible base elements first
    for (basetype, typename) in BASETYPE_NAME_PAIRS:
        # TODO: should exclusions error?
        if include and typename not in include:
            continue
        if typename in exclude:
            continue
        
        parsed_base_children = parse_xml_multiple_element(element, parent, 
                                                          BASE_NAMESPACE,
                                                          typename, basetype)
        if len(parsed_base_children) > 0:
            parent.parsed_children.extend(parsed_base_children)
                
 
class Topology(NetworkObject):
    
    class Meta:
        app_label = 'topology'
      
    def save(self, *args, **kwargs):
        # Topology doesn't have parents
        if self.parent != None:
            raise UNISXMLParsingException, \
                "Topology isn't supposed to have a parent element."
        super(Topology, self).save(*args, **kwargs)
    
    # TODO: These methods should also check for relations
    def get_domains(self):
        return Domain.objects.filter(parent=self)
        
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'topology')
        check_valid_parent(parent, valid_classes=(), optional=True,
                          error_msg="Topology isn't supposed to have a parent element.")
        
        if not element.hasAttribute('id'):
            element.setAttribute('id', 'topo' + str(time.time()))
        
        topology = super(Topology, cls).parse_xml(element, parent)
        
        parse_xml_base_children(element, topology)
        topology.parsed_properties_bag = \
                parse_xml_properties_bag(element, BASE_NAMESPACE, 'topology', topology)
        return topology


class TopologyProperties(models.Model):
    parent = models.ForeignKey(Topology, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
  
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'topology', (Topology,))
    
class Domain(NetworkObject):
    
    class Meta:
        app_label = 'topology'
    
    # TODO: These methods should also check for relations
    def get_nodes(self):
        return Node.objects.filter(parent=self)
    
    def get_links(self):
        return Link.objects.filter(parent=self)
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'domain')
        check_valid_parent(parent, valid_classes=(Topology,),
                          error_msg="Domain must have Topology parent element.")
        
        domain = super(Domain, cls).parse_xml(element, parent)
        
        parse_xml_base_children(element, domain, exclude=('port', 'service',))
        domain.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE,
                                                            'domain', domain)
        return domain

class DomainProperties(models.Model):
    parent = models.ForeignKey(Domain, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
    
    def toRealType(self):
        for subclass in self.__class__.__subclasses__():
            if hasattr(self, subclass.__name__.lower()):
                return getattr(self, subclass.__name__.lower())
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'domain', (Domain,))
    
class NodeAddresses(models.Model):
    node = models.ForeignKey('Node')
    address = models.ForeignKey(Address, unique=True)
                 
class Node(NetworkObject):
    location = models.OneToOneField(Location, null=True)
    role = models.OneToOneField(Role, null=True)
    # This solves the reuse of Address without having to specialize it
    addresses = models.ManyToManyField(Address, through='NodeAddresses')
    
    class Meta:
        app_label = 'topology'
    
    # TODO: These methods should also check for relations
    def get_ports(self):
        return Port.objects.filter(parent=self)
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'node')
        check_valid_parent(parent, valid_classes=(Topology, Domain,),
                          error_msg="Node must have Topology or Domain parent element.")
        
        node = super(Node, cls).parse_xml(element, parent)
        
        node.location = parse_xml_unique_element(element, node, BASE_NAMESPACE,
                                                 'location', Location)
        
        node.role = parse_xml_unique_element(element, node, BASE_NAMESPACE,
                                             'role', Role)
        
        node.parsed_addresses = parse_xml_multiple_element(element, node, 
                                                          BASE_NAMESPACE,
                                                          'address', Address)
        
        parse_xml_base_children(element, node, include=('port', 'service',))
        node.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE, 
                                                             'node', node)
        return node
    
class NodeProperties(models.Model):
    parent = models.ForeignKey(Node, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'node', (Node,))
    
class PortAddresses(models.Model):
    port = models.ForeignKey('Port')
    address = models.ForeignKey(Address, unique=True)
          
class Port(NetworkObject):
    capacity = models.CharField(max_length=255, null=True)
    # This solves the reuse of Address without having to specialize it
    addresses = models.ManyToManyField(Address, through='PortAddresses')
    
    class Meta:
        app_label = 'topology'
    
    # TODO: These methods should also check for relations
    def get_links(self):
        return Link.objects.filter(parent=self)
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'port')
        check_valid_parent(parent, valid_classes=(Topology, Node,),
                          error_msg="Port must have Topology or Node parent element.")
        
        port = super(Port, cls).parse_xml(element, parent)
        
        # Parse capacity
        port.capacity = parse_xml_unique_text_element(element, BASE_NAMESPACE, 
                                                      'capacity')
            
        port.parsed_addresses = parse_xml_multiple_element(element, port,
                                                          BASE_NAMESPACE,
                                                          'address', Address)
        
        parse_xml_base_children(element, port, include=('link',))
        port.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE, 
                                                          'port', port)
        return port
      
class PortProperties(models.Model):
    parent = models.ForeignKey(Port, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
    
    def toRealType(self):
        for subclass in self.__class__.__subclasses__():
            if hasattr(self, subclass.__name__.lower()):
                return getattr(self, subclass.__name__.lower())
    
    def toHTML(self):
        return ''
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'port', (Port,))
  
class GlobalName(models.Model):
    value = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True)
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.value
    
# TODO: see if ports should be enforced
class Link(NetworkObject):
    global_name = models.OneToOneField(GlobalName, null=True)
    directed = models.BooleanField(default=True)
    
    class Meta:
        app_label = 'topology'
    
    # TODO: This should be revised if Link will be 'adirectional'
    def get_sink(self):
        try:
            return self.relations.get(type='sink').targets.all()[0]
        except:
            return None
    
    def get_source(self):
        try:
            return self.relations.get(type='source').targets.all()[0]
        except:
            return None
    
    def get_end_points(self):
        if self.directed:
            return ( self.get_source(), self.get_sink() )
        else:
            relations = self.relations.filter(type='endPoint');
            return ( relations[0].targets.all()[0], relations[1].targets.all()[0] )
        
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'link')
        check_valid_parent(parent, valid_classes=(Topology, Domain, Port,),
            error_msg="Link must have Topology, Domain or Port parent element.")
        
        link = super(Link, cls).parse_xml(element, parent)
        
        link.global_name = parse_xml_unique_element(element, link, BASE_NAMESPACE,
                                                    'globalName', GlobalName)
        
        link.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE,
                                                          'link', link)
        # TODO: Refactor "get_boolean_attr"
        directed = element.getAttribute('directed')
        if directed:
            if directed == "true":
                link.directed = True
            elif directed == "false":
                link.directed = False
            else:
                raise UNISXMLParsingException, \
                    "Link's directed attributed must be either 'true' or 'false'!"
                    
        return link
     
class LinkProperties(models.Model):
    parent = models.ForeignKey(Link, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'link', (Link,))
  
# GFR: I'm not sure about this one, I chose to make the nodes, links and ports
#   explicitly defined instead of just a single 'references' to NetworkObject.
#   Not really consistent with similar cases on the rest of the model though.
class Network(NetworkObject):
    nodes = models.ManyToManyField(Node, related_name="networks")
    ports = models.ManyToManyField(Port, related_name="networks")
    links = models.ManyToManyField(Link, related_name="networks")
    
    class Meta:
        app_label = 'topology'

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'network')
        check_valid_parent(parent, valid_classes=(Topology, Domain,),
            error_msg="Network must have Topology or Domain parent element.")
        
        network = super(Network, cls).parse_xml(element, parent)
        
        network.parsed_idrefs = parse_xml_base_idrefs(element, 
                                                      include=('node', 'port', 'link'))
        
        network.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE, 
                                                             'network', network)
        return network
    
    
class NetworkProperties(models.Model):
    parent = models.ForeignKey(Network, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'network', (Network,))
    
class Path(NetworkObject):
    
    class Meta:
        app_label = 'topology'

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'path')
        check_valid_parent(parent, valid_classes=(Topology, Domain,),
            error_msg="Path must have Topology or Domain parent element.")
        
        path = super(Path, cls).parse_xml(element, parent)
        
        path.parsed_hops = parse_xml_multiple_element(element, path, BASE_NAMESPACE,
                                                      'hop', Hop)
        
        path.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE,
                                                          'path', path)
        return path
    
class PathProperties(models.Model):
    parent = models.ForeignKey(Path, related_name='properties_bag')
     
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'path', (Path,))
    
class Hop(models.Model):
    parent = models.ForeignKey(Path, related_name='hops')
    unis_id = models.CharField(max_length=255)
    target = models.ForeignKey(NetworkObject, related_name='hops_target')
    
    class Meta:
        app_label = 'topology'
    
    def __unicode__(self):
        return self.unis_id or self.unis_idref or ''
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'hop')
        check_valid_parent(parent, valid_classes=(Path,),
                          error_msg="Hop must have Path parent element.")
        
        hop = Hop()
        hop.parent = parent
        hop.unis_id = element.getAttribute('id').strip() or None
        
        hop.parsed_target = parse_xml_base_idrefs(element, 
                                                  exclude=('topology', 'service'))
        if len(hop.parsed_target) != 1:
            raise UNISXMLParsingException, \
                "hop element must have one (and only one) idRef!"
                
        hop.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE,
                                                         'hop', hop)
        return hop
    
  
class HopProperties(models.Model):
    parent = models.ForeignKey(Hop, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'hop', (Hop,))
          
class Service(NetworkObject):
    
    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, BASE_NAMESPACE, 'service')
        check_valid_parent(parent, valid_classes=(Node,), optional=True,
                          error_msg="Service must have Node parent element.")
        
        service = super(Service, cls).parse_xml(element, parent)
        
        service.parsed_properties_bag = parse_xml_properties_bag(element, BASE_NAMESPACE,
                                                             'service', service)
        return service
    
  
class ServiceProperties(models.Model):
    parent = models.ForeignKey(Service, related_name='properties_bag')
    
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        return parse_xml_unis_properties(cls, element, parent, 'service', (Service,))
  

class EndPointPair(NetworkObject):
    # TODO (AH): Endpoint parsing
    src = models.ForeignKey(NetworkObject, null=True, 
                            related_name='endpointpairs_src_target')
    dst = models.ForeignKey(NetworkObject, null=True, 
                            related_name='endpointpairs_dst_target')
    
    class Meta:
        app_label = 'topology'

class EndPointPairNames(models.Model):
    endpointpair = models.ForeignKey(EndPointPair)
    name = models.ForeignKey(Name, unique=True)   

BASETYPE_NAME_PAIRS = (
    (Topology,    'topology'),
    (Domain,      'domain'),
    (Node,        'node'),
    (Port,        'port'),
    (Link,        'link'),
    (Path,        'path'),
    (Network,     'network'),
    (Service,     'service'),
)

###############################################################################
# DCN
#
# TODO: Path, Hop, BidirectionPath
#
###############################################################################

DCN_NAMESPACE = "http://ogf.org/schema/network/topology/ctrlPlane/20080828/"

# TODO: domainSignature
class DCNTopologyProperties(TopologyProperties):
    idc_id = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'topology'
        
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, DCN_NAMESPACE, 'topologyProperties')
        
        properties = super(DCNTopologyProperties, cls).parse_xml(element, parent)
        properties.idc_id = parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                          'idcId')
        return properties
        
class DCNPortProperties(PortProperties):
    capacity =  models.CharField(max_length=255, null=True)
    maximum_reservable_capacity =  models.CharField(max_length=255, null=True)
    minimum_reservable_capacity =  models.CharField(max_length=255, null=True)
    granularity =  models.CharField(max_length=255, null=True)
    unreserverd_capacity = models.CharField(max_length=255, null=True)

    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, DCN_NAMESPACE, 'portProperties')
        
        properties = super(DCNPortProperties, cls).parse_xml(element, parent)
        
        properties.capacity = parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                            'capacity')
        properties.granularity = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                               'granularity')
        properties.maximum_reservable_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'maximumReservableCapacity')
        properties.minimum_reservable_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'minimumReservableCapacity')
        properties.unreserved_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'unreservedCapacity')
        return properties
    
class DCNLinkProperties(LinkProperties):
    capacity =  models.CharField(max_length=255, null=True)
    maximum_reservable_capacity =  models.CharField(max_length=255, null=True)
    minimum_reservable_capacity =  models.CharField(max_length=255, null=True)
    granularity =  models.CharField(max_length=255, null=True)
    unreserverd_capacity = models.CharField(max_length=255, null=True)
    traffic_engineering_metric =  models.CharField(max_length=255)
    
    class Meta:
        app_label = 'topology'

    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, DCN_NAMESPACE, 'linkProperties')
        properties = super(DCNLinkProperties, cls).parse_xml(element, parent)
        
        properties.capacity = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                            'capacity')
        properties.granularity = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                               'granularity')
        properties.maximum_reservable_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'maximumReservableCapacity')
        properties.minimum_reservable_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'minimumReservableCapacity')
        properties.unreserved_capacity = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'unreservedCapacity')
        properties.traffic_engineering_metric = \
                        parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                      'trafficEngineeringMetric')
        
        properties.parsed_link_protection_types = \
            parse_xml_multiple_element(element, properties, DCN_NAMESPACE, 
                                       'linkProtectionTypes', DCNLinkProtectionType)
        
        properties.parsed_administrative_groups = \
            parse_xml_multiple_element(element, properties, DCN_NAMESPACE, 
                                    'administrativeGroups', DCNLinkAdministrativeGroup)
            
        properties.parsed_switching_capability_descriptors = \
            parse_xml_multiple_element(element, properties, DCN_NAMESPACE, 
                                       'SwitchingCapabilityDescriptors', 
                                       DCNSwitchingCapabilityDescriptor)
        return properties
    
class DCNLinkProtectionType(models.Model):
    parent = models.ForeignKey(DCNLinkProperties, related_name='link_protection_types')
    value =  models.CharField(max_length=255)
   
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        check_valid_parent(parent, valid_classes=(DCNLinkProperties,),
                           error_msg="linkProtectionTypes not in linkProperties!")
        assert_xml_element(element, DCN_NAMESPACE, 'linkProtectionTypes')
        
        ptype = DCNLinkProtectionType()
        ptype.parent = parent
        
        if not isinstance(element.firstChild, dom.Text):
            raise UNISXMLParsingException, \
                "linkProtectionTypes element must have text content!"
        
        ptype.value = element.firstChild.data.strip()
            
        return ptype
    
            
class DCNLinkAdministrativeGroup(models.Model):
    parent = models.ForeignKey(DCNLinkProperties, related_name='administrative_groups')
    group = models.IntegerField()
    group_id = models.CharField(max_length=255, null=True)
   
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        check_valid_parent(parent, valid_classes=(DCNLinkProperties,),
                           error_msg="administrativeGroups not in linkProperties!")
        assert_xml_element(element, DCN_NAMESPACE, 'administrativeGroups')
        
        admin_group = DCNLinkAdministrativeGroup()
        admin_group.parent = parent
        
        admin_group.group = int(parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                              'group'))
        admin_group.group_id = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                             'groupID')
        return admin_group
    
# TODO: validate that there's at least one SwitchingCapabilitySpecificInfo    
class DCNSwitchingCapabilityDescriptor(models.Model):
    SWITCHING_CAP_TYPE = (
        (u"psc-1", u"psc-1"),
        (u"psc-2", u"psc-2"),
        (u"psc-3", u"psc-3"),
        (u"psc-4", u"psc-4"),
        (u"l2sc", u"l2sc"),
        (u"tdm", u"tdm"),
        (u"lsc", u"lsc"),
        (u"fsc", u"fsc"),
    )
    # TODO: handle xsd:string case
    ENCODING_TYPE = (
        (u"packet", u"packet"),
        (u"ethernet", u"ethernet"),
        (u"pdh", u"pdh"),
        (u"sdh/sonet", u"sdh/sonet"),
        (u"digital wrapper", u"digital wrapper"),
        (u"lambda", u"lambda"),
        (u"fiber", u"fiber"),
        (u"fiberchannel", u"fiberchannel"),
    )
    
    parent = models.ForeignKey(DCNLinkProperties, 
                               related_name='switching_capability_descriptors')
    switching_cap_type = models.CharField(max_length=6, 
                                          choices=SWITCHING_CAP_TYPE)
    encoding_type = models.CharField(max_length=16, choices=ENCODING_TYPE)
   
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        check_valid_parent(parent, valid_classes=(DCNLinkProperties,),
            error_msg="SwitchingCapabilityDescriptors not in linkProperties!")
        assert_xml_element(element, DCN_NAMESPACE, 'SwitchingCapabilityDescriptors')
        
        capdesc = DCNSwitchingCapabilityDescriptor()
        capdesc.parent = parent
        
        cap_type = parse_xml_unique_text_element(element, DCN_NAMESPACE, 
                                                 'switchingcapType')
        if cap_type == None:
            raise UNISXMLParsingException, \
                "SwitchingCapabilityDescriptors must have a switchingcapType element!"
        
        if (cap_type, cap_type) not in \
                        DCNSwitchingCapabilityDescriptor.SWITCHING_CAP_TYPE:
            raise UNISXMLParsingException, \
                "Invalid switchingcapType (" + capdesc.switching_cap_type + ")!"
        
        capdesc.encoding_type = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                              'encodingType')
        if capdesc.encoding_type == None:
            raise UNISXMLParsingException, \
                "SwitchingCapabilityDescriptors must have an encodingType element!"
        
        capdesc.parsed_switching_cap_specific_infos = \
            parse_xml_multiple_element(element, capdesc, DCN_NAMESPACE,
                                       'switchingCapabilitySpecificInfo', 
                                       DCNSwitchingCapabilitySpecificInfo)
        
        if len(capdesc.parsed_switching_cap_specific_infos) == 0:
            raise UNISXMLParsingException, \
                "SwitchingCapabilityDescriptors must have at least one " + \
                "switchingCapabilitySpecificInfo element!"
        
        return capdesc
            
class DCNSwitchingCapabilitySpecificInfo(models.Model):
    parent = models.ForeignKey(DCNSwitchingCapabilityDescriptor, 
                               related_name = 'switching_cap_specific_infos')
    capability = models.CharField(max_length=255, null=True)
    interface_mtu = models.IntegerField(null=True)
    vlan_range_availability = models.CharField(max_length=255, null=True)
    suggested_vlan_range = models.CharField(max_length=255, null=True)
    vlan_translation = models.NullBooleanField()
   
    class Meta:
        app_label = 'topology'
    
    @classmethod
    def parse_xml(cls, element, parent):
        check_valid_parent(parent, valid_classes=(DCNSwitchingCapabilityDescriptor,),
            error_msg="switchingCapabilitySpecificInfo not in " + \
                      "SwitchingCapabilityDescriptors!")
        assert_xml_element(element, DCN_NAMESPACE, 'switchingCapabilitySpecificInfo')
        
        info = DCNSwitchingCapabilitySpecificInfo()
        info.parent = parent
        
        info.capability = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                        'capability')
        info.interface_mtu = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                           'interfaceMTU')
        if info.interface_mtu != None:
            info.interface_mtu = int(info.interface_mtu)
        
        info.vlan_range_availability = \
            parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                          'vlanRangeAvailability')
        
        if info.capability == None and (info.interface_mtu == None or \
                                        info.vlan_range_availability == None):
            raise UNISXMLParsingException, \
                "switchingCapabilitySpecificInfo must have either capability " + \
                "element, or a interfaceMTU and a vlanRangeAvailability elements!"
        
        info.suggested_vlan_range = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                                  'suggestedVLANRange')
        translation = parse_xml_unique_text_element(element, DCN_NAMESPACE,
                                                    'vlanTranslation')
        if translation:
            if translation == "true":
                info.vlan_translation = True
            elif translation == "false":
                info.vlan_translation = False
            else:
                raise UNISXMLParsingException, \
                    "vlanTranslation must be either 'true' or 'false'!"
        
        if info.capability and (info.interface_mtu or info.vlan_range_availability or \
                                info.suggested_vlan_range or info.vlan_translation):
            raise UNISXMLParsingException, \
                "switchingCapabilitySpecificInfo's capability element must be alone!"
        return info


###############################################################################
# TeraPaths
#
###############################################################################

TPS_NAMESPACE = "http://ogf.org/schema/network/topology/terapaths/20100603/"

class TPSPortProperties(PortProperties):
    vlan =  models.CharField(max_length=6, null=True)
    subnet =  models.CharField(max_length=50, null=True)
    base_ip =  models.CharField(max_length=50, null=True)
    subnet_mask =  models.CharField(max_length=50, null=True)
    ip_a = models.CharField(max_length=50, null=True)
    ip_b = models.CharField(max_length=50, null=True)
    broadcast_ip = models.CharField(max_length=50, null=True)
    available = models.CharField(max_length=6, null=True)
    
    # TODO: pretty format this
    def toHTML(self):
        return 'TeraPaths Properties:<br>'\
               '\tvlan: %s<br>'\
               '\tsubnet: %s<br>'\
               '\tbaseIp: %s<br>'\
               '\tsubnetMask: %s<br>'\
               '\tipA: %s<br>'\
               '\tipB: %s<br>'\
               '\tbroadcastIp: %s<br>'\
               '\tavailable: %s<br>' % (self.vlan, self.subnet, self.base_ip,
                                        self.subnet_mask, self.ip_a, self.ip_b,
                                        self.broadcast_ip, self.available)
               
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, TPS_NAMESPACE, 'portProperties')
        
        properties = super(TPSPortProperties, cls).parse_xml(element, parent)
        
        properties.vlan = parse_xml_unique_text_element(element, TPS_NAMESPACE, 'vlan')
        properties.subnet = parse_xml_unique_text_element(element, TPS_NAMESPACE, 
                                                          'subnet')
        properties.base_ip = parse_xml_unique_text_element(element, TPS_NAMESPACE, 
                                                           'baseIp')
        properties.subnet_mask = parse_xml_unique_text_element(element, TPS_NAMESPACE, 
                                                               'subnetMask')
        properties.ip_a = parse_xml_unique_text_element(element, TPS_NAMESPACE, 'ipA')
        properties.ip_b = parse_xml_unique_text_element(element, TPS_NAMESPACE, 'ipB')
        properties.broadcast_ip = parse_xml_unique_text_element(element, TPS_NAMESPACE, 
                                                                'broadcastIp')
        properties.available = parse_xml_unique_text_element(element, TPS_NAMESPACE, 
                                                             'available')
        return properties
    

class TimeSeriesData(models.Model):
    target = models.ForeignKey(NetworkObject, related_name='time_series')
    eventType = models.CharField(max_length=255)
    time = models.DateTimeField()
    value = models.DecimalField(max_digits=23, decimal_places=5)
    
    class Meta:
        app_label = 'topology'
        ordering = ['target', 'eventType', 'time']


#########################################################################################
# Periscope-specific properties
#
# XXX: These are 'internal' properties and shouldn't be exported in any representation 
#########################################################################################

class PeriscopeSavedTopology(models.Model):
    topo = models.TextField()

class PeriscopeDomainProperties(DomainProperties):
    shape = models.OneToOneField('PeriscopeShape')
        
class PeriscopeNodeProperties(NodeProperties):
    shape = models.OneToOneField('PeriscopeShape')
        
class PeriscopePortProperties(PortProperties):
    shape = models.OneToOneField('PeriscopeShape')
    
    
class PeriscopeShape(models.Model):
    SHAPES = (
        (u"rect", u"rect"),
        (u"circle", u"circle"),
        (u"ellipse", u"ellipse"),
    )
    ALIGNS = (
        (u"start", u"start"),
        (u"middle", u"middle"),
        (u"end", u"end"),       
    )
    shape = models.CharField(max_length=10, choices=SHAPES)
    x = models.IntegerField() 
    y = models.IntegerField()
    width = models.IntegerField() 
    height = models.IntegerField()
    fill = models.CharField(max_length=20)
    text_xdisp = models.IntegerField()
    text_ydisp = models.IntegerField()
    text_align = models.CharField(max_length=6, choices=ALIGNS)
    
    
    def toJson(self):
        return '"shape":"%s","x":%s,"y":%s,"width":%s,"height":%s,"fill":"%s"'\
               ',"textXDisp":%s,"textYDisp":%s,"textAlign":"%s"' % \
               (self.shape, self.x, self.y, self.width, self.height, self.fill,
                self.text_xdisp, self.text_ydisp, self.text_align)

###############################################################################
# perfSONAR Topology
#
###############################################################################

NMWG_NAMESPACE = 'http://ggf.org/ns/nmwg/base/2.0/'
NMTB_NAMESPACE = 'http://ogf.org/schema/network/topology/base/20070828/'
NMTL2_NAMESPACE = 'http://ogf.org/schema/network/topology/l2/20070828/'
NMTL3_NAMESPACE = 'http://ogf.org/schema/network/topology/l3/20070828/'
PS_NAMESPACE = 'http://ggf.org/ns/nmwg/tools/org/perfsonar/service/1.0/'


class psHopProperties(HopProperties):
    number =  models.PositiveIntegerField()
    
class CloudNodeProperties(NodeProperties):
    CIDR =  models.CharField(max_length=19, null=True)
    traceroute = models.ManyToManyField(Port, null=True, related_name='traceroute_port')
    bwctl = models.ManyToManyField(Port, null=True, related_name='bwctl_port')
    pinger = models.ManyToManyField(Port, null=True, related_name='pinger_port')
    owamp = models.ManyToManyField(Port, null=True, related_name='owamp_port')

class L3PortProperties(PortProperties):
    netmask =  models.CharField(max_length=16, null=True)
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, NMTL3_NAMESPACE, 'portProperties')
        
        properties = super(L3PortProperties, cls).parse_xml(element, parent)
        
        properties.netmask = parse_xml_unique_text_element(element, NMTL3_NAMESPACE, 'netmask')
        
        return properties


class EventType(models.Model):
    value = models.CharField(max_length=255, unique=True, db_index=True)
    
    class Meta:
        app_label = 'topology'
      
    def __unicode__(self):
        return self.value
    
    @classmethod
    def parse_xml(cls, element, parent):
        assert_xml_element(element, NMTB_NAMESPACE, 'eventtype')
        
        eventtype = EventType()
        
        if not isinstance(element.firstChild, dom.Text):
            raise UNISXMLParsingException, "address element must have text content!"
        
        eventtype.value = element.firstChild.data.strip()
        
        return eventtype


    
class psServiceProperties(ServiceProperties):
    serviceName =  models.CharField(max_length=255, null=True)
    accessPoint =  models.CharField(max_length=255, null=False)
    serviceType =  models.CharField(max_length=255, null=False)
    serviceDescription =  models.CharField(max_length=255, null=True)
    eventTypes =  models.ManyToManyField(EventType, through='psServicePropertiesEventTypes')
    
    @classmethod
    def parse_xml(cls, element, parent):
        print "psServiceProperties is called"
        assert_xml_element(element, PS_NAMESPACE, 'serviceProperties')
        
        properties = super(psServiceProperties, cls).parse_xml(element, parent)
        
        properties.serviceName = parse_xml_unique_text_element(element, PS_NAMESPACE, 'serviceName')
        properties.accessPoint = parse_xml_unique_text_element(element, PS_NAMESPACE, 'accessPoint')
        properties.serviceDescription = parse_xml_unique_text_element(element, PS_NAMESPACE, 'serviceDescription')
        properties.parsed_eventTypes = parse_xml_multiple_element(element, properties, 
                                                          NMWG_NAMESPACE,
                                                          'eventtype', EventType)
        return properties

class psServicePropertiesEventTypes(models.Model):
    psServiceProperties = models.ForeignKey(psServiceProperties)
    eventtype = models.ForeignKey(EventType)

    
class psServiceWatchList(models.Model):
    service = models.ForeignKey(Service, related_name='service')
    event_type = models.ForeignKey(EventType)
    network_object = models.ForeignKey(NetworkObject, related_name='network_object')
    
    class Meta:
        app_label = 'topology'
        unique_together = (('service', 'event_type', 'network_object'),)
    
    def __unicode__(self):
        return "%s->%s->%s" % (self.service, self.event_type, self.network_object)

# TODO: maybe have this somewhere else?
NAMESPACE_PREFIX_MAP = {
    BASE_NAMESPACE: '',
    DCN_NAMESPACE: 'DCN',
    TPS_NAMESPACE: 'TPS',
    NMTL3_NAMESPACE: 'L3',
    PS_NAMESPACE: 'ps',
}
