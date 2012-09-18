.. _service_update:

Update Service
================

Updates the specified Service with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/services/{id}

where `id` is the Service's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Service <service_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Service was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Service.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Service couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Service representation <service_schema>` and 
`Location` HTTP header of that Service.


Examples
--------

The examples include only important HTTP header fields for clarity.


Updating a Service
~~~~~~~~~~~~~~~~~~~


**Request**::

    PUT /services/4fb4050bf4735379a7000000 HTTP/1.1    
    Host: example.com
    Accept: application/perfsonar+json
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/services#
    Content-Length: 248
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/service#",
        "accessPoint": "http://example.com:111/ms1/",
        "name": "service1",
        "status": "ON",
        "serviceType": "http://some_schema_domain/measurement_store",
        "ttl": 2000,
        "description": "sample MS service updated",
        "runningOn": {
            "href": "http://unis/nodes/2",
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

*Note* that the `ts` was updated by the server.::

    HTTP/1.1 201 Created    
    Content-Type: application/perfsonar+json ;profile=http://unis.incntre.iu.edu/schema/20120709/service#
    Location: /services/4fb4050bf4735379a7000000
    
    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/service#",
        "status": "ON",
        "id": "4fb4050bf4735379a7000000",
        "selfRef": "https://example.com/services/4fb4050bf4735379a7000000",
        "accessPoint": "http://example.com:111/ms1/",
        "serviceType": "http://some_schema_domain/measurement_store",
        "name": "service1",
        "ttl": 2000,
        "ts": 1337200240812328,
        "description": "sample MS service updated",
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
    
