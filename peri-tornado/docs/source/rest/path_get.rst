.. _path_get:

Get Path
=========

Returns the specified :ref:`Path representation <path_schema>`.

Request
--------

HTTP Request::
    
    GET http://examples.com/paths/{id}

where `id` is the Paths's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`Paths <path_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.

Query on a single Path is executed over the current and the older versions of 
the Path's representation. The returned result when query is used is a 
list of Paths.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Path representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Path.
* **404 Not found** No Path with the specified `id` exists.
* **500 Internal Server Error** Path couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Path representation <path_schema>` is returned.
If query is used the returned result is list of 
:ref:`Paths representation <path_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Path
~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/paths/4fb18fddf473533226000000
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/path#

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
        "id": "4fb18fddf473533226000000",
        "ts": 1337036765364994,
        "selfRef": "https://example.com/paths/4fb18fddf473533226000000",
        "urn": "urn:ogf:network:domain=example.com:path=path1",
        "description": "This is a sample path",
        "name": "path1",
        "directed": true,
        "hops": [
            {
                "href": "https://example.com/ports/1",
                "rel": "full"
            },
            {
                "href": "https://example.com/nodes/1",
                "rel": "full"
            },
            {
                "href": "https://example.com/ports/2",
                "rel": "full"
            },
            {
                "href": "https://example.com/nodes/2",
                "rel": "full"
            },
            {
                "href": "https://example.com/ports/3",
                "rel": "full"
            }
        ]
    }
