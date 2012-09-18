.. _link_schema:

Link Representation
===================

Extends  :ref:`Network Resource schema <networkresource_schema>`.

A *Link* object describes that there is a unidirectional/bidirectional
connection between two :ref:`Ports <port_schema>`.


A *Link* *SHOULD* have and attribute *endpoints* which is a list of two
hyperlinks to *Ports* if the *Link* is bidirectional or an object with two 
attributes *source* and *sink* if the *Link* is unidirectional.


JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/link>`_.


Attributes
~~~~~~~~~~
The following table contains only the Link specific attributes, for the
attributes extended from network resource see 
:ref:`Network Resource schema <networkresource_schema>`.

.. tabularcolumns:: |l|l|J|

+-----------+-------------+----------------------------------------------------+
| Name      | Value       | Description                                        |
+===========+=============+====================================================+
| directed  | boolean     | *true* *Link* is unidirectional.                   |
|           |             | *false* *Link* is bidirectional.                   |
+-----------+-------------+----------------------------------------------------+
| capacity  | number      | Link's capacity in bytes per second.               | 
+-----------+-------------+----------------------------------------------------+
| endpoints | list/object | List of two hyperlinks to Ports if bidirectional.  | 
|           |             | Object of source and sink if unidirectional.       |
+-----------+-------------+----------------------------------------------------+



Example
~~~~~~~

The following is an unidirectional Link representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/link#",
        "id": "link1",
        "selfRef": "https://example.com/links/link1"
        "ts": 1337711394175048, 
        "directed": true,
        "capacity": 10000000000,
        "endpoints": {
            "source": {
                "href": "https://example.com/ports/1",
                "ref": "full"
            },
            "sink": {
                "href": "https://example.com/ports/2",
                "ref": "full"
            }
        }
    }


The following is an bidirectional Link representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/link#",
        "id": "link2",
        "selfRef": "https://example.com/links/link2",
        "ts": 1337711394175048, 
        "directed": false,
        "capacity": 10000000000,
        "endpoints": [
            {
                "href": "https://example.com/ports/3",
                "ref": "full"
            },
            {
                "href": "https://example.com/ports/4",
                "ref": "full"
            }
        ]
    }



Actions
-------

* :ref:`insert <link_insert>` Creates new Link(s).
* :ref:`list/query <link_list>` Return all Links registered in the UNIS instance.
* :ref:`get <link_get>` Return Link representation.
* :ref:`update <link_update>` Update the specified Link.
* :ref:`delete <link_delete>` Delete a Link.
* :ref:`patch <link_patch>` patch the specified Link.
