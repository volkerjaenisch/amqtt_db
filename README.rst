amqtt_db
========

.. image:: https://travis-ci.org/volkerjaenisch/amqtt_db.svg?branch=master
   :target: https://travis-ci.org/github/volkerjaenisch/amqtt_db
   :alt: Travis CI status

.. image:: https://img.shields.io/coveralls/github/volkerjaenisch/amqtt_db/master.svg
   :target: https://coveralls.io/github/volkerjaenisch/amqtt_db?branch=master
   :alt: Coverage Status

#.. image:: https://img.shields.io/readthedocs/pkandcatapde.svg
#   :target: http://pkandcatapde.readthedocs.io
#   :alt: Documentation


DB and timescale DB persistence for amqtt.

Objective
---------

amqtt_db will persist payloads received by the amqtt broker into performant relational databases.
SQLAlchemy as well as timescaleBD are the target RMDB-Systems.

amqtt_db will do two steps to persist the amqtt data:

 1) decoding, and deserializing the payload of the MQTT packets
 1) transformation of the session, topic, property, value information into relational data models  

amqtt_db will support a wide variety of decodings, deserialisations, and target database models, by design.

amqtt is designed to be enhanced and extended.

Performance
-----------

Flexibility comes with a penalty on performance. The more layers of classes and filters we 
implement the higher the performance penalty.   

So we optimize the data flow by an optimistic approach. 

amqtt_db expects that the decoding, deserializing, transformations, target DB, target tables, table colums 
etc. are all well in place if it deals with a single incoming packet.
If the handling of that package fails, exceptions will be raised, and the error handling rushes in to deal with the problem.

Since the change rate on the decoding, deserializing, database model is quite low this optimistic approach will be quite performant. 

Details
-------

Please have a look at [payload handling](./payload_handling.md)