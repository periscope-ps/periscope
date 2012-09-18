.. _domain_insert:

Insert Domain
=================

Creates a new :ref:`Domain(s) <domain_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/domains


Request Body
~~~~~~~~~~~~

:ref:`Domain <domain_schema>` representation or list of
:ref:`Domains <domain_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Domain(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Domain(s).
* **409 Conflict** The Domain(s) already inserted before.
* **500 Internal Server Error** Domain(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Domain submitted: The new :ref:`Domain representation <domain_schema>`
and `Location` HTTP header of that Domain.

If list of Domains submitted: List of :ref:`Domains <domain_schema>` created.



Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Domain
~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /domains HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/domain#
    Content-Length: 248
    
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
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/domain#
    Location: https://example.com/domains/1
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/domain#",
        "id": "1",
        "ts": 1337976574414305,
        "selfRef": "https://example.com/domains/1",
        "nodes": [
            {
                "href": "https://example.com/nodes/4fbfe6fe9baf8a3e39000000",
                "rel": "full
            },
            {
                "href": "https://example.com/nodes/4fbfe6fe9baf8a3e39000001",
                "rel": "full
            }
        ],
        "ports": [
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000002",
                "rel": "full
            },
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000003",
                "rel": "full
            },
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000004",
                "rel": "full
            }
        ]
    }
