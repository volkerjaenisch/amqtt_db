Payload handling
================

MQTT has no defined structure of the payload since it is only a transport protocol.
With MQTT 5 a mime-type for the payload may be specified. 
So one sender can specify that its payload is JSON or python_pickle or XML or plain text or something else.  

This will help a lot on decoding the payload, but it does not solve the problem identifying the data types used 
in these structures.

MQTT 5 is not even supported by amqtt.

So amqtt_db needs a really clever strategy to identify the data types in the payload to effectively map them to data base columns.

There are two concepts to solve this problem:
 - Self describing data conventions like Homie, XML, Python-Pickle
 - Manual description of the payload data types

Each concept has its pros and cons:
 - The self description data conventions are cool for auto detection and varying or evolving parameter sets. 
    But on the other hand are they limited to their conventions and extensibility. Also not many sensors may speak these protocols. 

 - The manual description (E.g. a configuration file) lacks the auto detection and flexibility. 
    But on the other hand with this concept any sensor can be integrated in amqtt_db.

I will try to program amqtt_db as agnostic as possible to these two concepts: But at the end of the day for any 
packet coming its payload has to be decoded into type:value pairs to play with amqtt_db.


Realisation:
============

 - Payload decoders (JSON, XML, Pickel, Plain text, etc.).
   
    In the config a payload decoder for topic matching patterns can be assigned. This is an emulation of the MQTT5 
    feature of a mime-Type, but not on a per packet basis. The payload decoders are specified in terms of Python decoder classes. 
    These classes have to have as ancestor PayloadDecoderBase. 

 - Payload structure.

    In the config payload structures can be assigned to topic matching patterns. Payload structures are at least of the mapping type.
    They consist of key:type pairs and have to be compatible with the given payload decoder.
   
 - Dealing with corner cases.
    
    There may be sensors out there that only send "23.4" meaning 23.4 Degree Celsius. We will find a solution. 