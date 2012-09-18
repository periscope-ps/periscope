.. _network_insert:

Insert Network
=================

Creates a new :ref:`Network(s) <network_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/networks


Request Body
~~~~~~~~~~~~~

:ref:`Network <network_schema>` representation or list of
:ref:`Network <network_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Network(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Network(s).
* **409 Conflict** The Network(s) already inserted before.
* **500 Internal Server Error** Network(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Network submitted: The new :ref:`Network representation <network_schema>`
and `Location` HTTP header of that Network.

If list of Networks submitted: List of :ref:`Network <network_schema>` created.



Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Network
~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /networks HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/network#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/network#",
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
                        "href": "#/ports/2",
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

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/network#
    Location: https://example.com/networks/1
    
    {
        "id": "1",
        "ts": 1338494769852401,
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/network#",
        "selfRef": "https://example.com/networks/1",
        "ports": [
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000002",
                "rel": "full"
            },
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000003",
                "rel": "full"
            },
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000004",
                "rel": "full"
            }
        ],
        "nodes": [
            {
                "href": "https://example.com/nodes/4fc7cf319baf8a3c84000000",
                "rel": "full"
            },
            {
                "href": "https://example.com/nodes/4fc7cf319baf8a3c84000001",
                "rel": "full"
            }
        ]
    }
