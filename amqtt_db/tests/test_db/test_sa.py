import os
from datetime import date, time, datetime

import unittest

from amqtt_db.db.db_sa import SA
from amqtt_db.tests.resources.mockups import context, publish_packet

from tempfile import NamedTemporaryFile, TemporaryDirectory


class TestSA(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_test_db(self):
        temp_db_file_name = os.path.join(self.temp_dir.name, 'huhu')
        sa = SA(context, 'sqlite:///{}'.format(temp_db_file_name), echo=True)
        return sa

    def test_create_table(self):
        sa = self.create_test_db()

        column_def = {
            'a_name': type('ABC'),
            'a_date': type(date(2021,1,2)),
            'a_time': type(time(23,34,12)),
            'a_datetime': type(datetime(2021,1,2,23,34,12)),
            'a_int': type(123),
            'a_float': type(123.456),
            }

        sa.create_table('tests', column_def)

    def test_add_packet(self):
        sa = self.create_test_db()

        data = {
            'a_name': 'Hugo der Erste der Überflieger',
            'a_date': date(2021,1,2),
            'a_time': time(23,34,12),
            'a_datetime': datetime(2021,1,2,23,34,12),
            'a_int': 1212334,
            'a_float': 0.1234,
            }

        sa.add_packet('test1','abcdef','test/topic', data)

        query = sa.query_topic('test/topic', data)
        query_result = query.all()
        assert len(query_result) == 1
        assert query_result != [None]

