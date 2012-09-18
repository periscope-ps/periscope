.. _metadata_get:

Get Metadata
================

Returns the specified :ref:`Metadata <metadata_schema>`.

Request
--------

HTTP Request::
    
    GET http://examples.com/metadata/{id}

where `id` is the Metadata's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Metadata <metadata_schema>` can be queried by the mechanisms defined
in :ref:`UNIS query language <query_ref>`.

Query on a single Metadata is executed over the current and the older versions
of the Metadata's representation. The returned result when query is used is a 
list of Metadata.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Metadata representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Metadata.
* **404 Not found** No Metadata with the specified `id` exists.
* **500 Internal Server Error** Metadata couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Metadata representation <metadata_schema>` is returned.
If query is used the returned result is list of 
:ref:`Metadata representation <Metadata_schema>`.



Examples
--------

The examples include only important HTTP header fields for clarity.

Get Metadata
~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/metadata/4fb2b024f473535056000000
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/Metadata#

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
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#"
        }
    }

