from piston.handler import BaseHandler
from piston.utils import rc

from periscope.topology.models import Node, Port, Link, EndPointPair, Path

# This is a maximum number of results per query (can be override by max_results)
MAX_RESULTS = 1000

def instance_dict(instance, key_format=None, exclude_keys=['id', 'parent', 'networkobject_ptr']):
    """
    Returns a dictionary containing field names and values for the given instance
    """
    from django.db.models.fields.related import ForeignKey
    if key_format:
        assert '%s' in key_format, 'key_format must contain a %s'
    key = lambda key: key_format and key_format % key or key

    d = {}
    for field in instance._meta.fields:
        attr = field.name
        value = getattr(instance, attr)
        if value is not None and isinstance(field, ForeignKey):
            value = instance_dict(value) # value._get_pk_val()
        if value and key(attr) not in exclude_keys:
            d[key(attr)] = value
    for field in instance._meta.many_to_many:
        if key(field.name) != 'parent' :
            d[key(field.name)] = [instance_dict(obj) for obj in getattr(instance, field.attname).all()]
            if len(d[key(field.name)]) ==0: del d[key(field.name)]
    return d

def node_dict(node):
    """
    Returns a dictonary of the node's UNIS model
    """
    resp = instance_dict(node)
    
    ports = node.get_ports()
    if len(ports) > 0:
        resp['ports'] = []
        for p in ports:
            resp['ports'].append(port_dict(p))
    return resp

def port_dict(port):
    """
    Returns a dictonary of the port's UNIS model
    """
    resp = instance_dict(port)
    links = port.get_links()
    if len(links) > 0:
        resp['links'] = []
        for l in links:
           resp['links'].append(link_dict(l))
    return resp

def link_dict(link):
    """
    Returns a dictonary of the link's UNIS model
    """
    resp = instance_dict(link)
    if link.get_sink():
        resp['sink'] = instance_dict(link.get_sink())
    if link.get_source():
        resp['source'] = instance_dict(link.get_source())
    endpoints = link.get_end_points()
    if endpoints:
        resp['endpoints'] = (instance_dict(endpoints[0]),instance_dict(endpoints[1]))
    return resp


def endpointpair_dict(endpoint):
    """
    Returns a dictonary of the endpoint's UNIS model
    """
    resp = instance_dict(endpoint)
    return resp
    

def path_dict(path):
    """
    Returns a dictonary of the path's UNIS model
    """
    resp = instance_dict(path)
    return resp
                

                
class UNISHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Node
    
    def read(self, request, urn=None):
        base = Node.objects
        
        if urn != None:
            return base.get(unis_id=urn)
        else:
            return base.all()
    
class NodeUNISHandler(BaseHandler):
    allowed_methods = ('GET',)    
    
    def read(self, request, urn=None):
        attrs = self.flatten_dict(request.GET)
        
        if urn:
            try:
                node = Node.objects.get(unis_id=urn) 
                resp = node_dict(node)
                return resp
            except Node.DoesNotExist:
                resp = rc.NOT_HERE
                return resp
        else:
            max_results = MAX_RESULTS
            if 'max_results' in attrs:
                if attrs['max_results'].isdigit():
                    max_results = attrs['max_results']
                del attrs['max_results']
                
            if len(attrs) == 0:
                # no filtering just get all results up to the max results
                nodes = Node.objects.all()[:max_results]
            else:
                nodes = Node.objects.all()
                if 'address' in attrs:
                    nodes = nodes.filter(addresses__value=attrs['address'])
                if 'name' in attrs:
                    nodes = nodes.filter(names__value=attrs['name'])
            
            resp = []
            for n in nodes:
                resp.append(node_dict(n))
            return resp

class PortUNISHandler(BaseHandler):
    allowed_methods = ('GET',)    
    
    def read(self, request, urn=None):
        attrs = self.flatten_dict(request.GET)
        if urn:
            try:
                port = Port.objects.get(unis_id=urn)
                resp = port_dict(port)
                return resp
                
            except Node.DoesNotExist:
                resp = rc.NOT_HERE
                return resp
        else:
            max_results = MAX_RESULTS
            ports = []
            
            if 'max_results' in attrs:
                if attrs['max_results'].isdigit():
                    max_results = attrs['max_results']
                del attrs['max_results']
                
            if len(attrs) == 0:
                # no filtering just get all results up to the max results
                ports = Port.objects.all()[:max_results]
            else:
                ports = Port.objects.all()
                if 'address' in attrs:
                    ports = ports.filter(addresses__value=attrs['address'])
                if 'name' in attrs:
                    ports = ports.filter(names__value=attrs['name'])
                    
            resp = []
            for p in ports:
                resp.append(port_dict(p))
            return resp

class LinkUNISHandler(BaseHandler):
    allowed_methods = ('GET',)    
    
    def read(self, request, urn=None):
        if urn:
            try:
                link = Link.objects.get(unis_id=urn)
                resp = link_dict(link)
                return resp
                
            except Node.DoesNotExist:
                resp = rc.NOT_HERE
                return resp
        else:
            links = Link.objects.all()
            resp = []
            for l in links:
                resp.append(link_dict(l))
            return resp

class EndPointPairUNISHandler(BaseHandler):
    allowed_methods = ('GET',)
    
    def read(self, request, urn=None):
        if urn:
            try:
                endpoint = EndPointPair.objects.get(unis_id=urn)
                resp = endpointpair_dict(endpoint)
                return resp
            except EndPointPair.DoesNotExist:
                resp = rc.NOT_HERE
                return resp
        else:
            endpoints = EndPointPair.objects.all()
            resp = []
            for e in endpoints:
                resp.append(endpointpair_dict(e))
            return resp

class PathUNISHandler(BaseHandler):
    allowed_methods = ('GET',)    
    
    def read(self, request, urn=None):
        if urn:
            try:
                path = Path.objects.get(unis_id=urn)
                resp = path_dict(path)
                return resp
                
            except Node.DoesNotExist:
                resp = rc.NOT_HERE
                return resp
        else:
            paths = Path.objects.all()
            resp = []
            for p in paths:
                resp.append(path_dict(p))
            return resp     
