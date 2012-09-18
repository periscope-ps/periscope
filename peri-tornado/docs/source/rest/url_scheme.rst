.. _url_scheme:

URL Pattern
============

While REST doesn't mandate using a specific URL scheme, UNIS recommends the use 
of simple pattern to make it easier to use. Confirming to the RESTful
architectural style, all network resources has the same interface to insert,
query, update, and possibly delete.


.. tabularcolumns:: |l|l|l|J|

+---------------+--------+-----------------+-----------------------------------+
| Action        | Verb   | Noun            | Description                       |
+===============+========+=================+===================================+
| Insert        | POST   | /resources      | Creates new resource.             |
+---------------+--------+-----------------+-----------------------------------+
| List or Query | GET    | /resources      | Return all resources.             |
+---------------+--------+-----------------+-----------------------------------+
| Get           | GET    | /resources/{id} | Return the resource representation|
+---------------+--------+-----------------+-----------------------------------+
| Update        | PUT    | /resources/{id} | Update the specified resource.    |
+---------------+--------+-----------------+-----------------------------------+
| Delete        | DELETE | /resources/{id} | Delete the specified resource.    |
+---------------+--------+-----------------+-----------------------------------+
| Patch Update  | PATCH  | /resources/{id} | patch the specified resource.     |
+---------------+--------+-----------------+-----------------------------------+


*/resources* can be one of: :ref:`nodes <node_ref>`, :ref:`ports <port_ref>`,
:ref:`links <link_ref>`, :ref:`paths <path_ref>`, :ref:`services <service_ref>`,
:ref:`domains <domain_ref>`, networks, topologies, and
:ref:`metadata <metadata_ref>`.



Supported MIME Types
-------------------------

UNIS supports multiple MIME types:

* `application/perfsonar+json` for JSON data exchange.
* `application/perfsonar+xml` for legacy perfSONAR XML data exchange; **NOT IMPLEMENTED**.
* `application/perfsonar+bson`  **NOT IMPLEMENTED**..
* `text/event-stream` optional for web browser clients
* `text/html` optional for web browser clients, if the Periscope instance does want to serve regular web browsers it can disable this MIME Type.
