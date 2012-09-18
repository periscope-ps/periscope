.. _port_list:

List/Query Ports
=================

Return all :ref:`ports <port_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/ports

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`ports <port_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of ports is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read port(s).
* **500 Internal Server Error** Post(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`ports <port_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all ports
~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/ports
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/port#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "id": "1",
            "name": "port1",
            "selfRef": "https://example.com/ports/1",
            "urn": "urn:urn1",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "id": "2",
            "name": "port2",
            "selfRef": "https://example.com/ports/2",
            "urn": "urn:urn2",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "id": "3",
            "name": "port3",
            "selfRef": "https://example.com/ports/3",
            "urn": "urn:urn3",
            "ts": 1336706645889028
        }
    ]


List ports with specific URNs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/ports?urn=urn:urn1,urn:urn2
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/port#
    
    [
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "id": "1",
            "name": "port1",
            "selfRef": "https://example.com/ports/1",
            "urn": "urn:urn1",
            "ts": 1336706645889028
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "id": "2",
            "name": "port2",
            "selfRef": "https://example.com/ports/2",
            "urn": "urn:urn2",
            "ts": 1336706645889028
        }
    ]
