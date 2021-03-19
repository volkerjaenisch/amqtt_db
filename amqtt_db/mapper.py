from amqtt_db.base.base_mapper import BaseMapper


class WideMapper(BaseMapper):


    async def on_save_session(self, session):
        """
        Persist the session
        :param session: The current session
        """
        print("saving session {}".format(session))


    async def on_mqtt_packet_received(self, packet):
        print("saving package {}".format(packet))
