.. _metadata_update:

Update Metadata
================

Updates the specified Metadata with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/metadata/{id}

where `id` is the Metadata's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Metadata <metadata_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Metadata was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Metadata.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Metadata couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Metadata representation <Metadata_schema>` and 
`Location` HTTP header of that Metadata.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Metadata
~~~~~~~~~~~~~~~~~~~~


**Request**::

    PUT /metadata/4fb2b024f473535056000000 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/metadata#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/metadata#",
        "subject": {
            "href": "https://example.com/ports/1",
            "rel": "full"
        },
        "eventType": "event_x",
        "parameters": {
            "collectionInterval": 30000,
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#",
            "new_parameters": "new value"
        }
    }
    

**Response**

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/metadata#
    Location: https://example.com/metadata/4fb2b024f473535056000000
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/metadata#",
        "ts": 1337110564767952,
        "id": "4fb2b024f473535056000000",
        "selfRef": "https://example/com/metadata/4fb2b024f473535056000000",
        "subject": {
            "href": "https://example.com/ports/1",
            "rel": "full"
        },
        "eventType": "event_x",
        "parameters": {
            "collectionInterval": 30000,
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#",
            "new_parameters": "new value"
        }
    }
    
