"""
Base class for payload decoders
"""


class BaseDecoder(object):

    @staticmethod
    def decode(payload):
        """
        Gecodes a given payload
        :param payload: the payload
        :return: the decoded payload a python data structures
        """
