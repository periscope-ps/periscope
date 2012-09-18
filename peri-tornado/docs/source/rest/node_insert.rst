.. _node_insert:

Insert Node
============

Creates a new :ref:`node(s) <node_schema>`.

Request
--------

HTTP Request::
    
    POST http://examples.com/nodes


Request Body
~~~~~~~~~~~~

:ref:`Node <node_schema>` representation or list of :ref:`nodes <node_schema>`
representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The node(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new node(s).
* **409 Conflict** The node(s) already inserted before.
* **500 Internal Server Error** Node(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one node submitted: The new :ref:`node representation <node_schema>` and 
`Location` HTTP header of that node.

If list of nodes submitted: List of :ref:`nodes <node_schema>` created

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Node
~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /nodes HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "name": "node1",
        "urn": "urn:ogf:network:domain=example.com:node=node1",
        "description": "This is a sample node",
        "location": {
            "institution": "Indiana University"
        }
    }

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Location: https://example.com/nodes/4faed227f473534b88000000
    
    {
        "id": "4faeed0cf4735352b700000f", 
        "ts": 1336864012847944, 
        "selfRef": "https://example.com/nodes/4faeed0cf4735352b700000f", 
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "name": "node1",
        "urn": "urn:ogf:network:domain=example.com:node=node1", 
        "description": "This is a sample node", 
        "location": {
            "institution": "Indiana University", 
        }
    }
    

Insert list of Nodes
~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /nodes HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Content-Length: 248
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node1",
            "urn": "urn:ogf:network:domain=example.com:node=node1",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node2",
            "urn": "urn:ogf:network:domain=example.com:node=node2",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node3",
            "urn": "urn:ogf:network:domain=example.com:node=node3",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node4",
            "urn": "urn:ogf:network:domain=example.com:node=node4",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        }
    ]


**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.
`Location` HTTP header is not returned for the list of the nodes.::


    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    
    [
        {
            
            "id": "4faef1f9f4735353e3000000",
            "ts": 1336865273329438,
            "selfRef": "https://example.com/nodes/4faef1f9f4735353e3000000",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node1",
            "urn": "urn:ogf:network:domain=example.com:node=node1",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            
            "id": "4faef1f9f4735353e3000001",
            "ts": 1336865273329438,
            "selfRef": "https://example.com/nodes/4faef1f9f4735353e3000001",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node2",
            "urn": "urn:ogf:network:domain=example.com:node=node2",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            
            "id": "4faef1f9f4735353e3000002",
            "ts": 1336865273329438,
            "selfRef": "https://example.com/nodes/4faef1f9f4735353e3000002",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node3",
            "urn": "urn:ogf:network:domain=example.com:node=node3",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            
            "id": "4faef1f9f4735353e3000003",
            "ts": 1336865273329438,
            "selfRef": "https://example.com/nodes/4faef1f9f4735353e3000003",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "name": "node4",
            "urn": "urn:ogf:network:domain=example.com:node=node4",
            "description": "This is a sample node",
            "location": {
                "institution": "Indiana University"
            }
        }
    ]
