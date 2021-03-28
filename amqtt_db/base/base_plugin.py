from amqtt_db.base.constants import ON_SAVE_SESSION, ON_FIND_SESSION, ON_DEL_SESSION, ON_BROKER_POST_SHUTDOWN, \
    ON_MQTT_PACKET_RECEIVED, BASE_CONFIG_PATH
from amqtt_db.base.delegator import Delegator


class BasePlugin(Delegator):
    """
    Plugin base class
    """
    DELEGATED_METHODS = {
        'mapper': [
            ON_SAVE_SESSION,
            ON_FIND_SESSION,
            ON_DEL_SESSION,
            ON_BROKER_POST_SHUTDOWN,
            ON_MQTT_PACKET_RECEIVED,
            ]
    }

    config_path = BASE_CONFIG_PATH   # dotted name path e.g 'plugins.timescaledb'
    config = None

    def __init__(self, context):
        self.context = context
        self.init_config(context)

    def init_config(self, context):
        """
        Use the config_path to derive the config portion of this test_plugin and store it under self.config.
        :param context:
        :return:
        """
        temp_config = context.config
        for path_part in self.config_path.split('.'):
            temp_config = temp_config[path_part]
        self.config = temp_config

    def register_events(self):
        """
        This method is called from the test_plugin manager to register the events
        """
