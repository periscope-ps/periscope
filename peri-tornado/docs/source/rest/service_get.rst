.. _service_get:

Get Service
============

Returns the specified :ref:`Service <service_schema>`.

Request
--------

HTTP Request::
    
    GET https://example.com/services/{id}

where `id` is the Service's identifier.


Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from, :ref:`Service <service_schema>`
can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.

Query on a single Service is executed over the current and the older versions of 
the Service's representation. The returned result when query is used is a 
list of Services.


Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A Service representation is returned.
* **304 Not modified** The client's cached version of the representation is still up to date.
* **401 Unauthorized** The supplied credentials are not enough read the Service.
* **404 Not found** No Service with the specified `id` exists.
* **500 Internal Server Error** Service couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a :ref:`Service representation <service_schema>` is returned.
If query is used the returned result is list of 
:ref:`Services representation <service_schema>`.


Examples
--------

The examples include only important HTTP header fields for clarity.

Get Service
~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/services/4fb4050bf4735379a7000000
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/service#

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/service#",
        "status": "ON",
        "id": "4fb4050bf4735379a7000000",
        "selfRef": "https://example.com/services/4fb4050bf4735379a7000000",
        "accessPoint": "http://example.com:111/ms1/",
        "serviceType": "http://some_schema_domain/measurement_store",
        "name": "service1",
        "ttl": 1000,
        "ts": 1337197835687922,
        "description": "sample MS service",
        "runningOn": {
            "href": "http://unis/nodes/1",
            "rel": "full"
        },
        "properties": {
            "configurations": {
                "default_collection_size": 10000,
                "max_collection_size": 20000
            },
            "summary": {
                "metadata": [
                    "http://unis/metadata/1",
                    "http://unis/metadata/2"
                ]
            }
        }
    }

