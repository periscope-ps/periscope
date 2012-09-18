.. _domain_list:

List/Query Domains
===================

Return all :ref:`Domains <domain_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/domains

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Domains <domain_schema>` can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Domains is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Domains.
* **500 Internal Server Error** Domain(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Domain <domain_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all Domains
~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/domains
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/domain#
    
    [
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
    ]
