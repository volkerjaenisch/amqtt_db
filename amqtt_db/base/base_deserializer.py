"""
Base deserializer class. The deserializer unpacks the payload and maps it to DB compatible types.
"""


class BaseDeserializer(object):

    def deserialize(self, data):
        """
        Map the data in data to types. This is done according to the given structure for this particular
        data.
        :param data: The incoming data
        :return: a structure of the form {value:type}
        """
