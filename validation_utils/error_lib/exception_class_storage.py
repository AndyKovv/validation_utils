import re
from inspect import signature
from validation_utils.exceptions import (
    ExceptionClassRequired, HandlerParseException
)
from .exception_builder import ExceptionBuilder


class ExceptionClassesStorage:
    """
        Storage for exception Clases
    """
    REG = r"(.+?)([A-Z])"

    exception_builder = ExceptionBuilder
    handler_parser_exception = HandlerParseException
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            return object().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.__registry = dict()
        self.__cached_exceptions = dict()
        self._last_added_key = None  # Maybe remove parasite code

    def register(self, exception_class, parser):
        """
            Method should add exception to registry
            :exception_class - class with exception
            :parser - fucntion with parser
            :rtype - self
        """
        self.__exception_class_required(exception_class)
        self.__validate_parser(parser)
        exception_key = self.__make_exception_key(exception_class)
        self.set_last_added_key(exception_key)

        self.__registry.update(
            {exception_key: (self.exception_builder, exception_class, parser)}
        )
        return self

    def set_last_added_key(self, key):
        """
            Method should set last added key
            :key - <str> representation of keys
            :rtype - <self>
        """
        self._last_added_key = key
        return self

    def get(self, class_name):
        """
            Method should get class by name
            :class_name  - str representation of class_name
        """
        # TODO  add unregistered exception
        instance_from_cache = self.get_from_cache(class_name)
        if instance_from_cache:
            return instance_from_cache

        instances = self.__registry.get(class_name)

        exception_builder_class = instances[0]
        exception_class = instances[1]
        raise_handler = instances[2]

        exception_builder_instance = exception_builder_class.build_(
            exception_class, raise_handler
        )
        self.__add_to_cache(class_name, exception_builder_instance)
        return exception_builder_instance

    def get_from_cache(self, class_name):
        return self.__cached_exceptions.get(class_name)

    def __add_to_cache(self, class_name, exception_builder_instance):
        """
            Method should add to cache
            :
        """
        self.__cached_exceptions.update({
            class_name: exception_builder_instance
        })
        return self

    def __to_snake(self, match):
        return match.group(1).lower() + "_" + match.group(2).lower()

    def __make_exception_key(self, exception_class):
        """
            Method should make exception key
            :exception_class - exception key handler
        """
        class_name = exception_class.__name__
        return re.sub(self.REG, self.__to_snake, class_name, 0)

    def __exception_class_required(self, exception_class):
        """ Method should check exception class """
        if not issubclass(exception_class, Exception):
            raise ExceptionClassRequired(
                "Exception class must be inherite from Exception"
            )

    def __validate_parser(self, parser):
        """
            Method should validate parser
        """
        # Check if parser exist
        if parser is None:
            return True

        params = signature(parser).parameters
        if not params.get('self'):
            raise self.handler_parser_exception(
                "Incorrect parser, add 'self' argument first "
            )
        return True
