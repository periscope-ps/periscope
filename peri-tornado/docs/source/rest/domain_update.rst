.. _domain_update:

Update Domain
================

Updates the specified Domain with new representation.


Request
--------

HTTP Request::
    
    PUT https://example.com/domains/{id}

where `id` is the Domain's identifier.


Request Body
~~~~~~~~~~~~

:ref:`Domain <domain_schema>` representation.


Response
--------

Response Status Codes
~~~~~~~~~~~~~~~~~~~~~~
* **201 Created** The Domain was updated successfully.
* **400 Bad Request** The data given in the request failed validation.
* **401 Unauthorized** The supplied credentials are not enough to update the Domain.
* **409 Conflict** The same `ts` exists before.
* **500 Internal Server Error** Domain couldn't be updated, try again.


Response Body
~~~~~~~~~~~~~~
The new :ref:`Domain representation <domain_schema>` and 
`Location` HTTP header of that Domain.


Examples
--------

**TODO**
