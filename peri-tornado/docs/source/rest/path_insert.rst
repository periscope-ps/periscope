.. _path_insert:

Insert Path
============

Creates a new :ref:`Paths(s) <path_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/paths


Request Body
~~~~~~~~~~~~

:ref:`Path <path_schema>` representation or list of :ref:`Paths <path_schema>`
representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The path(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Path(s).
* **409 Conflict** The Path(s) already inserted before.
* **500 Internal Server Error** Path(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Path submitted: The new :ref:`Path representation <path_schema>` and 
`Location` HTTP header of that Path.

If list of Paths submitted: List of :ref:`Paths <path_schema>` created

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Path
~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /paths HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/path#
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
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

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/path#
    Location: https://example.com/paths/4fb18fddf473533226000000
    
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
    

Insert list of Paths
~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /paths HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/path#
    Content-Length: 248
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
            "name": "path1",
            "urn": "urn:ogf:network:domain=example.com:path=path1",
            "description": "This is a sample path",
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
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
            "name": "path2",
            "urn": "urn:ogf:network:domain=example.com:path=path2",
            "description": "This is a sample path",
            "directed": true,
            "hops": [
                {
                    "href": "https://example.com/ports/5",
                    "rel": "full"
                },
                {
                    "href": "https://example.com/nodes/3",
                    "rel": "full"
                },
                {
                    "href": "https://example.com/ports/6",
                    "rel": "full"
                }
            ]
        },
        
    ]



**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.
`Location` HTTP header is not returned for the list of the Paths.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/path#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
            "id": "4fb19107f473533226000002",
            "description": "This is a sample path",
            "selfRef": "https://example.com/paths/4fb19107f473533226000002",
            "urn": "urn:ogf:network:domain=example.com:path=path1",
            "ts": 1337037063594031,
            "directed": true,
            "name": "path1",
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
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
            "id": "4fb19107f473533226000003",
            "selfRef": "https://example.com/paths/4fb19107f473533226000003",
            "urn": "urn:ogf:network:domain=example.com:path=path2",
            "ts": 1337037063594662,
            "description": "This is a sample path",
            "directed": true,
            "name": "path2",
            "hops": [
                {
                    "href": "https://example.com/ports/5",
                    "rel": "full"
                },
                {
                    "href": "https://example.com/nodes/3",
                    "rel": "full"
                },
                {
                    "href": "https://example.com/ports/6",
                    "rel": "full"
                }
            ]
        }
    ]
