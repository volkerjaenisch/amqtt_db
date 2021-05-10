amqtt_db
========

![license](https://img.shields.io/github/license/volkerjaenisch/amqtt_db?style=flat-square)
[![Build Status](https://travis-ci.org/volkerjaenisch/amqtt_db.svg?branch=main)](https://travis-ci.org/volkerjaenisch/amqtt_db)
[![Coverage Status](https://coveralls.io/repos/github/volkerjaenisch/amqtt_db/badge.svg?branch=main)](https://coveralls.io/github/volkerjaenisch/amqtt_db?branch=main)
[![PyPI](https://img.shields.io/pypi/v/amqtt_db)](https://pypi.org/project/amqtt_db/)
[![Documantation](https://img.shields.io/readthedocs/amqtt-db.svg)](https://amqtt_db.readthedocs.io/en/latest/)

DB persistence for [amqtt](https://github.com/Yakifo/amqtt).

Objective
---------

amqtt_db persists payloads received by the [amqtt broker](https://github.com/Yakifo/amqtt) into performant relational databases.
SQLAlchemy as well as timescaleBD are the target RMDB-Systems.

amqtt_db will do four steps to persist the amqtt data:

 1) decoding the payload (e.G. from binary, JSON or which ever encoding)
 1) deserializing the payload to typed Python entities
 1) structure the session, topic, property, value information into a relational model of your choice
 1) generate the necessary tables, columns to store the data 

All of this steps can be configured via the amqtt yaml config. And you can even replace any these steps for each topic 
by your code in terms of Python plugins.
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
