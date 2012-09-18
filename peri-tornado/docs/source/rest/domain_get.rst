.. _domain_get:

Get Domain
============

Returns the specified :ref:`Domain <domain_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/domains/{id}

where `id` is the Domain's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`Domain <domain_schema>`
can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.

Query on a single Domain is executed over the current and the older versions of 
the Domain's representation. The returned result when query is used is a 
list of Domains.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Domain representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Domain.
* **404 Not found** No Domain with the specified `id` exists.
* **500 Internal Server Error** Domain couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Domain representation <domain_schema>` is returned.
If query is used the returned result is list of 
:ref:`Domains representations <domain_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Domain
~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/domains/1
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/domain#

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


