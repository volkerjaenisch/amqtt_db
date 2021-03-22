

class BaseTypeMapper(object):
    """
    Maps python types to DB Column types
    """

    def __init__(self):
        self.map = {}
