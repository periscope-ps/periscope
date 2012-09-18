.. _path_schema:

Path Representation
===================

Extends  :ref:`network resource schema <networkresource_schema>`.

A Path is an ordered list of connected 
:ref:`network resources <networkresource_schema>`.



JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/path>`_.


Attributes
~~~~~~~~~~
The following table contains only the Path specific attributes, for the
attributes extended from network resource see 
:ref:`network resource schema <networkresource_schema>`.


+----------+----------+----------------------------------------------------+
| Name     | Value    | Description                                        |
+==========+==========+====================================================+
| directed | Boolean  | Directed or undirected Path.                       |
+----------+----------+----------------------------------------------------+
| hops     | list     | ordered list of connected                          |
|          |          | :ref:`network resources <networkresource_schema>`. |
+----------+----------+----------------------------------------------------+


Example
~~~~~~~

The following is a simple Path representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/path#",
        "id": "pathid",
        "selfRef": "http://example.com/paths/pathid",
        "ts": 1336775637000,
        "name": "path1",
        "urn": "urn:ogf:network:domain=example.com:path=path1",
        "description": "This is a sample path",
        "directed": true,
        "hops": [
            {
                "href": "http://example.com/ports/1",
                "rel": "full"
            },
            {
                "href": "http://example.com/nodes/1",
                "rel": "full"
            },
            {
                "href": "http://example.com/ports/2",
                "rel": "full"
            },
            {
                "href": "http://example.com/nodes/2",
                "rel": "full"
            },
            {
                "href": "http://example.com/ports/3",
                "rel": "full"
            }
        ]
    }


Actions
-------

* :ref:`insert <path_insert>` Creates new Path(s).
* :ref:`list/query <path_list>` Return all Paths registered in the UNIS instance.
* :ref:`get <path_get>` Return the Path's representation.
* :ref:`update <path_update>` Update the specified Path.
* :ref:`delete <path_delete>` Delete a Path.
* :ref:`patch <path_patch>` patch the specified Path.


