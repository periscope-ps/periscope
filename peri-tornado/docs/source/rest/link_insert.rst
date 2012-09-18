.. _link_insert:

Insert Link
=================

Creates a new :ref:`Link(s) <link_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/links


Request Body
~~~~~~~~~~~~

:ref:`Link <link_schema>` representation or list of
:ref:`Links <link_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Link(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Link(s).
* **409 Conflict** The Link(s) already inserted before.
* **500 Internal Server Error** Link(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Link submitted: The new :ref:`Link representation <link_schema>`
and `Location` HTTP header of that Link.

If list of Links submitted: List of :ref:`Links <link_schema>` created.

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Link
~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /links HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/link#
    Content-Length: 248
    
    {
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


**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/link#
    Location: https://example.com/links/link1
    
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

