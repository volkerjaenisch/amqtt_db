

class BaseDB():
    """
    Base API to the data base
    """

    @classmethod
    def from_connection_string(self, connect_string):
        """
        Construct from connection string
        """

    def init_db(self):
        """
        Initialize the DB
        """

    def create_session_table(self):
        """
        Creates the session table
        """

    def create_table(self):
        """
        Creates a table
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

    def insert(self, data, table):
        """
        Inserts data in a table
        """


