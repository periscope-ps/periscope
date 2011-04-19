#!/usr/bin/env python

""" Collect all services related to ESnet
"""

from periscope.topology.models import *
from periscope.measurements.lib.CollectGLS import *
from periscope.measurements.lib.CollectHLS import *
from periscope.measurements.lib.CollectPSServices import *

# Step 1 delete all none esnet topology nodes
esNodes = []
domain = Domain.objects.all()
if domain.count() > 0:
    esNodes = domain[0].get_nodes()

for node in Node.objects.all():
    if node not in esNodes:
        node.delete()

for s in Service.objects.all():
    s.delete()

for e in EndPointPair.objects.all():
    e.delete()

# Step 2 Get root servers
populate_roots()


# Step 3 Find all hlses from esnet root servers
collector = HLSCollector()
services = Service.objects.filter(properties_bag__psserviceproperties__serviceType='gLS').filter(unis_id__contains='es.net')

for s in services:
    try:
        collector.populate_hlses(s)
    except Exception, ex:
        print s, ex

# Step 4 Find all esnet's hls 
services = Service.objects.filter(properties_bag__psserviceproperties__serviceType='hLS').filter(unis_id__contains='es.net')
    
collector = ServicesCollector()
for s in services:
    try:
        collector.populate_psservices(s)
    except Exception, ex:
        print s, ex
