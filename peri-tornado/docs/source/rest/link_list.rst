.. _link_list:

List/Query Links
===================

Return all :ref:`Links <link_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/links

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Links <link_schema>` can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Links is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Links.
* **500 Internal Server Error** Link(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Link <link_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all Links
~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/links
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/link#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/link#",
            "id": "link1",
            "selfRef": "https://example.com/links/link1"
            "ts": 1337711394175048, 
            "directed": true,
            "capacity": 10000000000,
            "endpoints": {
                "source": {
                    "href": "https://example.com/ports/1",
                    "ref": "full"
                },
                "sink": {
                    "href": "https://example.com/ports/2",
                    "ref": "full"
                }
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/link#",
            "id": "link2",
            "selfRef": "https://example.com/links/link2",
            "ts": 1337711394175048, 
            "directed": false,
            "capacity": 10000000000,
            "endpoints": [
                {
                    "href": "https://example.com/ports/3",
                    "ref": "full"
                },
                {
                    "href": "https://example.com/ports/4",
                    "ref": "full"
                }
            ]
        }
    ]
