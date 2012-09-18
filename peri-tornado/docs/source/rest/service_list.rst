.. _service_list:

List/Query Service
===================

Return all :ref:`Services <service_schema>` registered in the UNIS instance.

Request
-------

HTTP Request::

    GET https://example.com/services

Query Parameters
~~~~~~~~~~~~~~~~~

All the attributes defined in, or extended from,
:ref:`Services <service_schema>` can be queried by the mechanisms defined in
:ref:`UNIS query language <query_ref>`.
   

Request Body
~~~~~~~~~~~~

Empty


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **200 OK** A list (might be empty) of Services is returned successfully.
* **401 Unauthorized** The supplied credentials are not enough to read Services.
* **500 Internal Server Error** Service(s) couldn't be read, try again.

Response Body
~~~~~~~~~~~~~

If successful, a list (might be empty) of :ref:`Service <service_schema>`
will be returned.



Examples
--------

The examples include only important HTTP header fields for clarity.

List all Services
~~~~~~~~~~~~~~~~~~

**Request**::
    
    GET https://example.com/services
    Content-Type: application/perfsonar+json
    Accept: application/perfsonar+json
    Connection: close
    

**Response**::
    
    HTTP/1.1 200 OK
    Content-Type: application/perfsonar+json; profile=http://unis.incntre.iu.edu/schema/20120709/service#
    
    [
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
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/service#",
            "status": "ON",
            "id": "4fb4050bf4735379a7000000",
            "selfRef": "https://example.com/services/4fb4050bf4735379a7000000",
            "accessPoint": "http://example.com/ms2/",
            "serviceType": "http://some_schema_domain/measurement_store",
            "name": "service2",
            "ttl": 1000,
            "ts": 1337197835687922,
            "description": "sample MS service2",
            "runningOn": {
                "href": "http://unis/nodes/2",
                "rel": "full"
            }
        },
        {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/wservice#",
            "status": "ON",
            "id": "4fb409e5f4735379a7000002",
            "selfRef": "https://example.com/services/4fb409e5f4735379a7000002",
            "accessPoint": "http://example.com/ms3/",
            "serviceType": "http://some_schema_domain/measurement_store",
            "name": "service3",
            "ttl": 1000,
            "ts": 1337197835687922,
            "description": "sample MS service3",
            "runningOn": {
                "href": "http://unis/nodes/3",
                "rel": "full"
            }
        }
    ]
