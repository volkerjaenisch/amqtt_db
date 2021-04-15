
from amqtt_db.base.base_deserializer import BaseDeserializer
from amqtt_db.base.utils import get_class_func_by_name


class FlatDeserializer(BaseDeserializer):

    def __init__(self, types_strs):
        """
        Flat deserialize is given a column_name -> type_str mapping.
        It derives a mapping column_name -> type (Class/Function(Factory))
        :param types_strs: column_name -> types_str mapping

        >>> fs = FlatDeserializer({'a_datetime': 'datetime.datetime.fromtimestamp'})
        >>> type(fs.col2type['a_datetime'])
        <class 'builtin_function_or_method'>

        >>> fs = FlatDeserializer({'a_float': 'float'})
        >>> fs.col2type['a_float']
        <class 'float'>

        >>> fs = FlatDeserializer({'a_float': 'floata'})
        >>> fs.col2type['a_float']
        <class 'float'>

        """

        self.type_strs = types_strs
        self.col2type = {}    # Hold the actual mapping
        for key, type_str in types_strs.items():
            self.col2type[key] = (get_class_func_by_name(type_str))  # get the string to class/function mapping

    def deserialize(self, data):
        """
        Deserialize by key name assuming a flat data structure.
        :param data: data
        :return: typed data
        """
        result = {}
        residual = {}
        for key, value in data.items():
            try:
                result[key] = self.col2type[key](value)  # do the mapping
            except KeyError:
                residual[key] = None
        return result, residual
