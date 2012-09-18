.. _networkresource_schema:

Base Network Resource Representation
====================================

Network Resource is the abstract base for all other UNIS resources
(except :ref:`Topology <topology_schema>`
and :ref:`Metadata <metadata_schema>`). UNIS does not accept directly
a network resource, but it does handle all the resources derived from
network resource.

Identifiers in UNIS works slightly different than that in perfSONAR and
NML community. The `id` field has been long used as URN to globally identify
a network resource. In the UNIS model the id field is locally unique,
while the full network resource URL is globally unique. For example there can
exist a two network resources with `id=id1` if the two resources are from
different UNIS instances `http://example1.com/nodes/id1` and 
`http://example2.com/nodes/id1`. Any UNIS network resource can have URN as an
attribute and it’s recommended to use either perfSONAR or NML URN naming schemes.


*NOTE:* In the perfSONAR and NML community network resources are called network 
objects. However, UNIS has been designed with native REST API in mind [REST]_.


JSON Schema
-----------

See `<http://unis.incntre.iu.edu/schema/20120709/networkresource>`_.


Attributes
~~~~~~~~~~
.. tabularcolumns:: |l|l|J|

+---------------+-----------+--------------------------------------------------+
| Name          | Value     | Description                                      |
+===============+===========+==================================================+
| $schema       | URI       | The schema that represents the current object.   |
+---------------+-----------+--------------------------------------------------+
| id            | sting     | Network resource's locally unique identifier.    |
+---------------+-----------+--------------------------------------------------+
| selfRef       | URI       | self URL reference to the network resource.      |
+---------------+-----------+--------------------------------------------------+
| ts            | timestamp | time stamp of the last change on the network     |
|               |           | resource in nano-seconds.                        |
+---------------+-----------+--------------------------------------------------+
| urn           | URN       | URN name of the network resource.                |
|               |           | UNIS doesn't mandate any specific URN schema,    |
|               |           | but it's recommended to use either perfSONAR or  |
|               |           | NML URN naming schemes.                          |
+---------------+-----------+--------------------------------------------------+
| name          | string    | the network resource name.                       |
+---------------+-----------+--------------------------------------------------+
| description   | string    | text description of the network resource.        |
+---------------+-----------+--------------------------------------------------+
| location      | object    | physical location of the network resource.       |
+---------------+-----------+--------------------------------------------------+
| lifetimes     | list      | list of lifetimes of the network resource.       |
|               |           | Each lifetime is an object with two attributes   |
|               |           | `start` and `end`                                |
+---------------+-----------+--------------------------------------------------+
| status        | string    | The status of network resource.                  |
+---------------+-----------+--------------------------------------------------+
| properties    | object    | additional custom properties for network         |
|               |           | resource.                                        |
+---------------+-----------+--------------------------------------------------+
| relations     | object    | relations for this network resource to other     |
|               |           | network resources.                               |
+---------------+-----------+--------------------------------------------------+


Example
~~~~~~~
The following is a simple network resource example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/networkresource#",
        "id": "resource1",
        "selfRef": "http://example.com/resource1",
        "ts": 1336775637000,
        "name": "example1",
        "urn": "urn:ogf:network:example1",
        "description": "This is a sample network resource",
        "lifetimes": [
            {
                "start": "2012-05-10T22:37:02+00:00",
                "end": "2012-05-11T22:37:02+00:00"
            }
        ],
        "location": {
            "institution": "Indiana University"
        },
        "properties": {
            "custom_prop1": "value1"
        },
        "relations": {
            "custom_relation": [
                {
                    "href": "http://example.com/resource2",
                    "rel": "full"
                }
            ]
        }
    }

.. rubric:: Footnotes
.. [REST] http://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_2_1
