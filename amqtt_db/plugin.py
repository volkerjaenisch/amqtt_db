from amqtt_db.base.base_db import BaseDB
from amqtt_db.base.base_mapper import BaseMapper
from amqtt_db.base.base_plugin import BasePlugin


class DBPlugin(BasePlugin):
    """
    The DB plugin
    """

    config_path = 'amqtt_db'

    mapper = None
    db = None

    def __init__(self, context):
        super(DBPlugin, self).__init__(context)
        self.compose()

    def compose(self):
        """
        Constructs the plugin by choosing the mapper and the DB interface according to the config
        """
        self.mapper = self.get_mapper()
        self.db = self.get_db()

    def get_db(self):
        """
        Gets the DB according to the config
        """
        if 'connect' not in self.config:
            raise

        try:
            connect_string = self.config['connect']
        except KeyError:
            self.context.logger.error('No "connect" found in config file at {}'.format(self.config_path))
            raise

        try:
            self.db = BaseDB.from_connection_string(connect_string)
        except Exception as e:
            print(e)

    def get_mapper(self):
        """
        Gets the mapper according to the config
        """
        if 'mapper' not in self.config:
            raise
        try:
            mapper_type = self.config['mapper']
        except KeyError:
            self.context.logger.error('No "mapper" found in config file at {}'.format(self.config_path))
            raise

        try:
            self.mapper = BaseMapper.from_mapper_type(mapper_type)
        except Exception as e:
            print(e)

    def register_events(self):
        events = {}
        for name, func in self.mapper.__dict__.items():
            if name.startswith('on_'):
                events[name] = func
        return events
