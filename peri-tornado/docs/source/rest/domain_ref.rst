.. _domain_ref:

Domain
========

For the data representation see :ref:`Domain Representation <domain_schema>`.

.. tabularcolumns:: |l|l|l|J|


+---------------------------------+--------+---------------+----------------+
| Action                          | Verb   | Noun          | Description    |
+=================================+========+===============+================+
| :ref:`insert <domain_insert>`   | POST   | /domains      | Creates new    |
|                                 |        |               | Domain.        |
+---------------------------------+--------+---------------+----------------+
| :ref:`list/query <domain_list>` | GET    | /domains      | Return all     |
|                                 |        |               | Domains        |
|                                 |        |               | registered in  |
|                                 |        |               | the UNIS       |
|                                 |        |               | instance.      |
+---------------------------------+--------+---------------+----------------+
| :ref:`get <domain_get>`         | GET    | /domains/{id} | Return         |
|                                 |        |               | the Domain     |
|                                 |        |               | representation.|
+---------------------------------+--------+---------------+----------------+
| :ref:`update <domain_update>`   | PUT    | /domains/{id} | Update the     |
|                                 |        |               | specified      |
|                                 |        |               | Domain.        |
+---------------------------------+--------+---------------+----------------+
| :ref:`delete <domain_delete>`   | DELETE | /domains/{id} | Delete the     |
|                                 |        |               | specified      |
|                                 |        |               | Domain.        |
+---------------------------------+--------+---------------+----------------+
| :ref:`patch <domain_patch>`     | PATCH  | /domains/{id} | patch the      |
|                                 |        |               | specified      |
|                                 |        |               | Domain .       |
+---------------------------------+--------+---------------+----------------+




.. toctree::
   :maxdepth: 3
   
   domain_list
   domain_get
   domain_insert
   domain_update
   domain_delete
   domain_patch
   
