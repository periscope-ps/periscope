.. _network_update:

Update Network
================

Updates the specified Network with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/networks/{id}

where `id` is the Network's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Network <network_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Network was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Network.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Network couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Network representation <network_schema>` and 
`Location` HTTP header of that Network.


Examples
--------

**TODO**
