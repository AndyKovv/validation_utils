from functools import partial


def default_exception_raise_func(self):
    raise self.exception_class()


class ExceptionBuilder:

    def __init__(self):
        self._exception_class = None
        self._raise_func = None

    @property
    def default_exception_func(self):
        return default_exception_raise_func

    @property
    def exception_class(self):
        return self._exception_class

    @classmethod
    def build_(cls, exception_class, raise_func):
        """
            Method should build exception builder
        """
        instance = cls()
        instance._exception_class = exception_class
        instance._raise_func = (
            raise_func if raise_func else instance.default_exception_func
        )

        return instance

    def raise_(self):
        """
            Method should raise error
            :rtype - <partial> raise error
        """
        return partial(self._raise_func, self)
