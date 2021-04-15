from amqtt_db.base.constants import ON_SAVE_SESSION, ON_FIND_SESSION, ON_DEL_SESSION, ON_BROKER_POST_SHUTDOWN, \
    ON_MQTT_PACKET_RECEIVED, BASE_CONFIG_PATH
from amqtt_db.base.delegator import Delegator


class BasePlugin(Delegator):
    """
    Plugin base class
    """
    DELEGATED_METHODS = {
        'structure': [
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
        super(BasePlugin, self).__init__()
        self.context = context
        self.init_config(context)

    def init_config(self, context):
        """
        Use the config_path to derive the config portion of this test_plugin and store it under self.config.
        :param context:
        :return:
        """
        try:
            temp_config = context.config
            path_parts = self.config_path.split('.')
            for path_part in path_parts[:-1]:
                temp_config = temp_config[path_part]
            if path_parts[-1] in temp_config:
                self.config = context.config[path_parts[-1]]
            else:
                raise ImportError

        except KeyError as e:
            msg = 'amqtt_db: Plugin config not found under "{}" in the config file '.format(self.config_path)
            self.context.logger.error(msg)
            raise ImportError(e)

    def register_events(self):
        """
        This method is called from the test_plugin manager to register the events
        """
