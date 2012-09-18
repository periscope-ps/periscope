.. _path_ref:

Path
====

For the data representation see :ref:`Path Representation <path_schema>`.

+--------------------------------+--------+--------------+---------------------+
| Action                         | Verb   | Noun         | Description         |
+================================+========+==============+=====================+
| :ref:`insert <path_insert>`    | POST   | /paths/      | Creates new Path(s).|
|                                |        |              |                     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`list/query <path_list>`  | GET    | /paths       | Return all Paths    |
|                                |        |              | registered in the   |
|                                |        |              | UNIS instance.      |
+--------------------------------+--------+--------------+---------------------+
| :ref:`get <path_get>`          | GET    | /paths/{id}  | Return Path         |
|                                |        |              | representation.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`update <path_update>`    | PUT    | /paths/{id}  | Update the          |
|                                |        |              | specified Path.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`delete <path_delete>`    | DELETE | /paths/{id}  | Delete the          |
|                                |        |              | specified Path.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`patch <path_patch>`      | PATCH  | /paths/{id}  | patch the           |
|                                |        |              | specified Path.     |
+--------------------------------+--------+--------------+---------------------+

.. toctree::
   :maxdepth: 3
   
   path_list
   path_get
   path_insert
   path_update
   path_delete
   path_patch
   
