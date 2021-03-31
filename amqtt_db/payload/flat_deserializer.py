from datetime import datetime

from amqtt_db.base.base_deserializer import BaseDeserializer
from amqtt_db.base.utils import get_class_by_name


class FlatDeserializer(BaseDeserializer):

    def __init__(self, types_strs):
        self.type_strs = types_strs
        self.types = {}
        for key, type_str in types_strs.items():
            self.types[key] = (get_class_by_name(type_str))

    def get_datetime_from_list(self, datetime_list):
        result = datetime(
            datetime_list[0],
            datetime_list[1],
            datetime_list[2],
            datetime_list[3],
            datetime_list[4],
            datetime_list[5],
            datetime_list[6],
        )
        return result

    def deserialize(self, data):
        """
        Deserialize by key name assuming a flat data structure.
        :param data:
        :return: typed data
        """
        result = {}
        for key, value in data.items():
            result[key] = self.types[key](value)
        return result
