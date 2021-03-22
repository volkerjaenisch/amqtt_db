import unittest
from unittest.mock import patch, Mock, MagicMock

from hbmqtt.broker import BrokerContext

from amqtt_db.plugin import DBPlugin



context = MagicMock(BrokerContext)()
context.config = {
    'amqtt_db' : {
        'mapper': 'wide',
        'connect': 'sqlite://test.sqlite'
    }
}


class TestPlugin(unittest.TestCase):

    def test_plugin(self):

        plugin = DBPlugin(context)




if __name__ == '__main__':
    unittest.main()
