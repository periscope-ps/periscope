.. _port_update:

Update Port
===========

Updates the specified port with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/ports/{id}

where `id` is the port's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Port <port_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The port was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Port.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Port couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`port representation <port_schema>` and 
`Location` HTTP header of that port.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Port
~~~~~~~~~~~~~~~~


**Request**::

    PUT /ports/1 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is port has been updated",
        "location": {
            "institution": "Indiana University"
        }
    }

**Response**

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/port#
    Location: http://examples.com/ports/1
    
    {
        "id": "1", 
        "ts": 1336864012847944, 
        "selfRef": "https://example.com/ports/4fb04b3af473530a0f000000", 
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is port has been updated",
        "location": {
            "institution": "Indiana University"
        }
    }
    
