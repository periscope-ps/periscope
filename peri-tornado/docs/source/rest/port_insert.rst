.. _port_insert:

Insert Port
============

Creates a new :ref:`port(s) <port_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/ports


Request Body
~~~~~~~~~~~~

:ref:`Port <port_schema>` representation or list of :ref:`ports <port_schema>`
representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The port(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new port(s).
* **409 Conflict** The port(s) already inserted before.
* **500 Internal Server Error** Port(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one port submitted: The new :ref:`port representation <port_schema>` and 
`Location` HTTP header of that port.

If list of ports submitted: List of :ref:`ports <port_schema>` created

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Port
~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /ports HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is a sample port",
        "location": {
            "institution": "Indiana University"
        }
    }

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    Location: https://example.com/ports/4fb04b3af473530a0f000000
    
    {
        "id": "4fb04b3af473530a0f000000", 
        "ts": 1336864012847944, 
        "selfRef": "https://example.com/ports/4fb04b3af473530a0f000000", 
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is a sample port",
        "location": {
            "institution": "Indiana University"
        }
    }
    

Insert list of Ports
~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /ports HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    Content-Length: 248
    
    [
        {
            "id": "4fb04b3af473530a0f000000", 
            "ts": 1336864012847944, 
            "selfRef": "https://example.com/ports/4fb04b3af473530a0f000000", 
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "name": "port1",
            "urn": "urn:ogf:network:domain=example.com:port=port1",
            "capacity": 10000000000,
            "description": "This is a sample port",
            "location": {
                "institution": "Indiana University"
            }
        }
    ]


**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.
`Location` HTTP header is not returned for the list of the Ports.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    
    [
        {
            "id": "4fb04bfaf473530a0f000002",
            "ts": 1336953850984704,
            "selfRef": "https://example.com/ports/4fb04bfaf473530a0f000002",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "name": "port1",
            "urn": "urn:ogf:network:domain=example.com:port=port1",
            "capacity": 10000000000,
            "description": "This is a sample port1",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            "id": "4fb04bfaf473530a0f000003",
            "ts": 1336953850985000,
            "selfRef": "https://example.com/ports/4fb04bfaf473530a0f000003",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "name": "port2",
            "urn": "urn:ogf:network:domain=example.com:port=port2",
            "capacity": 10000000000,
            "description": "This is a sample port2",
            "location": {
                "institution": "Indiana University"
            }
        },
        {
            "id": "4fb04bfaf473530a0f000004",
            "ts": 1336953850985287,
            "selfRef": "https://example.com/ports/4fb04bfaf473530a0f000004",
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
            "name": "port3",
            "urn": "urn:ogf:network:domain=example.com:port=port3",
            "capacity": 10000000000,
            "description": "This is a sample port3",
            "location": {
                "institution": "Indiana University"
            }
        }
    ]
