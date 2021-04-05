

class TopicNotFound(Exception):
    """
    Raised if a topic is not found
    """


class TypeNotFound(Exception):
    """
    Raised if a type is not found
    """


class NoSAMappingForType(Exception):
    """
    Raised if no SA mapping for a given python type is found
    """
