#!/usr/bin/env python


import sys
import os

BASE_NAMESPACE = "http://ogf.org/schema/network/topology/unis/20100528/"

#tfile = "/home/ezra/repos/periscope/examples/manifest-auto.xml"

cert_file = "/usr/local/etc/protogeni/ssl/lampcert.pem"
key_file = "/usr/local/etc/protogeni/ssl/lampcert.pem"

host="unis.pg.damslab.org"
port=8012
uri="/perfSONAR_PS/services/unis"

sys.path.append('/home/ezra/repos')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from periscope.measurements.lib.SimpleClient import SimpleClient
from periscope.topology.lib.topology import create_from_xml_string
from periscope.topology.lib.util import save_parsed_elements, get_urn_value
from periscope.topology.models import PortAddresses
from periscope.measurements.models import UrnStub
from periscope.lamp.util import make_UNISQueryAll_message
    

def get_lamp_topology():
    
    # GFR: When using the lamp@slice certificate 
    #   there's no need for credential
    #
    #slice_cred = get_slice_cred(cred_file)
    #body = make_UNISQueryCred_message(slice_cred)
    
    # Note that UNIS will return only the slice view for the Query All
    body = make_UNISQueryAll_message()

    try:
        client = SimpleClient(host=host, port=port, uri=uri, cert=cert_file, key=key_file)
        response = client.send_request(body, useSSL=True)
    except:
        print "Error contacting UNIS"
        return
    
    print response

    #t = create_from_xml_file(tfile)
    t = create_from_xml_string(response)
    
    if not t:
        print "Could not parse any topologies"
        return

    save_parsed_elements(t[0])

    types = ['in', 'out', 'cpu', 'mem']
    slices = []
    for d in t[0].get_domains():
        id_fields = get_urn_value(d.unis_id, 'domain').split('+')
        if len(id_fields) == 3 and id_fields[1] == 'slice':
            slices.append(id_fields[2] + '@' + id_fields[0])

        for n in d.get_nodes():
            for p in n.get_ports():
                pa = PortAddresses.objects.filter(port__unis_id=p.unis_id, address__type='ipv4')
                #pn = NetworkObjectNames.objects.filter(networkobject=p)
                
                for type in types:
                    urn = UrnStub(urn=pa[0].address.value + '-' + type,
                                  ifName=get_urn_value(p.unis_id, 'port'),
                                  ifHost=get_urn_value(n.unis_id, 'node'),
                                  ifAddress=pa[0].address.value,
                                  type=type,
                                  source='MA')
                    urn.save()

    t[0].unis_id = "Topology for slice " + slices[0]
    t[0].save()
    
get_lamp_topology()
    

    
    
