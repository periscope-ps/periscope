from django.conf import settings
from periscope.topology.models import *
from periscope.topology.lib.topology import create_from_xml_file
from periscope.topology.lib.util import save_parsed_elements

try:
    topo = Topology.objects.get(unis_id='escps')
    topo.delete()
except:
    print "no existing escps topo"

t = create_from_xml_file(settings.PERISCOPE_ROOT + "examples/escps-unis.xml")
save_parsed_elements(t[0])

PeriscopeDomainProperties.objects.all().delete()
PeriscopeNodeProperties.objects.all().delete()
PeriscopePortProperties.objects.all().delete()

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
