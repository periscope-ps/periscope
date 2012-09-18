.. _port_ref:

Port
====

For the data representation see :ref:`Port Representation <port_schema>`.

+--------------------------------+--------+--------------+---------------------+
| Action                         | Verb   | Noun         | Description         |
+================================+========+==============+=====================+
| :ref:`insert <port_insert>`    | POST   | /ports/      | Creates new port(s).|
|                                |        |              |                     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`list/query <port_list>`  | GET    | /ports       | Return all ports    |
|                                |        |              | registered in the   |
|                                |        |              | UNIS instance.      |
+--------------------------------+--------+--------------+---------------------+
| :ref:`get <port_get>`          | GET    | /ports/{id}  | Return port         |
|                                |        |              | representation.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`update <port_update>`    | PUT    | /ports/{id}  | Update the          |
|                                |        |              | specified port.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`delete <port_delete>`    | DELETE | /ports/{id}  | Delete the          |
|                                |        |              | specified port.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`patch <port_patch>`      | PATCH  | /ports/{id}  | patch the           |
|                                |        |              | specified port.     |
+--------------------------------+--------+--------------+---------------------+

.. toctree::
   :maxdepth: 3
   
   port_list
   port_get
   port_insert
   port_update
   port_delete
   port_patch
   
