.. _network_get:

Get Network
============

Returns the specified :ref:`Network <network_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/networks/{id}

where `id` is the Network's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Network <network_schema>` can be queried by the mechanisms defined
in :ref:`UNIS query language <query_ref>`.

Query on a single Network is executed over the current and the older
versions of the Network's representation. The returned result when
query is used is a list of Networks.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Network representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Network.
* **404 Not found** No Network with the specified `id` exists.
* **500 Internal Server Error** Network couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Network representation <network_schema>` is returned.
If query is used the returned result is list of 
:ref:`Networks representations <network_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Network
~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/networks/1
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/network#

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


