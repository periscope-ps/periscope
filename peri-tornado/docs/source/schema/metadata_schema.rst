.. _metadata_schema:

Metadata Representation
=========================

Metadata describes the type of measurement data (the `eventType`),
the entity or entities being measured (the `subject`),
and the particular parameters of the measurement.

One key difference UNIS's metadata representation than perfSONAR’s metadata
representation is: the subject is a hyperlink to the actual network resource
representation registered at UNIS instance.
Two forces are pushing to have the subject to be a hyperlink rather than the 
actual description of the network resource. The first reason is having a
hyperlink in subject allows a better integration between the lookup service and
the topology service which allows the user to make topology based queries.
The second reason is the Hypermedia as the Engine of Application State (HATEOAS)
design constraint of REST. In HATEOAS, client interacts network application
entirely through hypermedia provided dynamically by the application server.


JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/metadata>`_.


Attributes
~~~~~~~~~~

+------------+-----------+-----------------------------------------------------+
| Name       | Value     | Description                                         |
+============+===========+=====================================================+
| id         | string    | Metadata's locally unique identifier.               |
+------------+-----------+-----------------------------------------------------+
| ts         | timestamp | time stamp of the last change on the metadata       |
|            |           | in nano-seconds.                                    |
+------------+-----------+-----------------------------------------------------+
| subject    | href      | Hyper link reference to Network Resource or         | 
|            |           | Metadata.                                           |
+------------+-----------+-----------------------------------------------------+
| parameters | object    | The parameters of the measurement.                  | 
+------------+-----------+-----------------------------------------------------+
| eventType  | string    | The type of measurement data.                       | 
+------------+-----------+-----------------------------------------------------+

Example
~~~~~~~

The following is a simple Metadata representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/metadata#",
        "id": "123",
        "selfRef": "http://example.com/metadata/123",
        "ts": 1336775637000,
        "subject": {
            "href": "https://example.com/ports/1",
            "rel": "full"
        },
        "eventType": "some event type",
        "parameters": {
            "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#",
            "collectionInterval": 30000
        }
    }


Actions
-------

* :ref:`insert <metadata_insert>` Creates new metadata.
* :ref:`list/query <metadata_list>` Return all metadata registered in the UNIS instance.
* :ref:`get <metadata_get>` Return metadata representation.
* :ref:`update <metadata_update>` Update the specified metadata.
* :ref:`delete <metadata_delete>` Delete a metadata.
* :ref:`patch <metadata_patch>` patch the specified metadata.

