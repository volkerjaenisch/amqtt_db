from unittest.mock import MagicMock

import yaml
from hbmqtt.broker import BrokerContext
from hbmqtt.mqtt import PublishPacket
from hbmqtt.mqtt.publish import PublishPayload, PublishVariableHeader

import logging


CONFIG_OK = """
plugins:
  - amqtt_db

amqtt_db:
  db_structure : amqtt_db.structure.structure.WideStructure
  db_connection : 'sqlite:///memory'

  payload :
    hall/temp_rh :
      amqtt_db.payload.json_decoder.JSONDecoder :
        amqtt_db.payload.flat_deserializer.FlatDeserializer :
          temp : float
          rh : float
          press : float
          gas : float
          'current time' : datetime.datetime.utcfromtimestamp
"""

CONFIG_PLUGIN_NAME_WRONG = """
plugins:
  - amqtt_db22
"""

CONFIG_AMQTT_DB_MISSING = """
plugins:
  - amqtt_db
"""

CONFIG_TOPIC_ENGINE_WRONG = """
plugins:
  - amqtt_db

amqtt_db:
    topic_engine : None
"""

CONFIG_NO_DB_CONNECT_STRING = """
plugins:
  - amqtt_db

amqtt_db:
    payload :
        hall/temp_rh :
          amqtt_db.payload.json_decoder.JSONDecoder :
            amqtt_db.payload.flat_deserializer.FlatDeserializer :
              temp : float
"""

CONFIG_NO_DB_STRUCTURE = """
plugins:
  - amqtt_db

amqtt_db:
    db_connection : 'sqlite:///memory'
    payload :
        hall/temp_rh :
          amqtt_db.payload.json_decoder.JSONDecoder :
            amqtt_db.payload.flat_deserializer.FlatDeserializer :
              temp : float
"""


CONFIG_WRONG_DB_STRUCTURE = """
plugins:
  - amqtt_db

amqtt_db:
    db_structure : amqtt_db.structure.structure.WideStru
    db_connection : 'sqlite:///memory'
    payload :
        hall/temp_rh :
          amqtt_db.payload.json_decoder.JSONDecoder :
            amqtt_db.payload.flat_deserializer.FlatDeserializer :
              temp : float
"""

CONFIG_TOPIC_WILDCARD = """
plugins:
  - amqtt_db

amqtt_db:
    db_structure : amqtt_db.structure.structure.WideStructure
    db_connection : 'sqlite:///memory'
    payload :
        hall/* :
          amqtt_db.payload.json_decoder.JSONDecoder :
            amqtt_db.payload.flat_deserializer.FlatDeserializer :
              temp : float
              press : float
              gas : float
              rh : float
              'current time' : datetime.datetime.utcfromtimestamp
"""

CONFIG_MISSING_RH_MEASURE = """
plugins:
  - amqtt_db

amqtt_db:
    db_structure : amqtt_db.structure.structure.WideStructure
    db_connection : 'sqlite:///memory'
    payload :
        hall/temp_rh :
          amqtt_db.payload.json_decoder.JSONDecoder :
            amqtt_db.payload.flat_deserializer.FlatDeserializer :
              temp : float
              press : float
              gas : float
              'current time' : datetime.datetime.utcfromtimestamp
"""


def get_context(config):
    context = MagicMock(spec=BrokerContext)()
    context.config = yaml.load(config, Loader=yaml.FullLoader)
    context.logger = logging.getLogger('test')
    context.logger.handlers = [logging.NullHandler()]
    return context


publish_packet = PublishPacket()
publish_packet.variable_header = PublishVariableHeader('hall/temp_rh')

payload = PublishPayload()
payload.data = bytearray(b'''{"3c610515b7c4": {"current time": 1617663897, "gas": 46.922, "temp": 24.35012, "press": 936.7473, "rh": 29.88471}}''')

publish_packet.payload = payload
