class BasePlugin():
    """
    Plugin base class
    """

    config_path = 'plugins'   # dotted name path e.g 'plugins.timescaledb'
    config = None

    def __init__(self, context):
        self.context = context
        self.init_config(context)

    def init_config(self, context):
        """
        Use the config_path to derive the config portion of this plugin and store it under self.config.
        :param context:
        :return:
        """
        temp_config = context.config
        for path_part in self.config_path.split('.'):
            temp_config = temp_config[path_part]
        self.config = temp_config

    def register_events(self):
        """
        This method is called from the plugin manager to register the events
        """

