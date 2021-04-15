from hbmqtt.mqtt import PublishPacket

from amqtt_db.base.base_structure import BaseStructure


class WideStructure(BaseStructure):
    """
    Mapping each MQTT topics to a table. Any content in the Payload is a column in the table.
    """

    # async def on_save_session(self, session):
    #     """
    #     Persist the session
    #     :param session: The current session
    #     """
    #     self.logger.debug("saving session {}".format(session))

    async def on_mqtt_packet_received(self, packet=None, session=None):
        if not isinstance(packet, PublishPacket):
            return

        self.logger.debug("saving package {}".format(packet))
        decoder, deserializer = self.topic_engine.topic2handler(packet.topic_name)
        topic = packet.topic_name

        decoded_payload = decoder.decode(packet.payload.data)

        sender, data = list(decoded_payload.items())[0]
        typed_data, residual_data = deserializer.deserialize(data)  # ToDo: Handle residual data
        typed_data['sender'] = int(sender, 16)
        self.db.add_packet(session, sender, self.topic2SQL(topic), typed_data)

        self.logger.debug("package {} saved".format(packet))
