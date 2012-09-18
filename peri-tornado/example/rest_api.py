#!/usr/bin/env python

"""
Small Examples about using the REST API
"""

import json
import time
import urllib
from httplib import HTTPConnection

HOST = "monitor.damslab.org"
PORT =  8888
URL = "http://%s:%s" % (HOST, PORT)

MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSXML': 'application/perfsonar+xml',
}

SCHEMAS = {
    'networkresource': 'http://monitor.damslab.org/unis/networkresource#',
    'node': 'http://monitor.damslab.org/unis/node#',
    'port': 'http://monitor.damslab.org/unis/port#',
    'link': 'http://monitor.damslab.org/unis/link#',
    'network': 'http://monitor.damslab.org/unis/network#',
    'blipp': 'http://monitor.damslab.org/unis/blipp#',
    'metadata': 'http://monitor.damslab.org/unis/metadata#',
}


node = {
    "id": "pc166",
    "addresses": {
        "dns": [
            "pc166.emulab.net",
            "node1.josecuervo.emulab-net.emulab.net"
        ]
    },
    "ports": [
        {
            "href": URL + "/ports/pc166_iface0",
            "rel": "instance"
        }
    ],
    "properties": {
        "pgeni": {
            "component_manager_urn": "urn:publicid:IDN+emulab.net+authority+cm",
            "component_manager_uuid": "28a10955-aa00-11dd-ad1f-001143e453fe",
            "component_urn": "urn:publicid:IDN+emulab.net+node+pc166",
            "component_uuid": "de99509e-773e-102b-8eb4-001143e453fe",
            "exclusive": True,
            "sliver_urn": "urn:publicid:IDN+emulab.net+sliver+72500",
            "sliver_uuid": "395c22c4-4d1a-11e1-a511-001143e453fe",
            "virtualization_subtype": "raw",
            "virtualization_type": "raw",
            "node_type": "pc",
            "disk_image": "urn:publicid:IDN+emulab.net+image+GeniSlices//UBUNTU91-LAMP"
        }
    }
}


port = {
    "id": "pc166_iface0",
    "names": {
        "ifname": [
            "eth27"
        ]
    },
    "addresses": {
        "mac": [
            "0002b365b8c9"
        ],
        "ipv4": [
            "10.10.1.1"
        ]
    },
    "properties": {
        "pgeni": {
            "component_id": "eth3",
            "component_urn": "urn:publicid:IDN+emulab.net+interface+pc166:eth3",
            "sliver_urn": "urn:publicid:IDN+emulab.net+sliver+72504",
            "sliver_uuid": "3c9b1bbb-4d1a-11e1-a511-001143e453fe"
        }
    }
}

meta1 = {
    "id": "meta1",
    "subject": {"href": URL + "/ports/pc166_iface0"},
    "eventTypes": ["ps.port.util"]
}

meta2 = {
    "id": "meta1",
    "subject": {"href": URL + "/ports/pc166_iface0"},
    "eventTypes": ["ps.port.discard"]
}

meta3 = {
    "id": "meta3",
    "subject": {"href": URL + "/ports/pc166_iface0"},
    "eventTypes": ["ps.port.error"]
}

meta4 = {
    "id": "meta4",
    "subject": {"href": URL + "/metadata/meta1"},
    "eventTypes": ["ps.port.util.avg"]
}


# POST and let the server handle the IDs
# Note node has ID in the body, so Periscope is going to use it
# Howeever if there is no ID the server will generate one
conn = HTTPConnection(HOST, PORT)
headers = {
        "Accept": MIME["PSJSON"],
        "Content-Type": MIME["PSJSON"] + "; profile="+ SCHEMAS["node"]
    }
conn.request("POST", "/nodes", json.dumps(node), headers)
res = conn.getresponse()
# This should be 202
print res.status


# Conflict
conn = HTTPConnection(HOST, PORT)
headers = {
        "Accept": MIME["PSJSON"],
        "Content-Type": MIME["PSJSON"] + "; profile="+ SCHEMAS["node"]
    }
conn.request("POST", "/nodes", json.dumps(node), headers)
res = conn.getresponse()
# This should be 409
print res.status



# PUT
conn = HTTPConnection(HOST, PORT)
headers = {
        "Accept": MIME["PSJSON"],
        "Content-Type": MIME["PSJSON"] + "; profile="+ SCHEMAS["port"]
    }
conn.request("PUT", "/ports/pc166_iface0" , json.dumps(port), headers)
res = conn.getresponse()
# This should be 201
print res.status



# POST Multiple Metadata at once
conn = HTTPConnection(HOST, PORT)
headers = {
        "Accept": MIME["PSJSON"],
        "Content-Type": MIME["PSJSON"] + "; profile="+ SCHEMAS["metadata"]
    }
conn.request("POST", "/metadata", json.dumps([meta1, meta2, meta3, meta4]), headers)
res = conn.getresponse()
# This should be 202
print res.status


# Sending Blipp
probs = []
for i in range(1000):
    ts = time.time() * 1000000
    probs.append({"mid": "meta1", "ts": ts, "v": ts * 5})
    probs.append({"mid": "meta2", "ts": ts, "v": ts * 5})
    probs.append({"mid": "meta3", "ts": ts, "v": ts * 5})
    probs.append({"mid": "meta4", "ts": ts, "v": ts * 5})

conn = HTTPConnection(HOST, PORT)
headers = {
        "Accept": MIME["PSJSON"],
        "Content-Type": MIME["PSJSON"] + "; profile="+ SCHEMAS["blipp"]
    }
conn.request("POST", "/events", json.dumps(probs), headers)
res = conn.getresponse()
# This should be 202
print res.status

