import aiounittest

from amqtt_db.plugin import DBPlugin
from amqtt_db.tests.resources.mockups import publish_packet, get_context, CONFIG_OK, CONFIG_TOPIC_WILDCARD, CONFIG_MISSING_RH_MEASURE


class TestPlugin2(aiounittest.AsyncTestCase):

    async def test_on_packet(self):
        context = get_context(CONFIG_OK)
        plugin = DBPlugin(context)
        await plugin.on_mqtt_packet_received(packet=publish_packet)


class TestPlugin3(aiounittest.AsyncTestCase):

    async def test_wildcard_topic(self):
        context = get_context(CONFIG_TOPIC_WILDCARD)
        plugin = DBPlugin(context)
        await plugin.on_mqtt_packet_received(packet=publish_packet)


class TestPlugin4(aiounittest.AsyncTestCase):

    async def test_initial_package_with_missing_payload_measure_entry(self):
        context = get_context(CONFIG_MISSING_RH_MEASURE)
        plugin = DBPlugin(context)
        await plugin.on_mqtt_packet_received(packet=publish_packet)
