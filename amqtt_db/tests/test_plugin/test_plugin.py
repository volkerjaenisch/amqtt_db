import unittest
import aiounittest


from amqtt_db.plugin import DBPlugin
from amqtt_db.tests.resources.mockups import context, publish_packet


class TestPlugin(aiounittest.AsyncTestCase):

    def test_plugin(self):
        _plugin = DBPlugin(context)    # noqa: F841

    async def test_on_packet(self):
        plugin = DBPlugin(context)
        await plugin.on_mqtt_packet_received(packet=publish_packet)


if __name__ == '__main__':
    unittest.main()
