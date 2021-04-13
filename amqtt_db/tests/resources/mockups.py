
from unittest.mock import MagicMock

import yaml
from hbmqtt.broker import BrokerContext
from hbmqtt.mqtt import PublishPacket
from hbmqtt.mqtt.publish import PublishPayload, PublishVariableHeader

import logging

CONFIG = """
plugins:
  - amqtt_db

amqtt_db:
  db_structure : amqtt_db.structure.structure:WideStructure
  db_connection : 'sqlite:///test_topic.qlite'

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


context = MagicMock(spec=BrokerContext)()
context.config = yaml.load(CONFIG, Loader=yaml.FullLoader)
context.logger = logging.getLogger('test')


publish_packet = PublishPacket()
publish_packet.variable_header = PublishVariableHeader('hall/temp_rh')

payload = PublishPayload()
payload.data = bytearray(b'''{"3c610515b7c4": {"current time": 1617663897, "gas": 46.922, "temp": 24.35012, "press": 936.7473, "rh": 29.88471}}''')

publish_packet.payload = payload
