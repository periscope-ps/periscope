.. _domain_schema:

Domain Representation
=======================

Extends :ref:`Network Resource schema <networkresource_schema>`.

Collection of :ref:`Network Resources <networkresource_schema>` that are
part of an administrative *Domain*.


JSON Schema
-----------

See `<http://unis.incntre.iu.edu/schema/20120709/domain>`_.


Attributes
~~~~~~~~~~
The following table contains only the *Domain* specific attributes, 
for the attributes extended from Network Resource see 
:ref:`Network Resource schema <networkresource_schema>`.

.. tabularcolumns:: |l|l|J|

+----------+-------+---------------------------------------------------+
| Name     | Value | Description                                       |
+==========+=======+===================================================+
| ports    | list  | List of Ports that are part of this Domain.       |
|          |       | Each element is HyperLink to a Port               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| nodes    | list  | List of Nodes that are part of this Domain.       |
|          |       | Each element is HyperLink to a Node               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| links    | list  | List of Links that are part of this Domain.       |
|          |       | Each element is HyperLink to a Link               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| paths    | list  | List of Paths that are part of this Domain.       |
|          |       | Each element is HyperLink to a Path               |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| networks | list  | List of Networks that are part of this Domain.    |
|          |       | Each element is HyperLink to a Network            |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+
| domains  | list  | List of Domains that are part of this Domain.     |
|          |       | Each element is HyperLink to a Domain             |
|          |       | representation.                                   |
+----------+-------+---------------------------------------------------+


Example
~~~~~~~~

The following is a simple Domain example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/domain#",
        "id": "1",
        "ts": 1337976574414305,
        "selfRef": "https://example.com/domains/1",
        "nodes": [
            {
                "href": "https://example.com/nodes/4fbfe6fe9baf8a3e39000000",
                "ref": "full"
            },
            {
                "href": "https://example.com/nodes/4fbfe6fe9baf8a3e39000001",
                "ref": "full"
            }
        ],
        "ports": [
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000002",
                "ref": "full"
            },
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000003",
                "ref": "full"
            },
            {
                "href": "https://example.com/ports/4fbfe6fe9baf8a3e39000004",
                "ref": "full"
            }
        ]
    }



Actions
-------

* :ref:`insert <domain_insert>` Creates new Domain(s).
* :ref:`list/query <domain_list>` Return all Domains registered in the UNIS instance.
* :ref:`get <domain_get>` Return Domain representation.
* :ref:`update <domain_update>` Update the specified Domain.
* :ref:`delete <domain_delete>` Delete a Domain.
* :ref:`patch <domain_patch>` patch the specified Domain.

