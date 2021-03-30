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
        handler = self.parent.topic_engine.topic2handler(packet.topic_name)

        decoded_payload = handler[0].decode(packet.payload.data)

        # ToDo : Here type enrichment

        await self.parent.db.add_packet(session, sender, topic, data)

        self.logger.debug("package {} saved".format(packet))
