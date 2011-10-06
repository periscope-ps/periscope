#!/usr/bin/env python

""" Imports ANI Testbed XML unis topology to Django's model and generates
Periscope shape properties.
"""

import math

from django.conf import settings

from periscope.topology.models import *
from periscope.topology.lib.topology import create_from_xml_file
from periscope.topology.lib.util import save_parsed_elements


# Imports ANI's XML unis topology to Django's model
if Topology.objects.all().count() == 0:
    topo = create_from_xml_file(settings.PERISCOPE_ROOT + "examples/anitestbed.xml")
    save_parsed_elements(topo[0])


# Delete all previous shape properties
PeriscopeDomainProperties.objects.all().delete()
PeriscopeNodeProperties.objects.all().delete()
PeriscopePortProperties.objects.all().delete()

# newy-tb-rt-1
newy_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1')
PeriscopeNodeProperties.objects.create(parent=newy_node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=200, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/2/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=340, y=210, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-1/3/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=340, y=190, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=270, y=175, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=160, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/2')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=325, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=xe-0/0/3')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=260, y=200, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-rt-1:port=ge-1/0/1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=240, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# newy-diskpt-1

newy_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1')
PeriscopeNodeProperties.objects.create(parent=newy_node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=50, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth5')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=265, y=70, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=260, y=50, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth8')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=90, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth4')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=280, y=80, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-diskpt-1:port=eth9')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=320, y=80, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# newy-app
newy_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-app')
PeriscopeNodeProperties.objects.create(parent=newy_node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=350, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=265, y=330, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-app:port=eth2')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=310, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# newy-tb-of-1
newy_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1')
PeriscopeNodeProperties.objects.create(parent=newy_node, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=100, y=200, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Te0/25')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=125, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/8')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=100, y=160, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Te0/26')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=140, y=200, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=newy-tb-of-1:port=Gi0/6')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=135, y=220, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# bnl-tb-rt-2
bnl_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2')

PeriscopeNodeProperties.objects.create(parent=bnl_node,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=800, y=200, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=760, y=210, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-0/0/1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=760, y=190, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=800, y=160, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=ge-1/0/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=827, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/3/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=840, y=200, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-rt-2:port=xe-1/2/0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=800, y=240, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# bnl-diskpt-1
bnl_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1')

PeriscopeNodeProperties.objects.create(parent=bnl_node,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=1000, y=350, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth5')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=1000, y=310, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth4')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=965, y=330, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth8')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=960, y=350, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-1:port=eth10')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=965, y=370, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


# bnl-diskpt-2
bnl_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2')

PeriscopeNodeProperties.objects.create(parent=bnl_node,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=800, y=350, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth7')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=835, y=330, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth8')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=840, y=350, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth9')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=835, y=370, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-diskpt-2:port=eth4')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=800, y=310, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))


bnl_node = Node.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2')

PeriscopeNodeProperties.objects.create(parent=bnl_node,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=1000, y=200, width=40, height=40, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=Te0/25')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=960, y=200, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=testbed.es.net:node=bnl-tb-of-2:port=Te0/26')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=1000, y=240, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))
