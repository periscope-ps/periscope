.. _topology_list:

List/Query Topologies
=======================

Return all :ref:`Topologies <topology_schema>` registered in the UNIS
instance.

Request
-------

HTTP Request::

    GET https://example.com/topologies

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Topologies <topology_schema>` can be queried by the mechanisms
defined in :ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Topologies is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Topologies.
* **500 Internal Server Error** Topology(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Topology <topology_schema>`
will be returned.


Examples
--------

The examples include only important HTTP header fields for clarity.

List all Topologies
~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/topologies
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/topology#
    
    [
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
    ]
