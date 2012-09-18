.. _metadata_list:

List/Query Metadata
====================

Return all :ref:`metadata <metadata_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/metadata

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, 
:ref:`metadata <metadata_schema>` can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of metadata is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read metadata.
* **500 Internal Server Error** Metadata couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`metadata <metadata_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

Query Metadata by subject and event type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/metadata?subject.href=https://example.com/ports/1&eventType=event_x
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/metadata#
    
    [
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
    ]
