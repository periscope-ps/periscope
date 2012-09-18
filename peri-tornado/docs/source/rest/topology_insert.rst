.. _topology_insert:

Insert Topology
=================

Creates a new :ref:`Topology(s) <topology_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/topologies


Request Body
~~~~~~~~~~~~~

:ref:`Topology <topology_schema>` representation or list of
:ref:`Topology <topology_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Topology(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Topology(s).
* **409 Conflict** The Topology(s) already inserted before.
* **500 Internal Server Error** Topology(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Topology submitted: The new :ref:`Topology representation <topology_schema>`
and `Location` HTTP header of that Topology.

If list of Topologies submitted: List of :ref:`Topology <topology_schema>` created.


Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Topology
~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /topologies HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/topology#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
        "id": "1",
        "domains": [
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/domain#",
                "id": "1",
                "nodes": [
                    {
                        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                        "name": "node1",
                        "urn": "urn:ogf:network:domain=example.com:node=node1",
                        "description": "This node uses JSONPath to its ports",
                        "ports": [
                            {
                                "href": "$..[?(@.name=='port1')]",
                                "rel": "full"
                            },
                            {
                                "href": "$..[?(@.urn=='urn:ogf:network:domain=example.com:port=port2')]",
                                "rel": "full"
                            }
                        ]
                    },
                    {
                        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                        "name": "node2",
                        "urn": "urn:ogf:network:domain=example.com:node=node2",
                        "description": "This node uses JSONPointer to its ports",
                        "ports": [
                            {
                                "href": "#/domains/0/ports/2",
                                "rel": "full"
                            }
                        ]
                    }
                ],
                "ports": [
                    {
                        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                        "name": "port1",
                        "urn": "urn:ogf:network:domain=example.com:port=port1",
                        "capacity": 1000
                    },
                    {
                        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                        "name": "port2",
                        "urn": "urn:ogf:network:domain=example.com:port=port2",
                        "capacity": 10000000
                    },
                    {
                        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                        "name": "port3",
                        "urn": "urn:ogf:network:domain=example.com:port=port3",
                        "capacity": 10000000000
                    }
                ]
            }
        ]
    }

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/topology#
    Location: https://example.com/topologies/1
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
        "id": "1",
        "selfRef": "https://example.com/topologies/1",
        "ts": 1338579183933748,
        "domains": [
            {
                "href": "https://example.com/domains/1",
                "rel": "full
            }
        ]
    }
