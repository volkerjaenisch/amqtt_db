from datetime import date, datetime, time

from sqlalchemy import create_engine

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
            date: sa.DATE,
            time: sa.TIME,
            datetime: sa.DATETIME,
        }
        self.map.update(_map)


class SA(BaseDB):
    """
    SQLAlchemy storage
    """
    engine = None
    type_mapper = None

    def init_db(self, connect_string):
        """
        Initialize the DB
        """
        self.engine = create_engine(connect_string)
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

    async def add_packet(self, session, sender, topic, data):
        pass
