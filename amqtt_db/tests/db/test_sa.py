import unittest

from amqtt_db.db.db_sa import SA


class TestSA(unittest.TestCase):

    def test_create_table(self):
        sa = SA(self, 'sqlite:///test.sqlite')

        column_def = {'name': str}

        sa.create_table('test', column_def)

