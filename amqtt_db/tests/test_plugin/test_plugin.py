import aiounittest


from amqtt_db.plugin import DBPlugin
from amqtt_db.tests.resources.mockups import get_context, CONFIG_OK, CONFIG_AMQTT_DB_MISSING, \
    CONFIG_PLUGIN_NAME_WRONG, CONFIG_TOPIC_ENGINE_WRONG, CONFIG_NO_DB_CONNECT_STRING, CONFIG_NO_DB_STRUCTURE, \
    CONFIG_WRONG_DB_STRUCTURE


class TestPlugin(aiounittest.AsyncTestCase):

    def test_plugin_loads(self):
        context = get_context(CONFIG_OK)
        _plugin = DBPlugin(context)    # noqa: F841

    def test_plugin_wrong_config(self):
        context = get_context(CONFIG_PLUGIN_NAME_WRONG)
        self.assertRaises(ImportError, DBPlugin, context)

    def test_plugin_amqtt_section_missing(self):
        context = get_context(CONFIG_AMQTT_DB_MISSING)
        self.assertRaises(ImportError, DBPlugin, context)

    def test_plugin_topic_engine_wrong(self):
        context = get_context(CONFIG_TOPIC_ENGINE_WRONG)
        self.assertRaises(ImportError, DBPlugin, context)

    def test_plugin_no_db_connect_string(self):
        context = get_context(CONFIG_NO_DB_CONNECT_STRING)
        self.assertRaises(ImportError, DBPlugin, context)

    def test_plugin_no_db_structure(self):
        context = get_context(CONFIG_NO_DB_STRUCTURE)
        self.assertRaises(ImportError, DBPlugin, context)

    def test_plugin_wrong_db_structure(self):
        context = get_context(CONFIG_WRONG_DB_STRUCTURE)
        self.assertRaises(ImportError, DBPlugin, context)
