.. _service_schema:

Service Representation
=======================

Extends  :ref:`Network Resource <networkresource_schema>`.

A Service object describes a certain capability being offered by
a :ref:`Network Resource <networkresource_schema>`.


JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/service>`_.

Attributes
~~~~~~~~~~
The following table contains only the Service specific attributes, for the
attributes extended from network resource see 
:ref:`network resource schema <networkresource_schema>`.


.. tabularcolumns:: |l|l|J|

+---------------+-----------+--------------------------------------------------+
| Name          | Value     | Description                                      |
+===============+===========+==================================================+
| accessPoint   | string    | The Service's access point. It's recommended to  |
|               |           | use URI format.                                  |
+---------------+-----------+--------------------------------------------------+
| serviceType   | sting     | The type of the service provided.                |
+---------------+-----------+--------------------------------------------------+
| ttl           | integer   | The duration in seconds that the service         |
|               |           | representation is valid since `ts` of the last   |
|               |           | service representation update.                   |
|               |           | If `ttl` defined, UNIS will delete the service   |
|               |           | when current_time > ttl * 1000000 + ts.          |
+---------------+-----------+--------------------------------------------------+
| runningOn     | href      | The network resource that runs the Service.      |
+---------------+-----------+--------------------------------------------------+


Example::
~~~~~~~~~~

The following is a simple service resource example::

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


Actions
-------

* :ref:`insert <service_insert>` Creates new Service.
* :ref:`list/query <service_list>` Return all Services registered in the UNIS instance.
* :ref:`get <service_get>` Return Service representation.
* :ref:`update <service_update>` Update the specified Service.
* :ref:`delete <service_delete>` Delete a Service.
* :ref:`patch <service_patch>` patch the specified Service.
