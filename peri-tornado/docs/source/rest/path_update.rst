.. _path_update:

Update Path
===========

Updates the specified Path with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/paths/{id}

where `id` is the path's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Path <path_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Path was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Path.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Path couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`path representation <path_schema>` and 
`Location` HTTP header of that Path.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Path
~~~~~~~~~~~~~~~~


**Request**::

    PUT /paths/4fb18fddf473533226000000 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/path#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
        "urn": "urn:ogf:network:domain=example.com:path=path1",
        "description": "This is a sample UPDATED path",
        "name": "path1",
        "directed": true,
        "hops": [
            {
                "href": "https://example.com/ports/new_port",
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

**Response**

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/node#
    Location: https://example.com/paths/4fb18fddf473533226000000
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
        "id": "4fb18fddf473533226000000",
        "ts": 1337036765364994,
        "selfRef": "https://example.com/paths/4fb18fddf473533226000000",
        "urn": "urn:ogf:network:domain=example.com:path=path1",
        "description": "This is a sample UPDATED path",
        "name": "path1",
        "directed": true,
        "hops": [
            {
                "href": "https://example.com/ports/new_port",
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
    
