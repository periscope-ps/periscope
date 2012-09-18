.. _network_schema:

Network Representation
=======================

Extends :ref:`Node <node_schema>`.

Collection of :ref:`Network Resources <networkresource_schema>` that are
part of one Network.

At abstract level a Network can look like a Node with list of Ports that
connects it to other networks.


JSON Schema
-----------

See `<http://unis.incntre.iu.edu/schema/20120709/network>`_.


Attributes
~~~~~~~~~~
The following table contains only the *Network* specific attributes, 
for the attributes extended from Node see 
:ref:`Network Resource schema <node_schema>`.

.. tabularcolumns:: |l|l|J|

+----------+-------+---------------------------------------------------+
| Name     | Value | Description                                       |
+==========+=======+===================================================+
| ports    | list  | List of Ports that are part of this Network.      |
|          |       | Each element is HyperLink to a Port               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| nodes    | list  | List of Nodes that are part of this Network.      |
|          |       | Each element is HyperLink to a Node               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| links    | list  | List of Links that are part of this Network.      |
|          |       | Each element is HyperLink to a Link               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| paths    | list  | List of Paths that are part of this Network.      |
|          |       | Each element is HyperLink to a Path               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| networks | list  | List of Networks that are part of this Network.   |
|          |       | Each element is HyperLink to a Network            |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| domains  | list  | List of Domains that are part of this Network.    |
|          |       | Each element is HyperLink to a Domain             |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+


Example
~~~~~~~

The following is a simple Network example::


    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/network#",
        "id": "1",
        "selfRef": "https://example.com/networks/1",
        "ts": 1338494769852401,
        "ports": [
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000002",
                "ref": "full"
            },
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000003",
                "ref": "full"
            },
            {
                "href": "https://example.com/ports/4fc7cf319baf8a3c84000004",
                "ref": "full"
            }
        ],
        "nodes": [
            {
                "href": "https://example.com/nodes/4fc7cf319baf8a3c84000000",
                "ref": "full"
            },
            {
                "href": "https://example.com/nodes/4fc7cf319baf8a3c84000001",
                "ref": "full"
            }
        ]
        "links": [
            {
                "href": "https://example.com/links/4fc7d00b9baf8a3ec7000000",
                "ref": "full"
            },
            {
                "href": "https://example.com/links/4fc7d0139baf8a3ec7000001",
                "ref": "full"
            }
        ]
    }


Actions
-------
