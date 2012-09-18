.. _topology_get:

Get Topology
============

Returns the specified :ref:`Topology <topology_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/topologies/{id}

where `id` is the Topology's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Topology <topology_schema>` can be queried by the mechanisms defined
in :ref:`UNIS query language <query_ref>`.

Query on a single Topology is executed over the current and the older
versions of the Topology's representation. The returned result when
query is used is a list of Topologies.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Topology representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Topology.
* **404 Not found** No Topology with the specified `id` exists.
* **500 Internal Server Error** Topology couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Topology representation <topology_schema>` is returned.
If query is used the returned result is list of 
:ref:`Topologies representations <topology_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Topology
~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/topologies/1
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/topology#

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


