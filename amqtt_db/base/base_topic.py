"""
Base of a topic engine, routing the payload to the configured deserializer
"""
import re

from amqtt_db.base.constants import PAYLOAD_CONFIG
from amqtt_db.base.errors import TopicNotFound, NoPayloadDefinition, WrongPayloadDefinition
from amqtt_db.base.utils import get_class_func_by_name


class BaseTopicEngine(object):

    def __init__(self, parent):
        self.parent = parent
        self.topic_handlers = {}    # topic to handler mapping
        self.decoders = {}
        self.deserializers = {}
        self.topic_re = {}    # topic to handler mapping
        self.read_config(parent.config)

    def read_config(self, config):
        """
        Build a simple parse tree out of the payload config
        :param config: The payload config
        """
        try:
            payload_config = config[PAYLOAD_CONFIG]
        except KeyError:
            raise NoPayloadDefinition
        try:
            for key, value in payload_config.items():
                entry = list(value.items())[0]
                decoder_cls_name = entry[0]
                decoder_class = get_class_func_by_name(decoder_cls_name)
                if decoder_cls_name in self.decoders:
                    decoder = self.decoders[decoder_cls_name]
                else:
                    decoder = decoder_class()
                    self.decoders[decoder_cls_name] = decoder

                deserialier_config = entry[1]
                deserializer_cls_name, types = list(deserialier_config.items())[0]
                deserializer_class = get_class_func_by_name(deserializer_cls_name)

                if deserializer_cls_name in self.deserializers:
                    deserializer = self.deserializers[deserializer_cls_name]
                else:
                    deserializer = deserializer_class(types)
                    self.deserializers[deserializer_cls_name] = deserializer

                self.topic_handlers[key] = [decoder, deserializer]
                self.topic_re[re.compile(key)] = self.topic_handlers[key]
        except (KeyError, AttributeError):
            raise WrongPayloadDefinition

    def topic2handler(self, topic):
        """
        Get a handler for a topic according to the payload definitions
        :param topic:
        :return: The handler
        """
        if topic in self.topic_handlers:
            return self.topic_handlers[topic]
        else:
            result = self.match_topic(topic)
            if result is not None:
                self.topic_handlers[topic] = result
                return result
        raise TopicNotFound()

    def match_topic(self, topic):
        """
        Match a topic to an handler according to the config
        :param topic:
        :return:
        """
        for regex, handler in self.topic_re.items():
            if regex.match(topic):
                self.topic_handlers[topic] = self.topic_re[regex]
                return self.topic_re[regex]

        return None
