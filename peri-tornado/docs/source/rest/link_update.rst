.. _link_update:

Update Link
================

Updates the specified Link with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/links/{id}

where `id` is the Link's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Link <link_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Link was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Link.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Link couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Link representation <link_schema>` and 
`Location` HTTP header of that Link.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Link
~~~~~~~~~~~~~~~~~~~


**Request**::

    PUT /links/link1 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/link#
    Content-Length: 248
    
    {
        "directed": true,
        "capacity": 10000000000,
        "endpoints": {
            "source": {
                "href": "https://example.com/ports/5",
                "ref": "full"
            },
            "sink": {
                "href": "https://example.com/ports/6",
                "ref": "full"
            }
        }
    }

**Response**

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/link#
    Location: /links/link1
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/link#",
        "id": "link1",
        "selfRef": "https://example.com/links/link1"
        "ts": 1337200240812328, 
        "directed": true,
        "capacity": 10000000000,
        "endpoints": {
            "source": {
                "href": "https://example.com/ports/5",
                "ref": "full"
            },
            "sink": {
                "href": "https://example.com/ports/6",
                "ref": "full"
            }
        }
    }

    
