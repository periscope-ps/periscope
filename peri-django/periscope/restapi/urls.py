from django.conf.urls.defaults import *
from piston.resource import Resource


from periscope.restapi.UNISHandlers import UNISHandler, NodeUNISHandler, \
    PortUNISHandler, LinkUNISHandler, EndPointPairUNISHandler, PathUNISHandler

unis = Resource(handler=UNISHandler)
unis_node = Resource(handler=NodeUNISHandler)
unis_port = Resource(handler=PortUNISHandler)
unis_link = Resource(handler=LinkUNISHandler)
unis_endpoint = Resource(handler=EndPointPairUNISHandler)
unis_path = Resource(handler=PathUNISHandler)

urlpatterns = patterns('',
    url(r'^network/unis/$', unis),
    url(r'^network/unis/node/$', unis_node, { 'emitter_format': 'json' }),
    url(r'^network/unis/node/(?P<urn>[^/]+)/', unis_node, { 'emitter_format': 'json' }),
    url(r'^network/unis/port/$', unis_port, { 'emitter_format': 'json' }),
    url(r'^network/unis/port/(?P<urn>[^/]+)/', unis_port, { 'emitter_format': 'json' }),
    url(r'^network/unis/endpoint/$', unis_endpoint, { 'emitter_format': 'json' }),
    url(r'^network/unis/endpoint/(?P<urn>[^/]+)/', unis_endpoint, { 'emitter_format': 'json' }),
    url(r'^network/unis/link/$', unis_link, { 'emitter_format': 'json' }),
    url(r'^network/unis/link/(?P<urn>[^/]+)/', unis_link, { 'emitter_format': 'json' }),
    url(r'^network/unis/path/$', unis_path, { 'emitter_format': 'json' }),
    url(r'^network/unis/path/(?P<urn>[^/]+)/', unis_path, { 'emitter_format': 'json' }),
    url(r'^network/unis/(?P<urn>[^/]+)/', unis, { 'emitter_format': 'xml' }),
    
)
