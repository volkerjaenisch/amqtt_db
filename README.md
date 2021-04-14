amqtt_db
========

![license](https://img.shields.io/github/license/volkerjaenisch/amqtt_db?style=flat-square)

![travis](https://api.travis-ci.org/volkerjaenisch/amqtt_db.svg?branch=main)

![coverals](https://img.shields.io/coveralls/github/volkerjaenisch/amqtt_db/master.svg)

![PyPI](https://img.shields.io/pypi/v/amqtt_db?style=flat-square)

![Documantation](https://img.shields.io/readthedocs/amqtt-db.svg)


DB and timescale DB persistence for amqtt.

Objective
---------

amqtt_db will persist payloads received by the [amqtt broker](https://github.com/Yakifo/amqtt) into performant relational databases.
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

Documentation
-------------

Please have a look at the [documentation](http://amqtt-db.readthedocs.io).
