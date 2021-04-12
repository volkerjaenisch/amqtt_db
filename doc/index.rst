.. amqtt_db documentation master file, created by
   sphinx-quickstart on Sat Apr 10 23:52:34 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

amqtt_db a persistence framework for amqtt
==========================================


Persisting MQTT-Messages is a quite complicated task. You have weak specified data coming in from the senders and you
like them stored in a structure your application likes the best. But what is the best structure?

Even typical IoT Home-Control data may have quite different schemes to store:
 - One table per room
 - One table for each observable
 - One table per sender
 - or your setup

Since there are so different possible "best" structures no software will be able to handle all of them accurately.
So amqtt_db is not a ready to go solution but an extensible framework.

There are many things I hate on frameworks.
 - Unnecessary boilerplate
 - Favoring flexibility over performance
 - Being hermetically

but also some things I really like.
 - Batteries included
 - A base ground to settle on
 - DRY concepts

Therefore I tried to come up with more of the later and less of the former.

amqtt_db architecture
=====================


    .. figure:: ./static/data_flow.png
        :width: 800px
        :align: center
        :alt: alternate text
        :figclass: align-center


The amqtt_db framework is configured completely via the mqtt yaml config file.
Four processing layers transform your MQTT data into your favourite structure in the BD:

 - The first layer is the DB Structure (One per plugin).
   A DBStructure defines the general flow of data. How to map the incoming data into the DB structure.
   The default is to map each sender into its own table with the observables as columns of this table.

   You are free to program any other DBStructure for your application.

 - The second layer is the Decoder (One per topic).
   For each topic you can define a Decoder. The decoder transforms the MQTT payload into a python data structure.
   E.G. if your MQTT client sends you a JSON Package you can decode it with a JSON-Decoder.

   You are free to program any other Decoder for your application.

 - The third layer is the Deserializer (One per topic).
   For each topic you can define a Deserializer which is the conversion of the data items (measures) into typed python objects.
   E.G. Convert "[2021, 03, 01, 00, 04, 55]" into a datetime object. In a simple case this may be a dictionary mapping column names to python types.

   You are free to program any other Deserializer for your application.

 - The forth layer is the DB Mapper. (One per plugin).
   A DB mapper controls how Python data types are converted to DB data types.
   E.G. How to convert a Python Boolean to the DB? As a short int, as a Boolean field, or as a char.

   You are free to program any other DB mapper for your application.



.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :doc:`apidoc/modules`
* :ref:`search`
