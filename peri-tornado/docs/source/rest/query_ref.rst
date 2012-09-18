.. _query_ref:

Querying UNIS
==============

UNIS defines simple query language across the different UNIS resources.

Querying exact values
----------------------

Any attribute defined in the UNIS representation can be queried directly.

**Example**

If the user wants to query a node with `name=node1`::

    http://example.com/nodes?name=node1


Nested attributes can be queried using dot notation

**Example**

If the user wants to query a node with `{"properties": {"prop1": {"nested": "val"}}}`::

    http://example.com/nodes?properties.prop1.nested=val1


Logical operators
------------------

AND
~~~~

**Example**

If the user wants to query a node with `name=node1`::

    http://example.com/nodes?name=node1&ts=1336935293363662
    http://example.com/nodes?name=node1&name=node2  # wont return any thing :-)

OR
~~~~
**Example**

If the user wants to query a node with `name=node1` or `ts=1336935293363662`::

    http://example.com/nodes?name=node1|ts=1336935293363662

IN
~~
**Example**

If the user wants to query a node with `name in [node1, node2, node3]`

    http://example.com/nodes?name=node1,node2,node3
    

=: Equal
~~~~~~~~~~~
**Example**

If the user wants to query a node with `ts=1336935293363662`

    http://example.com/nodes?ts=1336935293363662

lt: Less than
~~~~~~~~~~~~~~
**Example**

If the user wants to query a node with `ts<1336935293363662`

    http://example.com/nodes?ts=lt=1336935293363662

lte: Less than or equal
~~~~~~~~~~~~~~~~~~~~~~~
**Example**

If the user wants to query a node with `ts<=1336935293363662`

    http://example.com/nodes?ts=lte=1336935293363662

gt: Greater than
~~~~~~~~~~~~~~~~
**Example**

If the user wants to query a node with `ts>1336935293363662`

    http://example.com/nodes?ts=gt=1336935293363662

gte: Greater than or equal
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Example**

If the user wants to query a node with `ts>=1336935293363662`

    http://example.com/nodes?ts=gte=1336935293363662


Query values data types
-------------------------

Basic values in UNIS queries are simply a string of characters. UNIS tries to
reason about some values; `ts` and `ttl` as an example. However, UNIS supports
typed values. The syntax of a typed value is::
    
    type:value

UNIS supports the following value types:

* string
* number
* boolean: possible values True, False, 0, 1


Examples::

    http://example.com/nodes?properties.prop1.nested=number:10
    http://example.com/nodes?properties.prop1.nested=boolean:true
    


Filtering specific fields
--------------------------

The user can filter specific fields in the results using `fields` parameter.
The following example shows how to show only the `id` and `institution`::

    http://example.com/nodes?fields=id,location.institution


Limiting results
--------------------------

The number of returned results can be limited by `limit` parameter.
The following example shows how to limit results to 10 nodes::
    
    http://example.com/nodes?limit=2
    

Examples
---------

The following example shows `(name=node1 OR name=node2 OR ts=1336935293363662) AND
{"location": {"institution": "Indiana University"}}`::

    http://example.com/nodes?name=node1,node2|ts=1336935293363662&location.institution=Indiana

