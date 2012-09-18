.. _metadata_insert:

Insert Metadata
================

Creates a new :ref:`metadata <metadata_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/metadata


Request Body
~~~~~~~~~~~~

:ref:`Metadata <metadata_schema>` representation or list of 
:ref:`metadata <metadata_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The metadata was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new metadata.
* **409 Conflict** The metadata already inserted before.
* **500 Internal Server Error** Metadata couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one metadata submitted: The new 
:ref:`metadata representation <metadata_schema>` and `Location` HTTP header of
that metadata.

If list of metadata submitted: List of :ref:`metadata <metadata_schema>`
created.

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Metadata
~~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /metadata HTTP/1.1    
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
        "eventType": "some event type",
        "parameters": {
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#",
            "collectionInterval": 30000
        }
    }

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

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
        "eventType": "some event type",
        "parameters": {
            "collectionInterval": 30000,
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#"
        }
    }
