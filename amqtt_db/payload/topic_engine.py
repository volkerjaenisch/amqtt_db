from amqtt_db.base.base_topic import BaseTopicEngine
from amqtt_db.base.errors import TopicNotFound


class TopicEngine(BaseTopicEngine):

    def topic2handler(self, topic):
        """
        Get a handler for a topic according to the payload definitions
        :param topic:
        :return: The handler
        """
        if topic in self.topic_handlers:
            return self.topic_handlers[topic]
        else:
            result = self.match_topic(topic)
            if result is not None:
                self.topic_handlers[topic] = result
                return result
        raise TopicNotFound()

    def match_topic(self, topic):
        """
        Match a topic to an handler according to the config
        :param topic:
        :return: a topic handler
        """
