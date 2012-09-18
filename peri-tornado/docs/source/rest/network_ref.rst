.. _network_ref:

Network
========

For the data representation see
:ref:`Network Representation <network_schema>`.

.. tabularcolumns:: |l|l|l|J|


+---------------------------------+--------+---------------+----------------+
| Action                          | Verb   | Noun          | Description    |
+=================================+========+===============+================+
| :ref:`insert <network_insert>`  | POST   | /networks     | Creates new    |
|                                 |        |               | Network.       |
+---------------------------------+--------+---------------+----------------+
| :ref:`list/query <network_list>`| GET    | /networks     | Return all     |
|                                 |        |               | Networks       |
|                                 |        |               | registered in  |
|                                 |        |               | the UNIS       |
|                                 |        |               | instance.      |
+---------------------------------+--------+---------------+----------------+
| :ref:`get <network_get>`        | GET    | /networks/{id}| Return         |
|                                 |        |               | the Network    |
|                                 |        |               | representation.|
+---------------------------------+--------+---------------+----------------+
| :ref:`update <network_update>`  | PUT    | /networks/{id}| Update the     |
|                                 |        |               | specified      |
|                                 |        |               | Network.       |
+---------------------------------+--------+---------------+----------------+
| :ref:`delete <network_delete>`  | DELETE | /networks/{id}| Delete the     |
|                                 |        |               | specified      |
|                                 |        |               | Network.       |
+---------------------------------+--------+---------------+----------------+
| :ref:`patch <network_patch>`    | PATCH  | /networks/{id}| Patch the      |
|                                 |        |               | specified      |
|                                 |        |               | Network.       |
+---------------------------------+--------+---------------+----------------+




.. toctree::
   :maxdepth: 3
   
   network_list
   network_get
   network_insert
   network_update
   network_delete
   network_patch
   
