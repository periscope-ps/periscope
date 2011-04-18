from django.conf import settings
from periscope.topology.models import *
from periscope.topology.lib.topology import create_from_xml_file
from periscope.topology.lib.util import save_parsed_elements

t = create_from_xml_file(settings.PERISCOPE_ROOT + "examples/terapaths-unis-2.xml")
save_parsed_elements(t[0])

PeriscopeDomainProperties.objects.all().delete()
PeriscopeNodeProperties.objects.all().delete()
PeriscopePortProperties.objects.all().delete()

d = Domain.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov')
PeriscopeDomainProperties.objects.create(parent=d, 
    shape=PeriscopeShape.objects.create(
    shape="rect", x=10, y=10, width=425, height=350, fill="moccasin",
    text_xdisp="10", text_ydisp="20", text_align="left"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=amon')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=430, y=170, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=amon:port=te1/1')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=400, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=170, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=Port-channel5')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=270, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=TenGigabitEthernet9/1')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=330, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=TenGigabitEthernet9/4')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=200, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=unrouted-VLAN-3561')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=140, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=unrouted-VLAN-3562')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=285, y=195, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr1:port=unrouted-VLAN-3563')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=315, y=195, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=ex2500')
PeriscopeNodeProperties.objects.create(parent=n,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=300, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=ex2500:port=port1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=300, y=270, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=ex2500:port=port2')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=272, y=290, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=ex2500:port=port3')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=272, y=310, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=180, y=170, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2:port=Port-channel5')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=210, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2:port=GigabitEthernet9/23')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=155, y=185, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2:port=GigabitEthernet9/37')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=155, y=155, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2:port=GigabitEthernet9/24')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=166, y=196, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=qtr2:port=GigabitEthernet9/25')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=180, y=199, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos01')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=60, y=90, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos01:port=eth0')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=85, y=104, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos03')
PeriscopeNodeProperties.objects.create(parent=n,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=60, y=250, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos03:port=eth0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=85, y=233, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos03:port=eth1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=89, y=260, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos04')
PeriscopeNodeProperties.objects.create(parent=n,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=120, y=320, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos04:port=eth0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=127, y=292, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos04:port=eth1')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=147, y=332, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos02')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=60, y=170, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.bnl.gov:node=netqos02:port=eth2')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=85, y=185, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

d = Domain.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org')
PeriscopeDomainProperties.objects.create(parent=d, 
    shape=PeriscopeShape.objects.create(
    shape="rect", x=800, y=80, width=200, height=270, fill="palegreen",
    text_xdisp="10", text_ydisp="20", text_align="left"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=810, y=170, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=TenGigabitEthernet7/4')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=835, y=153, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=TenGigabitEthernet2/2')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=840, y=170, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=TenGigabitEthernet2/3')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=836, y=184, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=unrouted-VLAN-3561')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=810, y=140, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=unrouted-VLAN-3562')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=795, y=195, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=nile:port=unrouted-VLAN-3563')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=825, y=195, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera03')
PeriscopeNodeProperties.objects.create(parent=n, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=940, y=135, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera03:port=eth0')
PeriscopePortProperties.objects.create(parent=p, 
    shape=PeriscopeShape.objects.create(
    shape="circle", x=910, y=140, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera04')
PeriscopeNodeProperties.objects.create(parent=n,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=940, y=220, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera04:port=eth0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=915, y=203, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

n = Node.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera05')
PeriscopeNodeProperties.objects.create(parent=n,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=910, y=300, width=30, height=30, fill="lightcyan",
    text_xdisp="0", text_ydisp="0", text_align="middle"
))

p = Port.objects.get(unis_id='urn:ogf:network:domain=escps.ultralight.org:node=tera05:port=eth0')
PeriscopePortProperties.objects.create(parent=p,
    shape=PeriscopeShape.objects.create(
    shape="circle", x=890, y=278, width=5, height=5, fill="aliceblue",
    text_xdisp="-10", text_ydisp="-10", text_align="middle"
))

