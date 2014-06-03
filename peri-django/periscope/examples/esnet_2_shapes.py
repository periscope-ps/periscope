#!/usr/bin/env python

""" Imports ESnet's XML unis topology to Django's model and generates
Periscope shape properties.
"""

import math

from django.conf import settings

from periscope.topology.models import *
from periscope.topology.lib.topology import create_from_xml_file
from periscope.topology.lib.util import save_parsed_elements


# Imports ESnet's XML unis topology to Django's model
#topo = create_from_xml_file(settings.PERISCOPE_ROOT + "examples/esnet_topology_unis.xml")
#save_parsed_elements(topo[0])


# Delete all previous shape properties
PeriscopeDomainProperties.objects.all().delete()
PeriscopeNodeProperties.objects.all().delete()
PeriscopePortProperties.objects.all().delete()


# Give nodes x, y coordinates based on the geolocation
es_domain = Domain.objects.get(unis_id="urn:ogf:network:domain=ps.es.net")

nodes = list(es_domain.get_nodes())

def get_xy(location):
    lat = location.latitude
    lon = location.longitude
    
    x = (125 + float(lon)) * 21
    y = (50 - float(lat)) *  21
    return (x,y)


for node in nodes:
    coords = get_xy(node.location)
    x = coords[0]
    y = coords[1]
    
    nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
        shape=PeriscopeShape.objects.create(
        shape="circle", x=x, y=y, width=22, height=22, fill="blue",
        text_xdisp="0", text_ydisp="0", text_align="middle"
    ))
    
    nodeprop.save()


node = Node.objects.get(names__value='anl-mr2')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.y -= 80
shape.save()


node = Node.objects.get(names__value='star-cr1')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.y += 80
shape.save()


node = Node.objects.get(names__value='nersc-mr2')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.y += 100
shape.x += 50
shape.save()


node = Node.objects.get(names__value='snll-mr2')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.y -= 80
shape.save()

node = Node.objects.get(names__value='llnl-mr2')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.x -= 20
shape.save()

node = Node.objects.get(names__value='sunn-cr1')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.x += 60
shape.save()

node = Node.objects.get(names__value='snv-mr2')
shape = PeriscopeNodeProperties.objects.get(parent=node).shape
shape.y += 100
shape.x -= 20
shape.save()



# Set the properties of gridFTP cloud nodes
node = Node.objects.get(unis_id='urn:ogf:network:domain=anl.gov:node=anl')
nodes.append(node)
esNode = Node.objects.get(names__value='anl-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x - 70, y=esShape.y+60, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=nersc.gov:node=nersc')
nodes.append(node)
esNode = Node.objects.get(names__value='nersc-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+20, y=esShape.y+60, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=vpac.org:node=vpac')
nodes.append(node)
esNode = Node.objects.get(names__value='sunn-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+10, y=esShape.y-40, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=ci.uchicago.edu:node=uchicago')
nodes.append(node)
esNode = Node.objects.get(names__value='snll-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x, y=esShape.y-50, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=ncsa.illinois.edu:node=ncsa')
nodes.append(node)
esNode = Node.objects.get(names__value='anl-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x-60, y=esShape.y-30, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=iu.edu:node=iu')
nodes.append(node)
esNode = Node.objects.get(names__value='snll-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x, y=esShape.y-50, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=ucar.edu:node=ucar')
nodes.append(node)
esNode = Node.objects.get(names__value='denv-cr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x-100, y=esShape.y+100, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=tacc.utexas.edu:node=tacc')
nodes.append(node)
esNode = Node.objects.get(names__value='snll-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x, y=esShape.y-50, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=psc.edu:node=psc')
nodes.append(node)
esNode = Node.objects.get(names__value='bost-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x, y=esShape.y+60, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=purdue.edu:node=purdue')
nodes.append(node)
esNode = Node.objects.get(names__value='anl-mr2')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=ivec.org:node=ivec')
nodes.append(node)
esNode = Node.objects.get(names__value='pnwg-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=lbl.gov:node=lbl')
nodes.append(node)
esNode = Node.objects.get(names__value='pnwg-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=olemiss.edu:node=olemiss')
nodes.append(node)
esNode = Node.objects.get(names__value='chic-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=ornl.gov:node=ornl')
nodes.append(node)
esNode = Node.objects.get(names__value='nash-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x+60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=loni.org:node=loni')
nodes.append(node)
esNode = Node.objects.get(names__value='chic-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x-60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


node = Node.objects.get(unis_id='urn:ogf:network:domain=unh.edu:node=unh')
nodes.append(node)
esNode = Node.objects.get(names__value='bost-cr1')
esShape = PeriscopeNodeProperties.objects.get(parent=esNode).shape
nodeprop = PeriscopeNodeProperties.objects.create(parent=node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=esShape.x-60, y=esShape.y+20, width=22, height=22, fill="lightblue",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))
nodeprop.save()


# Set the location to only Ports of interest
paths = Path.objects.all()
for path in paths:
    hops = Hop.objects.filter(parent=path)
    for hop in hops:
        link = hop.target.toRealType()
        sport = link.get_source().toRealType()
        dport = link.get_sink().toRealType()
        snode = sport.parent.toRealType()
        dnode = dport.parent.toRealType()
        
        if snode not in nodes:
            continue
        if dnode not in nodes:
            continue
        # print "%s -> %s" %( sport, dport)
        snodeprops = PeriscopeNodeProperties.objects.get(parent=snode)
        dnodeprops = PeriscopeNodeProperties.objects.get(parent=dnode)
        x1 = snodeprops.shape.x
        y1 = snodeprops.shape.y
        
        x2 = dnodeprops.shape.x
        y2 = dnodeprops.shape.y
        
        if float(x2) - float(x1) == 0:
            dt1 = 0
        else:
            dt1 = (y2 - float(y1)) / (float(x2) - float(x1))
        angle1 = math.atan(dt1)
        
        if len(PeriscopePortProperties.objects.filter(parent=dport)) == 0:
            (px, py) = (x2+ 30 * math.cos(math.pi +  angle1), y2+ 30 * math.sin(math.pi + angle1))
            portprop = PeriscopePortProperties.objects.create(parent=dport,
                shape=PeriscopeShape.objects.create(
                shape="circle", x=px, y=py, width=5, height=5, fill="aliceblue",
                text_xdisp="-10", text_ydisp="-10", text_align="middle"
            ))
            portprop.save()
        
        if len(PeriscopePortProperties.objects.filter(parent=sport)) == 0:
            (px, py) = (x1+ 30 * math.cos(angle1), y1+ 30 * math.sin(angle1))
            portprop = PeriscopePortProperties.objects.create(parent=sport,
                shape=PeriscopeShape.objects.create(
                shape="circle", x=px, y=py, width=5, height=5, fill="aliceblue",
                text_xdisp="-10", text_ydisp="-10", text_align="middle"
            ))
            portprop.save()
