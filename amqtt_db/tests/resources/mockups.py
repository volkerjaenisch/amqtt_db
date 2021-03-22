
from unittest.mock import patch, Mock, MagicMock

from hbmqtt.broker import BrokerContext
from hbmqtt.mqtt import PublishPacket
from hbmqtt.mqtt.publish import PublishPayload

context = MagicMock(BrokerContext)()
context.config = {
    'amqtt_db' : {
        'mapper': 'wide',
        'connect': 'sqlite://test.sqlite'
    }
}


publish_packet = MagicMock(PublishPacket)()

payload = MagicMock(PublishPayload)()
payload.data = bytearray(b'{"3c610515b7c4": {"current time": [2021, 3, 22, 0, 22, 47, 44, 892838], "bme": {"gas": 46.922, "temp": 24.35012, "press": 936.7473, "rh": 29.88471}}}')

publish_packet.payload = payload



