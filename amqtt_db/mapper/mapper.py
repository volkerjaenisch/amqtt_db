import json

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
        topic = packet.topic_name
        raw_data = json.loads(packet.payload.data)
        sender = list(raw_data.keys())[0]  # ToDo eliminate this waste of time
        data = raw_data[sender]

        await self.parent.db.add_packet(session, sender, topic, data)

        self.logger.debug("package {} saved".format(packet))
