from amqtt_db.base.base_deserializer import BaseDeserializer


class FlatDeserializer(BaseDeserializer):

    def __init__(self, types):
        self.types = types

    @staticmethod
    def deserialize(data, types):
        """
        Deserialize by key name assuming a flat data structure.
        :param data:
        :param types:
        :return:
        """
        result = {}
        for key, value in data.items():
            result[key] = types[key](value)

