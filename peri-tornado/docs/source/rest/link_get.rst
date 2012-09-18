.. _link_get:

Get Link
============

Returns the specified :ref:`Link <link_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/links/{id}

where `id` is the Link's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`Link <link_schema>`
can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.

Query on a single Link is executed over the current and the older versions of 
the Link's representation. The returned result when query is used is a 
list of Links.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Link representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Link.
* **404 Not found** No Link with the specified `id` exists.
* **500 Internal Server Error** Link couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Link representation <link_schema>` is returned.
If query is used the returned result is list of 
:ref:`Links representations <link_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Link
~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/links/link1
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/link#

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
    }


