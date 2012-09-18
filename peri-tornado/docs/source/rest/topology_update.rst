.. _topology_update:

Update Topology
================

Updates the specified Topology with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/topologies/{id}

where `id` is the Topology's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Topology <topology_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Topology was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Topology.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Topology couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Topology representation <topology_schema>` and 
`Location` HTTP header of that Topology.


Examples
--------

**TODO**
