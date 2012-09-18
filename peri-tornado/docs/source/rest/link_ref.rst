.. _link_ref:

Link
========

For the data representation see :ref:`Link Representation <link_schema>`.

.. tabularcolumns:: |l|l|l|J|

+--------------------------------+--------+-------------+----------------------+
| Action                         | Verb   | Noun        | Description          |
+================================+========+=============+======================+
| :ref:`insert <link_insert>`    | POST   | /links      | Creates new Link.    |
+--------------------------------+--------+-------------+----------------------+
| :ref:`list/query <link_list>`  | GET    | /links      | Return all Links     |
|                                |        |             | registered in the    |
|                                |        |             | UNIS instance.       |
+--------------------------------+--------+-------------+----------------------+
| :ref:`get <link_get>`          | GET    | /links/{id} | Return the Link      |
|                                |        |             | representation.      |
+--------------------------------+--------+-------------+----------------------+
| :ref:`update <link_update>`    | PUT    | /links/{id} | Update the specified |
|                                |        |             | Link.                |
+--------------------------------+--------+-------------+----------------------+
| :ref:`delete <link_delete>`    | DELETE | /links/{id} | Delete the specified |
|                                |        |             | Link.                |
+--------------------------------+--------+-------------+----------------------+
| :ref:`patch <link_patch>`      | PATCH  | /links/{id} | patch the specified  |
|                                |        |             | Link .               |
+--------------------------------+--------+-------------+----------------------+


.. toctree::
   :maxdepth: 3
   
   link_list
   link_get
   link_insert
   link_update
   link_delete
   link_patch
   
