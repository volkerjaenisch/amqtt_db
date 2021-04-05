from datetime import date, datetime, time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    def create_table(self, name, column_def=None):
        """
        Dynamically create a table from a column definition
        :param name: Table name
        :param column_def: Column definition, dict like
        """
        if column_def is None:
            return

        table_description = {
            '__tablename__': name,
            'id': sa.Column(sa.BigInteger().with_variant(sa.Integer, "sqlite"), primary_key=True),
            'sqlite_autoincrement': True,
        }

        for col_name, col_type in column_def.items():
            try:
                sa_col_type = self.type_mapper.map[col_type]
            except KeyError:
                raise NoSAMappingForType('Python type "{}" has no SA mapping defined'.format(col_type))
            table_description[col_name] = sa.Column(sa_col_type)

        _table = type(name, (Base,), table_description)
        Base.metadata.create_all(self.engine, tables=[Base.metadata.tables[name]])

    def get_column_def(self, data):
        result = {}
        for col_name, col_data in data.items():
            result[col_name] = type(col_data)
        return result

    def create_topic_table(self, topic, data):
        self.logger.debug('Building new table for topic {}'.format(topic))
        column_def = self.get_column_def(data)
        self.create_table(topic, column_def)

    def get_topic_cls(self, topic, data):
        try:
            topic_table = Base.metadata.tables[topic]
        except KeyError:
            self.create_topic_table(topic, data)
            topic_table = Base.metadata.tables[topic]

        return topic_table.decl_class

    def add_packet(self, session, sender, topic, data):
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
