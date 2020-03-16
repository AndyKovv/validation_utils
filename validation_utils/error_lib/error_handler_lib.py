
from .exception_class_storage import ExceptionClassesStorage


class ErrorHandlerLib:
    """
        Error handler library
    """

    instance = None
    raise_key = 'raise_'

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            return object().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__exception_storage = ExceptionClassesStorage()
        self.__temp_class = None
        self.__temp_parser = None

    def register_exception(self, exception_class):
        """
            Method should register exception classes exception class 
        """
        self.__temp_class = exception_class
        self.__try_add_to_storage()
        return self

    def register_parser(self, parser):
        """
            Method should add handler
            :handler - func with logic
            :rtype - self
        """
        self.__temp_class_required()
        self.__temp_parser = parser
        self.__try_add_to_storage()
        self.__clear_temp_data()
        return self

    def __clear_temp_data(self):
        """
            Method should clear temp data:
            :rtype - self
        """
        self.__temp_class = None
        self.__temp_parser = None
        return self

    def __try_add_to_storage(self):
        """
            Method should dump classes to storage
            :rtype - self
        """
        if not self.__temp_class:
            return False

        self.__exception_storage.register(
            self.__temp_class, self.__temp_parser
        )
        return self

    def __temp_class_required(self):
        """
            Method should raise exception
            if client try add handler without excetion class
        """
        if not self.__temp_class:
            raise AttributeError("Call register_exception() first")

    def _exception_(self, key):
        """
            Method should raise exception from storage
            :key - <str> with exception name
        """
        exception_name = key.strip(self.raise_key[:-1]).strip('_')
        exception_ = self.__exception_storage.get(exception_name)
        return exception_.raise_()

    def __getattr__(self, key):
        if key.startswith(self.raise_key):
            return self._exception_(key)

        return self.__dict__[key]


error_ = ErrorHandlerLib()
