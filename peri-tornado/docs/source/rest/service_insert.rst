.. _service_insert:

Insert Service
=================

Creates a new :ref:`Service(s) <service_schema>`.

Request
--------

HTTP Request::
    
    POST https://example.com/services


Request Body
~~~~~~~~~~~~

:ref:`Service <service_schema>` representation or list of
:ref:`Services <service_schema>` representations.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Service(s) was inserted successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to create new Service(s).
* **409 Conflict** The Service(s) already inserted before.
* **500 Internal Server Error** Service(s) couldn't be inserted, try again.

Response Body
~~~~~~~~~~~~~~

If one Service submitted: The new :ref:`Service representation <service_schema>`
and `Location` HTTP header of that Service.

If list of Services submitted: List of :ref:`Services <service_schema>` created

Examples
--------

The examples include only important HTTP header fields for clarity.


Insert single Service
~~~~~~~~~~~~~~~~~~~~~~

**Request**::

    POST /services HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/service#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/service#",
        "accessPoint": "http://example.com:111/ms1/",
        "name": "service1",
        "status": "ON",
        "serviceType": "http://some_schema_domain/measurement_store",
        "ttl": 1000,
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

**Response**

*Note* that the `id`, `ts` and `selfRef` were created by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/service#
    Location: https://example.com/services/4fb4050bf4735379a7000000
    
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
