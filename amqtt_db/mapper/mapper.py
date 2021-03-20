import json

from hbmqtt.mqtt import PublishPacket

from amqtt_db.base.base_mapper import BaseMapper


class WideMapper(BaseMapper):

    async def on_save_session(self, session):
        """
        Persist the session
        :param session: The current session
        """
        print("saving session {}".format(session))

    async def on_mqtt_packet_received(self, packet=None, session=None):
        if not isinstance(packet, PublishPacket):
            return

        print("saving package {}".format(packet))
        topic = packet.topic_name
        data = json.loads(packet.payload.data)
        sender = list(data.keys())[0]



        pass

