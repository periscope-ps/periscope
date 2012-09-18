.. _node_update:

Update Node
===========

Updates the specified node with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/nodes/{id}

where `id` is the node's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Node <node_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The node was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Node.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Node couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`node representation <node_schema>` and 
`Location` HTTP header of that node.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Node
~~~~~~~~~~~~~~~~


**Request**::

    PUT /nodes/1 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "name": "node1",
        "urn": "urn:ogf:network:domain=example.com:node=node1",
        "description": "This node has been updated",
        "location": {
            "institution": "Indiana University"
        }
    }

**Response**

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Location: https://example.com/nodes/1
    
    {
        "id": "1", 
        "ts": 1336864012847944, 
        "selfRef": "https://example.com/nodes/4faeed0cf4735352b700000f", 
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "name": "node1",
        "urn": "urn:ogf:network:domain=example.com:node=node1", 
        "description": "This node has been updated", 
        "location": {
            "institution": "Indiana University", 
        }
    }
    
