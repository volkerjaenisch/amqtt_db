"""
Shamelessly stolen from
https://www.michaelcho.me/article/method-delegation-in-python
"""


class Delegator(object):
    def __getattr__(self, called_method):
        def __raise_standard_exception():
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, called_method))

        def wrapper(*args, **kwargs):
            delegation_config = getattr(self, 'DELEGATED_METHODS', None)
            if not isinstance(delegation_config, dict):
                __raise_standard_exception()

            delegate_object_str = ''
            for delegate_object_str, delegated_methods in delegation_config.items():
                if called_method in delegated_methods:
                    break
            else:
                __raise_standard_exception()

            delegate_object = getattr(self, delegate_object_str, None)

            return getattr(delegate_object, called_method)(*args, **kwargs)

        return wrapper
