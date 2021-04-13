from amqtt_db.base.base_decoder import BaseDecoder

import json


class JSONDecoder(BaseDecoder):

    @staticmethod
    def decode(payload):
        return json.loads(payload)
