
class AMQTTDBException(Exception):
    """
    Base Exception for module
    """


class TopicNotFound(AMQTTDBException):
    """
    Raised if a topic is not found
    """


class TypeNotFound(AMQTTDBException):
    """
    Raised if a type is not found
    """


class NoSAMappingForType(AMQTTDBException):
    """
    Raised if no SA mapping for a given python type is found
    """


class NoPayloadDefinition(AMQTTDBException):
    """
    Raised if no payload definition is found in the config
    """


class WrongPayloadDefinition(AMQTTDBException):
    """
    Raised if the payload config cannot be loaded by the topic engine
    """
