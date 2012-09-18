.. _port_schema:

Port Representation
===================

Extends  :ref:`network resource schema <networkresource_schema>`.

A Port connects a :ref:`Node <node_schema>` to the rest of the world.
A Port might have zero or more forwarding rules.


JSON Schema
-----------
See `<http://unis.incntre.iu.edu/schema/20120709/port>`_.


Attributes
~~~~~~~~~~
The following table contains only the *Port* specific attributes, for the
attributes extended from network resource see 
:ref:`network resource schema <networkresource_schema>`.

.. tabularcolumns:: |l|l|J|

+-----------+--------+---------------------------------------------------------+
| Name      | Value  | Description                                             |
+===========+========+=========================================================+
| address   | object | Object of `{"type": "type", "address": "some_val"}`,    |
|           |        | For example: `{"type": "ipv4", "address": "10.10.0.10"}`|
+-----------+--------+---------------------------------------------------------+
| capacity  | number | Port's capacity in bytes per second.                    | 
+-----------+--------+---------------------------------------------------------+
| index     | string | Port's index.                                           | 
+-----------+--------+---------------------------------------------------------+
| rules     | list   | List of forwarding rules implemented in the port        | 
|           |        | Each element is object that has three attributes        |
|           |        | `priority`, `match`, and `actions`.                     |
+-----------+--------+---------------------------------------------------------+

Example
~~~~~~~

The following is a simple Port representation example::

    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
        "id": "123",
        "selfRef": "https://example.com/port/123",
        "ts": 1336775637000,
        "name": "port1",
        "urn": "urn:ogf:network:domain=example.com:port=port1",
        "capacity": 10000000000,
        "description": "This is a sample port",
        "location": {
            "institution": "Indiana University"
        }
    }


Actions
-------

* :doc:`insert </rest/port_insert>` Creates new port(s).
* :doc:`list/query </rest/port_list>` Return all ports registered in the UNIS instance.
* :doc:`get </rest/port_get>` Return port representation.
* :doc:`update </rest/port_update>` Update the specified port.
* :doc:`delete </rest/port_delete>` Delete a port.
* :doc:`patch </rest/port_patch>` patch the specified port.

