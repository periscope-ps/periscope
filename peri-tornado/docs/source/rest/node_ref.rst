.. _node_ref:

Node
====

For the data representation see :ref:`Node Representation <node_schema>`.

+--------------------------------+--------+--------------+---------------------+
| Action                         | Verb   | Noun         | Description         |
+================================+========+==============+=====================+
| :ref:`insert <node_insert>`    | POST   | /nodes/      | Creates new node(s).|
|                                |        |              |                     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`list/query <node_list>`  | GET    | /nodes       | Return all nodes    |
|                                |        |              | registered in the   |
|                                |        |              | UNIS instance.      |
+--------------------------------+--------+--------------+---------------------+
| :ref:`get <node_get>`          | GET    | /nodes/{id}  | Return node         |
|                                |        |              | representation.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`update <node_update>`    | PUT    | /nodes/{id}  | Update the          |
|                                |        |              | specified node.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`delete <node_delete>`    | DELETE | /nodes/{id}  | Delete the          |
|                                |        |              | specified node.     |
+--------------------------------+--------+--------------+---------------------+
| :ref:`patch <node_patch>`      | PATCH  | /nodes/{id}  | patch the           |
|                                |        |              | specified node.     |
+--------------------------------+--------+--------------+---------------------+

.. toctree::
   :maxdepth: 3
   
   node_list
   node_get
   node_insert
   node_update
   node_delete
   node_patch
   
