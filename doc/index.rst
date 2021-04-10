.. amqtt_db documentation master file, created by
   sphinx-quickstart on Sat Apr 10 23:52:34 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

amqtt_db a persistence framework for amqtt
==========================================


Persisting MQTT-Messages is a quite complicated task. So this code may not be the simple solution to your application
with MQTT and Python you are looking for.

Persisting MQTT-Messages depends on the data coming in and the structure you will persist it into.

Even with typical IoT Home-Control scenarios there may be different schemes to store the MQTT data:
 - One table per room
 - One table for each observable
 - One table per sender
 - One table for each observable with references to the room, sender
 - or your setup

Since there are so different requirements amqtt_db is not a ready to go solution but an extensible framework.

    .. figure:: ./static/data_flow.png
        :width: 800px
        :align: center
        :alt: alternate text
        :figclass: align-center


The framework gives you four layers to transform your MQTT data into your favourite structure in the BD:

 - The first layer is the Mapper (One per plugin).
   A mapper defines the general flow of data. How to map the incoming data into the DB structure.
   The default is to map each sender into its own table with the observables as columns of this table.

   You are free to program any other mapper for your application.

 - The second layer is the Decoder (One per topic).
   For each topic you can define a Decoder. The decoder transforms the MQTT payload into a python data structure.
   E.G. if your MQTT client sends you a JSON Package you can decode it with a JSON-Decoder.

   You are free to program any other Decoder for your application.


 - The third layer is the deserialization (One per topic).
   For each topic you can define a deserialization. In a simple case this may be a dictionary mapping column names to python types.

   You are free to program any other Deserializer for your application.

 - The forth layer is the mapping to the DB. (One per plugin).
   This controls how Python data types are converted to BD datatypes.

   You are free to program any other DBmapper for your application.













.. toctree::
   :maxdepth: 2
   :caption: Contents:







Indices and tables
==================

* :ref:`genindex`
* :doc:`apidoc/modules`
* :ref:`search`
