"""
Base deserializer class. The deserializer unpacks the payload and maps it to DB compatible types.
"""


class BaseDeserializer(object):

    @staticmethod
    def deserialize(data, types):
        """
        Map the data in data to types in structure.
        :param data: The incoming data structure
        :param types: The type structure usually a mapping type
        :return: a column_def structure
        """
