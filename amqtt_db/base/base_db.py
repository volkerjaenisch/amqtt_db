import weakref


class BaseDB(object):
    """
    Base API to the data base
    """

    def __init__(self, parent, connect_string):
        self.parent = weakref.ref(parent)
        self.init_db(connect_string)

    def init_db(self, connect_string):
        """
        Initialize the DB
        """

    def create_session_table(self):
        """
        Creates the session table
        """

    def create_table(self, name, column_def):
        """
        Creates a table based on table_name and column definition. Where Column_def is a dict of col_name, col_type
        """

    def extend_table_colums(self, table, colums):
        """
        Extends a table with some columns
        """

    def drop_table(self):
        """
        Creates a table
        """

    def empty_table(self):
        """
        Empties a table
        """

    def add_packet(self, session, sender, topic, data):
        """
        persist a packet
        """
