import inspect
import weakref

from amqtt_db.base.base_plugin import BasePlugin
from amqtt_db.base.base_topic import BaseTopicEngine
from amqtt_db.base.constants import TOPIC_ENGINE, DB_CONNECT_STRING, DB_MAPPER
from amqtt_db.db.db_sa import SA
from amqtt_db.mapper.mapper import WideMapper


class DBPlugin(BasePlugin):
    """
    The DB Plugin
    """

    config_path = 'amqtt_db'
    db = None
    mapper = None
    topic_engine = None

    def __init__(self, context):
        super(DBPlugin, self).__init__(context)
        self.compose()

    def compose(self):
        """
        Constructs the plugin by choosing the mapper and the DB interface according to the config
        """
        self.get_topic_engine()
        self.get_mapper()
        self.get_db()
        self.register_events()

    def get_topic_engine(self):
        """
        Gets the topic engine according to the config
        """
        if TOPIC_ENGINE not in self.config:
            topic_engine = BaseTopicEngine
        else:
            topic_engine = self.config[TOPIC_ENGINE]

        try:
            self.topic_engine = topic_engine(self)
        except KeyError:
            self.context.logger.error('No topic engine could be started {}'.format(topic_engine))
            raise


    def get_db(self):
        """
        Gets the DB according to the config
        """
        if DB_CONNECT_STRING not in self.config:
            raise

        try:
            connect_string = self.config[DB_CONNECT_STRING]
        except KeyError:
            self.context.logger.error('No "db_connection" found in config file at {}'.format(self.config_path))
            raise

        try:
            self.db = SA(self, connect_string)
        except Exception as e:
            msg = 'Connection to DB with connect string {} failed with error {}'
            self.context.logger.error(msg.format(connect_string, e))

    def get_mapper(self):
        """
        Gets the mapper according to the config
        """
        if DB_MAPPER not in self.config:
            raise
        try:
            _mapper_type = self.config[DB_MAPPER]
        except KeyError:
            self.context.logger.error('No "DB mapper" found in config file at {}'.format(self.config_path))
            raise

        try:
            self.mapper = WideMapper(self)  # ToDo: Mapper Factory
        except Exception as e:
            print(e)


    def register_events(self):
        events = {}
        method_names = inspect.getmembers(self.mapper, predicate=inspect.ismethod)
        for method_name, method in method_names:
            if method_name.startswith('on_'):
                events[method_name] = method
        return events

    def __getattr__(self, item):
        try:
            result = self.__getattribute__(item)
        except AttributeError:
            result = getattr(self.mapper, item)
        return result
