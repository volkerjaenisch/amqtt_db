from hbmqtt.mqtt import PublishPacket

from amqtt_db.base.base_mapper import BaseMapper


class WideMapper(BaseMapper):

    async def on_save_session(self, session):
        """
        Persist the session
        :param session: The current session
        """
        self.logger.debug("saving session {}".format(session))

    async def on_mqtt_packet_received(self, packet=None, session=None):
        if not isinstance(packet, PublishPacket):
            return

        self.logger.debug("saving package {}".format(packet))
        decoder, deserializer = self.parent.topic_engine.topic2handler(packet.topic_name)
        topic = packet.topic_name

        decoded_payload = decoder.decode(packet.payload.data)

        sender, data = list(decoded_payload.items())[0]
        typed_data = deserializer.deserialize(data)
        await self.parent.db.add_packet(session, sender, topic, typed_data)

        self.logger.debug("package {} saved".format(packet))
