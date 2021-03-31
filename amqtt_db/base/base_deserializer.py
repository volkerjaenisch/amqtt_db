"""
Base deserializer class. The deserializer unpacks the payload and maps it to DB compatible types.
"""


class BaseDeserializer(object):

    def __init__(self, types):
        self.types = types

    def deserialize(self, data):
        """
        Map the data in data to types in structure.
        :param data: The incoming data structure
        :return: a column_def structure
        """
