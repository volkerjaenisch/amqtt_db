from datetime import date, datetime, time

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from migrate.versioning.schema import Table as MiTable, Column as MiColumn

from amqtt_db.base.base_db import BaseDB

import sqlalchemy as sa

from amqtt_db.base.errors import NoSAMappingForType
from amqtt_db.base.type_mapper import BaseTypeMapper
from amqtt_db.db.base import Base


class SATypeMapper(BaseTypeMapper):
    """Maps python types to SQLAlchemy Column types"""

    def __init__(self):
        super(SATypeMapper, self).__init__()
        _map = {
            float: sa.FLOAT,
            int: sa.BigInteger,
            str: sa.VARCHAR,
            date: sa.types.Date,
            time: sa.types.Time,
            datetime: sa.types.DateTime,
        }
        self.map.update(_map)


class SA(BaseDB):
    """
    SQLAlchemy storage
    """
    autocommit = None
    connect_string = None
    engine = None
    session = None
    type_mapper = None

    def init_db(self, connect_string, autocommit=False, echo=False):
        """
        Initialize the DB
        """
        self.autocommit = autocommit
        self.connect_string = connect_string
        self.engine = create_engine(connect_string, echo=echo)
        self.session = sessionmaker(bind=self.engine, autocommit=self.autocommit)()
        self.type_mapper = SATypeMapper()

    def create_table(self, name, column_def):
        """
        Dynamically create a table from a column definition
        :param name: Table name
        :param column_def: Column definition, dict like
        """
        # The blueprint of the table
        table_description = {
            '__tablename__': name,
            'id': sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"), primary_key=True),
            'sqlite_autoincrement': True,
        }
        # The columns from the column_def are converted to SA Types and added to the blueprint
        for col_name, col_type in column_def.items():
            try:
                sa_col_type = self.type_mapper.map[col_type]
            except KeyError:
                raise NoSAMappingForType('Python type "{}" has no SA mapping defined'.format(col_type))
            table_description[col_name] = sa.Column(sa_col_type)

        # Construct the Table from the blueprint
        _table = type(name, (Base,), table_description)  # noqa: F841
        # Create the table in the DB
        Base.metadata.create_all(self.engine, tables=[Base.metadata.tables[name]])
        # Add the table to the metadata
        Base.metadata._add_table(name, None, Base.metadata.tables[name])

    def handle_new_columns(self, topic_cls, data):
        """
        Handle new columns.
        :param topic_cls: The topic decl class
        :param data: The data from the payload
        :return:
        """
        # Check if we really need additional columns
        new_cols = self.find_new_colums(topic_cls, data)
        # No new columns we return
        if len(new_cols) == 0:
            return
        # We need new columns, add them
        self.add_new_columns(topic_cls, new_cols)

    def find_new_colums(self, topic_cls, data):
        """
        This is good place to do some heuristics to check if really new columns should be made.
        :param topic_cls: The topic decl class
        :param data: The data from the payload
        :return: List of new columns if any
        """

        new_columns = {}
        existing_columns = topic_cls.__mapper__.columns
        for col_name, value in data.items():
            if col_name not in existing_columns:
                col_type = type(value)
                new_columns[col_name] = self.type_mapper.map[col_type]
        return new_columns

    def add_new_columns(self, topic_cls, column_def):
        """
        This is a bit of a hack since SQLAlchemy does not come with an out of the box solution
        for such a volatile DB usage we need. SQLAlchemy is mostly used for quite _static DB schema where migrations
        happen infrequently. At the IoT-Front we have to deal with permanent changes of the DB schema due to changes
        in the messages.
        """
        # The first part utilizes SQLalchemy.migrate to add new columns to the topic table.
        table_name = str(topic_cls.__table__.name)
        # Create a migration table.
        table = MiTable(table_name, MetaData(bind=self.engine))
        # for any new column
        for col_name, col_type in column_def.items():
            # Create a Migration Column
            col = MiColumn(col_name, col_type)
            # Do the migration
            col.create(table)

        # Now that we have a new table in the DB we should get rid of the old topic table,
        # so we remove it from the metadata.
        Base.metadata.remove(topic_cls.__table__)

        # The new Topic Table we get by inspecting the the Table from the DB correctly
        new_table = Table("test/topic_growth", Base.metadata, autoload_with=self.engine)

        # From the new Topic Table we generate its declarative class
        new_dcl = type(str(table_name), (Base,), {'__table__': new_table})

        # Since the new topic table was gained by inspection and not declarative construction our nice mechanism
        # (see db.base.py) to link the declarative class to the table automatically, failed.
        # so we set the link manually
        new_table.decl_class = new_dcl

        # At last we add the new topic table to the metadata.
        Base.metadata._add_table(table_name, None, new_table)

    def get_column_def(self, data):
        """
        Get a cloumn definition from data.
        :param data: Data from the payload
        :return: Column definition with the types of the data
        """
        result = {}
        for col_name, col_data in data.items():
            result[col_name] = type(col_data)
        return result

    def create_topic_table(self, topic, data):
        """
        Create a new topic table. At frist get the column definition. Then create the table from it.
        :param topic: MQTT Topic
        :param data: Data from the Payload
        """
        self.logger.debug('Building new table for topic {}'.format(topic))
        column_def = self.get_column_def(data)
        self.create_table(topic, column_def)

    def get_topic_cls(self, topic, data):
        """
        If the topic cannot be found in the metadata a new topic table will be creatd.
        For this process we need the current data to determine the columns needed.
        columns to be created.
        :param topic: The mqtt topic
        :param data: The data from the payload.
        :return: the declarative class for the topic
        """

        if topic not in Base.metadata.tables:
            self.create_topic_table(topic, data)

        topic_table = Base.metadata.tables[topic]

        return topic_table.decl_class

    def add_packet(self, session, sender, topic, data):
        """
        Insert a package into to DB.
        At first find the topic declarative class. Then instantiate it with the data from the payload.
        Add it to the session and commit.
        If a TypeError occurs we add the missing columns and try again.
        :param session: Not used
        :param sender: The sender ID of the package
        :param topic: The MQTT topic
        :param data: The data from the payload
        """

        topic_cls = self.get_topic_cls(topic, data)
        try:
            topic_line = topic_cls(**data)
        except TypeError:
            self.handle_new_columns(topic_cls, data)
            topic_cls = self.get_topic_cls(topic, data)
            topic_line = topic_cls(**data)

        self.session.add(topic_line)
        self.session.commit()

    def query_topic(self, topic, data):
        topic_cls = self.get_topic_cls(topic, data)

        query = self.session.query(topic_cls)
        for col_name, value in data.items():
            query = query.filter(getattr(topic_cls, col_name) == value)

        return query
