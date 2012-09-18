.. _node_schema:

Node Representation
===================

Extends  :ref:`network resource schema <networkresource_schema>`.

A Node is generally a device connected to, or part of, the network. A node does
not necessarily correspond to a physical machine. It MAY be a virtual device or
a group of devices [NML]_.

A node is connected to other network resources by its 
:ref:`Ports <port_schema>` [NML]_, and it might have zero or more 
forwarding rules.


JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/node>`_.


Attributes
~~~~~~~~~~
The following table contains only the node specific attributes, for the
attributes extended from network resource see 
:ref:`network resource schema <networkresource_schema>`.


+---------+-------+------------------------------------------------------------+
| Name    | Value | Description                                                |
+=========+=======+============================================================+
| ports   | list  | List of ports that are part of this node                   |
|         |       | Each element is HyperLink, to a port representation.       |
+---------+-------+------------------------------------------------------------+
| rules   | list  | List of forwarding rules implemented in the node           |
|         |       | Each element is object that has three attributes           |
|         |       | `priority`, `match`, and `actions`.                        |
+---------+-------+------------------------------------------------------------+


Example
~~~~~~~

The following is a simple Node representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
        "id": "123",
        "selfRef": "http://example.com/nodes/123",
        "ts": 1336775637000,
        "name": "node1",
        "urn": "urn:ogf:network:domain=example.com:node=node1",
        "description": "This is a sample node",
        "location": {
            "institution": "Indiana University"
        },
        "ports": [
            {
                "href": "http://example.com/ports/1",
                "rel": "full"
            }
        ],
        "rules": [
            {
                "priority": 100,
                "match": {
                    "type": "ipv4",
                    "value": "10.10.0.10"
                },
                "actions": [
                    {
                        "type": "forward",
                        "dest": "eth1"
                    },
                    {
                        "type": "forward",
                        "dest": "eth2"
                    }
                ]
            }
        ]
    }


Actions
-------

* :ref:`insert <node_insert>` Creates new node(s).
* :ref:`list/query <node_list>` Return all nodes registered in the UNIS instance.
* :ref:`get <node_get>` Return node representation.
* :ref:`update <node_update>` Update the specified node.
* :ref:`delete <node_delete>` Delete a node.
* :ref:`patch <node_patch>` patch the specified node.


.. rubric:: Footnotes
.. [NML] See Network Markup Language Base Schema version 1
