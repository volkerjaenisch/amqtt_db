import unittest
from datetime import date, time, datetime


from amqtt_db.db.db_sa import SA


class TestSA(unittest.TestCase):

    def test_create_table(self):
        sa = SA(self, 'sqlite:///test.sqlite')

        column_def = {
            'name': str,
            'date': date,
            'time': time,
            'datetime': datetime,
            'int': int,
            'float': float,
            }

        sa.create_table('test', column_def)

