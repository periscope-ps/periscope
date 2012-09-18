.. _collection_handler:

Hanlding Collection Resources
===============================

UNIS's approach to rely on hyperlinks for resources can slow some 
operations; specifically inserting new big Topology, Domain, or Network.

In this document we refere to Topology, Domain and Network as
network resources collection.
 
To mitigate the long round trip times for inserting each resource type,
UNIS allows inserting the entire network resources collection with self
hyperlinks. Self hyperlinks use JSONPath or JSONPointer.
When UNIS receive's a POST request to insert new Topology, Domain, or 
Network, it checks each network resource included (e.g. nodes, ports,
links, etc...) and generate new `ids` and `selfRefs` if needed.


Self Hyperlinks
----------------

JSONPath
~~~~~~~~~

JSONPath is an XPath equivlent for the JSON documents [JSONPATH]_.
The following table gives an overview of the JSONPath syntax.

.. tabularcolumns:: |l|J|

+------------+------------------------------------------------------+
| JSONPath   | Description                                          |
+============+======================================================+
| `$`        | the root object.                                     |
+------------+------------------------------------------------------+
| `@`        | the current object.                                  |
+------------+------------------------------------------------------+
| `.` or `[]`| child operator.                                      |
+------------+------------------------------------------------------+
| `..`       | recursive descent.                                   |
+------------+------------------------------------------------------+
| `*`        | wildcard for all names regadlress their names.       |
+------------+------------------------------------------------------+
| `[]`       | subscript operator.                                  |
+------------+------------------------------------------------------+
| `?()`      | applies a fileter expression.                        |
+------------+------------------------------------------------------+


JSONPointer
~~~~~~~~~~~~

JSONPointer identifes a specific value in JSON document [JSONPOINTER]_.



Examples
~~~~~~~~~

Example JSON Document
::::::::::::::::::::::::
    
The following is a simple :ref:`Topology <topology_schema>` example::


    {
        "$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
        "id": "1",
        "nodes": [
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                "name": "node1",
                "urn": "urn:ogf:network:domain=example.com:node=node1",
                "description": "This is a sample node",
                "ports": [
                    {
                        "href": "$..[?(@.[name=port1])]",
                        "rel": "full"
                    },
                    {
                        "href": "$..[?(@.[name=port2])]",
                        "rel": "full"
                    }
                ]
            },
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                "name": "node2",
                "urn": "urn:ogf:network:domain=example.com:node=node2",
                "description": "This is a sample node2",
                "ports": [
                    {
                        "href": "$..[?(@.[name=port3])]",
                        "rel": "full"
                    }
                ]
            }
        ],
        "ports": [
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                "name": "port1",
                "urn": "urn:ogf:network:domain=example.com:port=port1",
                "capacity": 1000
            },
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                "name": "port2",
                "urn": "urn:ogf:network:domain=example.com:port=port2",
                "capacity": 10000000
            },
            {
                "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                "name": "port3",
                "urn": "urn:ogf:network:domain=example.com:port=port3",
                "capacity": 10000000000
            }
        ]
    }



JSONPath Examples
::::::::::::::::::::::::

The following table shows some JSONPath queries and their results:

.. tabularcolumns:: |l|J|

+------------------------------+-------------------------------------+ 
| JSONPath                     | Reuslt                              |
+==============================+=====================================+
| `$.*`                        | return the entire document.         |
+------------------------------+-------------------------------------+
| `$.nodes`                    | return all nodes in the document    |
+------------------------------+-------------------------------------+
| `$.ports[0]`                 | return the first port.              |
+------------------------------+-------------------------------------+
| `$.ports[?(@.name=="port2")]`| return the port which has attribue  |
|                              | name=port2.                         |
+------------------------------+-------------------------------------+
| `$..[?(@.name=="port2")]`    | return any object which has         |
|                              | attribue name=port2.                |
+------------------------------+-------------------------------------+


JSONPointer Examples
::::::::::::::::::::::::

.. tabularcolumns:: |l|J|

+------------------------------+-------------------------------------+ 
| JSONPointer                  | Reuslt                              |
+==============================+=====================================+
| `#/`                         | return the entire document.         |
+------------------------------+-------------------------------------+
| `#/nodes`                    | return all nodes in the document    |
+------------------------------+-------------------------------------+
| `#/ports/0`                  | return the first port.              |
+------------------------------+-------------------------------------+



.. rubric:: Footnotes
.. [JSONPATH] http://goessner.net/articles/JsonPath/
.. [JSONPOINTER] http://tools.ietf.org/html/draft-pbryan-zyp-json-pointer-02
