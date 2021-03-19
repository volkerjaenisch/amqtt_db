import weakref


class BaseMapper(object):
    """
    API for the mqtt messages
    """

    def __init__(self, parent):
        self.parent = weakref.ref(parent)

    @classmethod
    def from_mapper_type(self, parent, mapper_type):
        """
        Construct a mapper from mapper type
        """
        return BaseMapper(parent)  # ToDo: Factory of mappers

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

