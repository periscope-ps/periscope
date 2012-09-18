.. _service_ref:

Service
========

For the data representation see :ref:`Service Representation <service_schema>`.

+-----------------------------------+--------+----------------+----------------+
| Action                            | Verb   | Noun           | Description    |
+===================================+========+================+================+
| :ref:`insert <service_insert>`    | POST   | /services      | Creates new    |
|                                   |        |                | Service.       |
+-----------------------------------+--------+----------------+----------------+
| :ref:`list/query <service_list>`  | GET    | /services      | Return all     |
|                                   |        |                | Services       |
|                                   |        |                | registered in  |
|                                   |        |                | the UNIS       |
|                                   |        |                | instance.      |
+-----------------------------------+--------+----------------+----------------+
| :ref:`get <service_get>`          | GET    | /services/{id} | Return         |
|                                   |        |                | the Service    |
|                                   |        |                | representation.|
+-----------------------------------+--------+----------------+----------------+
| :ref:`update <service_update>`    | PUT    | /services/{id} | Update the     |
|                                   |        |                | specified      |
|                                   |        |                | Service.       |
+-----------------------------------+--------+----------------+----------------+
| :ref:`delete <service_delete>`    | DELETE | /services/{id} | Delete the     |
|                                   |        |                | specified      |
|                                   |        |                | Service.       |
+-----------------------------------+--------+----------------+----------------+
| :ref:`patch <service_patch>`      | PATCH  | /services/{id} | patch the      |
|                                   |        |                | specified      |
|                                   |        |                | Service .      |
+-----------------------------------+--------+----------------+----------------+


.. toctree::
   :maxdepth: 3
   
   service_list
   service_get
   service_insert
   service_update
   service_delete
   service_patch
   
