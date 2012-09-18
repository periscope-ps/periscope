.. _node_get:

Get Node
=========

Returns the specified :ref:`node <node_schema>`.

Request
--------

HTTP Request::
    
    GET http://examples.com/nodes/{id}

where `id` is the node's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`nodes <node_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.

Query on a single node is executed over the current and the older versions of 
the node's representation. The returned result when query is used is a 
list of Nodes.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A node representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the node.
* **404 Not found** No node with the specified `id` exists.
* **500 Internal Server Error** Node(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`node representation <node_schema>` is returned.
If query is used the returned result is list of 
:ref:`Nodes representation <node_schema>`.



Examples
--------

The examples include only important HTTP header fields for clarity.

Get Node
~~~~~~~~~

**Request**::
    
    GET https://example.com/nodes/1
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/node#

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "id": "1",
        "name": "node1",
        "selfRef": "https://example.com/nodes/1",
        "urn": "urn:urn1",
        "ts": 1336706645889028
    }


Get the a representation with specific timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/nodes/1?ts=1336866031650383
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/node#
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "id": "1",
        "name": "node1",
        "selfRef": "https://example.com/nodes/1",
        "urn": "urn:urn1",
        "ts": 1336866031650383
    }
