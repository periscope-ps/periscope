.. _topology_schema:

Topology Representation
=======================

Collection of :ref:`Network Resources <networkresource_schema>` that are
part of a Topology.


JSON Schema
-----------

See `<http://unis.incntre.iu.edu/schema/20120709/topology>`_.


Attributes
~~~~~~~~~~

.. tabularcolumns:: |l|l|J|

+---------------+-----------+--------------------------------------------------+
| Name          | Value     | Description                                      |
+===============+===========+==================================================+
| $schema       | URI       | The schema that represents the current object.   |
+---------------+-----------+--------------------------------------------------+
| id            | sting     | Topology's locally unique identifier.            |
+---------------+-----------+--------------------------------------------------+
| selfRef       | URI       | self URL reference to the Topology.              |
+---------------+-----------+--------------------------------------------------+
| ts            | timestamp | time stamp of the last change on the Topology    |
|               |           | in nano-seconds.                                 |
+---------------+-----------+--------------------------------------------------+
| urn           | URN       | URN name of the Topology.                        |
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
| ports         | list      | List of Ports that are part of this Topology.    |
|               |           | Each element is HyperLink to a Port              |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+
| nodes         | list      | List of Nodes that are part of this Topology.    |
|               |           | Each element is HyperLink to a Node              |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+
| links         | list      | List of Links that are part of this Topology.    |
|               |           | Each element is HyperLink to a Link              |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+
| paths         | list      | List of Paths that are part of this Topology.    |
|               |           | Each element is HyperLink to a Path              |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+
| networks      | list      | List of Networks that are part of this Topology. |
|               |           | Each element is HyperLink to a Network           |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+
| domains       | list      | List of Domains that are part of this Topology.  |
|               |           | Each element is HyperLink to a Domain            |
|               |           | representation.                                  |
+---------------+-----------+--------------------------------------------------+


Example
~~~~~~~

Actions
-------
