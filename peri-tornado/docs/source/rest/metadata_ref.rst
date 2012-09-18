.. _metadata_ref:

Metadata
========

For the data representation see
:ref:`Metadata Representation <metadata_schema>`.

+-----------------------------------+--------+----------------+----------------+
| Action                            | Verb   | Noun           | Description    |
+===================================+========+================+================+
| :ref:`insert <metadata_insert>`   | POST   | /metadata/     | Creates new    |
|                                   |        |                | Metadata.      |
+-----------------------------------+--------+----------------+----------------+
| :ref:`list/query <metadata_list>` | GET    | /metadata      | Return all     |
|                                   |        |                | metadata       |
|                                   |        |                | registered in  |
|                                   |        |                | the UNIS       |
|                                   |        |                | instance.      |
+-----------------------------------+--------+----------------+----------------+
| :ref:`get <metadata_get>`         | GET    | /metadata/{id} | Return         |
|                                   |        |                | the meatadata  |
|                                   |        |                | representation.|
+-----------------------------------+--------+----------------+----------------+
| :ref:`update <metadata_update>`   | PUT    | /metadata/{id} | Update the     |
|                                   |        |                | specified      |
|                                   |        |                | metadata.      |
+-----------------------------------+--------+----------------+----------------+
| :ref:`delete <metadata_delete>`   | DELETE | /metadata/{id} | Delete the     |
|                                   |        |                | specified      |
|                                   |        |                | metadata.      |
+-----------------------------------+--------+----------------+----------------+
| :ref:`patch <metadata_patch>`     | PATCH  | /metadata/{id} | patch the      |
|                                   |        |                | specified      |
|                                   |        |                | metadata.      |
+-----------------------------------+--------+----------------+----------------+

.. toctree::
   :maxdepth: 3
   
   metadata_list
   metadata_get
   metadata_insert
   metadata_update
   metadata_delete
   metadata_patch
   
