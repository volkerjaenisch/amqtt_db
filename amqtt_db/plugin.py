import inspect
import sys
import traceback

from amqtt_db.base.base_plugin import BasePlugin
from amqtt_db.base.base_topic import BaseTopicEngine
from amqtt_db.base.constants import TOPIC_ENGINE, DB_CONNECT_STRING, DB_STRUCTURE
from amqtt_db.base.utils import get_class_func_by_name
from amqtt_db.db.db_sa import SA


class DBPlugin(BasePlugin):
    """
    The DB Plugin
    """

    config_path = 'plugins.amqtt_db'
    db = None
    structure = None
    topic_engine = None

    def __init__(self, context):
        super(DBPlugin, self).__init__(context)
        self.compose()

    def handle_exception(self, e):
        msg = "amqtt_db ERROR: {}".format(e.__repr__())
        self.context.logger.error(msg)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for line in traceback.format_tb(exc_traceback):
            self.context.logger.error(line[:-1])
        raise ImportError()

    def compose(self):
        """
        Constructs the plugin by choosing the structure and the DB interface according to the config
        """
        self.get_topic_engine()
        self.get_db()
        self.get_structure()
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
        except Exception as e:
            self.context.logger.error('No topic engine could be started')
            self.handle_exception(e)

    def get_db(self):
        """
        Gets the DB according to the config
        """
        try:
            connect_string = self.config[DB_CONNECT_STRING]
        except KeyError as e:
            self.context.logger.error('No "db_connection" found in config file at: "{}"'.format(self.config_path))
            self.handle_exception(e)

        try:
            self.db = SA(self.context, connect_string)
        except Exception as e:
            msg = 'Connection to DB with connect string: "{}" failed'.format(connect_string)
            self.context.logger.error(msg)
            self.handle_exception(e)

    def get_structure(self):
        """
        Gets the structure according to the config
        """
        try:
            structure_cls_str = self.config[DB_STRUCTURE]  # noqa: F841
        except KeyError as e:
            msg = 'Cannot read/find "db_structure" entry in config file part "{}"'.format(self.config_path)
            self.context.logger.error(msg)
            self.handle_exception(e)

        try:
            structure_cls = get_class_func_by_name(structure_cls_str)
            self.structure = structure_cls(self.topic_engine, self.db, self.context)  # ToDo: Mapper Factory
        except Exception as e:
            self.handle_exception(e)

    def register_events(self):
        events = {}
        method_names = inspect.getmembers(self.structure, predicate=inspect.ismethod)
        for method_name, method in method_names:
            if method_name.startswith('on_'):
                events[method_name] = method
        return events

    def __getattr__(self, item):
        try:
            result = self.__getattribute__(item)
        except AttributeError:
            result = getattr(self.structure, item)
        return result
