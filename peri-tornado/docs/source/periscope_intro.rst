.. _periscope_intro:

Introduction
==============

The recent advancement in Software Defined Networks (SDNs) increased the need
for a centric view of the network that is reflects the actual topology of
the network and provide different real-time and historical data about
network resources. Many previous models for the network has been proposed;
To name few NMWG, NDL, and the under development model NML.
However all these models focused in how to model a network and left many open
questions that make these models less optimal for the use in SDN world.
One of the biggest limitations of these models that they don't define a well
defined API or at best a suboptimal API is defined to interact with
these models.

Currently networks are viewed from different perspectives; design,
configuration and management, monitoring, and analysis.
Each view of the network is using one or more models to represent the network.
For example, NETCONF uses YANG for network configuration
and management while perfSONAR uses NMWG for network monitoring.
Generally network models are designed and optimized with unique properties
and level of abstraction to serve a certain view of the network.
However, using different inconsistent models for each views often leads to
inconsistent views of the same network.
