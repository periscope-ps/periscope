#!/usr/bin/env python

import time
from urlparse import urlparse
from datetime import datetime

from lxml import etree,objectify

from periscope.measurements.lib.SimpleClient import SimpleClient


NMWG="http://ggf.org/ns/nmwg/base/2.0/"
TRACEROUTE="http://ggf.org/ns/nmwg/tools/traceroute/2.0"
NMWGT="http://ggf.org/ns/nmwg/topology/2.0/"

def make_traceroute_msg(src, dst):
    msg = """
<nmwg:message id="SetupDataRequest1" type="SetupDataRequest" 
xmlns:nmwg="http://ggf.org/ns/nmwg/base/2.0/" 
xmlns:nmwgt="http://ggf.org/ns/nmwg/topology/2.0/" 
xmlns:traceroute="http://ggf.org/ns/nmwg/tools/traceroute/2.0/">

    <nmwg:metadata id="traceroutemeta1">
        <traceroute:subject id="tracesub1">
            <nmwgt:endPointPair>
                <nmwgt:src value="%s"/>
                <nmwgt:dst value="%s"/>
            </nmwgt:endPointPair>
        </traceroute:subject>
        <nmwg:eventType>http://ggf.org/ns/nmwg/tools/traceroute/2.0/</nmwg:eventType>
    </nmwg:metadata>
    <nmwg:data id="data2" metadataIdRef="traceroutemeta1"/>
</nmwg:message>
""" % (src, dst)
    return msg

def parse_traceroute_response(result):
    root = etree.fromstring(result)
    endpoint = root.find(".//{%s}endPointPair" % NMWGT)
    
    if endpoint is None:
        return None
    meta = endpoint.getparent().getparent()
    metaid = meta.get('id')
    data = root.find('.//{%s}data[@metadataIdRef="%s"]' % (NMWG, metaid))
    
    if data is None:
         return
    
    datum = data.findall('.//{%s}datum[@queryNum="1"]' % TRACEROUTE)
    
    hops = {}
    for d in datum:
        hops[int(d.get('ttl'))] = d.get('hop')
        
    keys = hops.keys()
    keys.sort()
    ret = []
    for k in keys:
        ret.append(hops[k])
    
    return ret


def query_traceroute(accessPoint, src, dst):
    url_parse = urlparse(accessPoint)
    client = SimpleClient(host=url_parse.hostname, port=url_parse.port, uri=url_parse.path)
    query = make_traceroute_msg(src, dst)
    response = client.send_request(query)
    return parse_traceroute_response(response)

