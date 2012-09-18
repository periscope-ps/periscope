.. _path_list:

List/Query Paths
=================

Return all :ref:`Paths <path_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/paths

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`Paths <path_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Oaths is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Path(s).
* **500 Internal Server Error** Path(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Paths <path_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all Paths
~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/paths
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/path#
    
    [
        {
            "id": "4fb1927ff473533226000006",
            "description": "This is a sample path",
            "directed": true,
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
            "name": "path1",
            "selfRef": "https://example.com/paths/4fb1927ff473533226000006",
            "urn": "urn:ogf:network:domain=example.com:path=path1",
            "ts": 1337037439424815,
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
            "id": "4fb1927ff473533226000007",
            "selfRef": "https://example.com/paths/4fb1927ff473533226000007",
            "urn": "urn:ogf:network:domain=example.com:path=path2",
            "ts": 1337037439425199,
            "directed": true,            
            "name": "path2",
            "description": "This is a sample path",
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
