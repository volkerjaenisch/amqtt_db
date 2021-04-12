import weakref


class BaseStructure(object):
    """
    API for the mqtt handlers
    """

    def __init__(self, topic_engine, db, context):
        self._topic_engine = weakref.ref(topic_engine)
        self._context = weakref.ref(context)
        self._db = weakref.ref(db)
        self.logger = self.context.logger

    @property
    def db(self):
        return self._db()

    @property
    def context(self):
        return self._context()

    @property
    def topic_engine(self):
        return self._topic_engine()

    def topic2SQL(self, topic):
        """
        Generic way to generate a table name from MQTT topic
        :param topic: MQTT topic
        :return: SQL confirm table name
        """
        return topic

    # @classmethod
    # def from_mapper_type(cls, parent, _mapper_type):
    #     """
    #     Construct a structure from structure type
    #     """
    #     return BaseMapper(parent)  # ToDo: Factory of mappers

    async def on_save_session(self, session):
        """
        Persist the session
        :param session: The current session
        """

    async def on_find_session(self, client_id):
        """
        Retrieve a session by client ID
        :param client_id:
        :returns The session
        """

    async def on_del_session(self, client_id):
        """
        Delete a session by ClientID
        :param client_id:
        """

    async def on_broker_post_shutdown(self):
        """
        Shutdown the database if broker has shut down
        """
