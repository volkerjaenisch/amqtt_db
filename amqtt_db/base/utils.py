from pydoc import locate

from amqtt_db.base.errors import TypeNotFound


def get_class_func_by_name(class_func_path):
    """
    This simple one liner is a security hazard. Here takes place the conversion of config strings to living
    python classes or functions.
    If your config files are not protected this is the place the hacker will attack.
    :param class_func_path: A given full qualified class or function locator.
    :return: A python object of this thing
    """
    cls = locate(class_func_path)
    if cls is None:
        msg = 'While doing a string to type conversion the type: "{}" cannot be found.'.format(class_func_path)
        raise TypeNotFound(msg)

    return cls
