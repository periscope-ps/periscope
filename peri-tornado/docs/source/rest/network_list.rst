.. _network_list:

List/Query Networks
====================

Return all :ref:`Networks <network_schema>` registered in the UNIS
instance.

Request
-------

HTTP Request::

    GET https://example.com/networks

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Networks <network_schema>` can be queried by the mechanisms
defined in :ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Networks is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Networks.
* **500 Internal Server Error** Network(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Network <network_schema>`
will be returned.


Examples
--------

The examples include only important HTTP header fields for clarity.

List all Networks
~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/networks
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/network#
    
    [
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
    ]
