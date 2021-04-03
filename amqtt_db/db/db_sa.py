from datetime import date, datetime, time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from amqtt_db.base.base_db import BaseDB

import sqlalchemy as sa


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
            date: sa.types.DATE,
            time: sa.types.TIME,
            datetime: sa.types.DateTime,
        }
        self.map.update(_map)


class SA(BaseDB):
    """
    SQLAlchemy storage
    """
    engine = None
    type_mapper = None
    autocommit = None
    session = None

    def init_db(self, connect_string, autocommit=None):
        """
        Initialize the DB
        """
        self.autocommit = autocommit
        self.engine = create_engine(connect_string)
        self.session = sessionmaker(bind=self.engine, autocommit=self.autocommit)()
        self.type_mapper = SATypeMapper()

    async def create_table(self, name, column_def=None):
        """
        Dynamically create a table from a column definition
        :param name: Table name
        :param column_def: Column definition, dict like
        """
        if column_def is None:
            return

        table_description = {
            '__tablename__': name,
            'id': sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
        }

        for col_name, col_type in column_def.items():
            sa_col_type = self.type_mapper.map[col_type]
            table_description[col_name] = sa.Column(sa_col_type)

        _table = type(name, (Base,), table_description)
        Base.metadata.create_all(self.engine, tables=[Base.metadata.tables[name]])

    def get_column_def(self, data):
        result = {}
        for col_name, col_data in data.items():
            result[col_name] = type(col_data)
        return result

    async def create_topic_table(self, session, sender, topic, data):
        self.logger.debug('Building new table for topic {}'.format(topic))
        column_def = self.get_column_def(data)
        await self.create_table(topic, column_def)

    async def add_packet(self, session, sender, topic, data):
        try:
            topic_table = Base.metadata.tables[topic]
        except KeyError:
            await self.create_topic_table(session, sender, topic, data)
            topic_table = Base.metadata.tables[topic]

        topic_cls = topic_table.decl_class
        topic = topic_cls(**data)

        self.session.add(topic)
        self.session.commit()
