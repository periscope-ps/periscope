.. _node_list:

List/Query Nodes
=================

Return all :ref:`nodes <node_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/nodes

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`nodes <node_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of nodes is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read node(s).
* **500 Internal Server Error** Node(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`nodes <node_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all nodes
~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/nodes
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/node#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "id": "1",
            "name": "node1",
            "selfRef": "https://example.com/nodes/1",
            "urn": "urn:urn1",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "id": "2",
            "name": "node2",
            "selfRef": "https://example.com/nodes/2",
            "urn": "urn:urn2",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "id": "3",
            "name": "node3",
            "selfRef": "https://example.com/nodes/3",
            "urn": "urn:urn3",
            "ts": 1336706645889028
        }
    ]


List nodes with specific URNs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/nodes?urn=urn:urn1,urn:urn2
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/node#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "id": "1",
            "name": "node1",
            "selfRef": "https://example.com/nodes/1",
            "urn": "urn:urn1",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
            "id": "2",
            "name": "node2",
            "selfRef": "https://example.com/nodes/2",
            "urn": "urn:urn2",
            "ts": 1336706645889028
        }
    ]
