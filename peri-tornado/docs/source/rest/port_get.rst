.. _port_get:

Get Port
=========

Returns the specified :ref:`port <port_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/ports/{id}

where `id` is the port's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`ports <port_schema>` can
be queried by the mechanisms defined in :ref:`UNIS query language <query_ref>`.

Query on a single port is executed over the current and the older versions of 
the port's representation. The returned result when query is used is a 
list of Ports.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A port representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the port.
* **404 Not found** No port with the specified `id` exists.
* **500 Internal Server Error** Port couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`port representation <port_schema>` is returned.
If query is used the returned result is list of 
:ref:`Ports representation <port_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Port
~~~~~~~~~

**Request**::
    
    GET https://example.com/ports/123
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/port#

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "id": "123",
        "selfRef": "https://example.com/ports/123",
        "ts": 1336775637000,
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is a sample port",
        "location": {
            "institution": "Indiana University"
        }
    }


Get the a representation with specific timestamp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/ports/1?ts=1336866031650383
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/port#
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "id": "123",
        "selfRef": "https://example.com/ports/123",
        "ts": 1336866031650383,
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is a sample port",
        "location": {
            "institution": "Indiana University"
        }
    }
