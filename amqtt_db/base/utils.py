from pydoc import locate

from amqtt_db.base.errors import TypeNotFound


def get_class_by_name(class_path):
    cls = locate(class_path)
    if cls is None:
        raise TypeNotFound('While doing a string to type conversion the type: "{}" cannot be found.'.format(class_path))

    return cls
