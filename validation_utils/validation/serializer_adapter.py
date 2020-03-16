from functools import partial


class BaseSerializerAdapter:
    """
        Base serializer adapter
        uses for discover serializer type
        and make interface for call methods
    """
    add_data_method_key = "add_data_method"
    validate_method_key = "validate_method"
    validate_data_handler_key = "validated_data_handler"
    error_data_key = "error_data_handler"

    def __init__(self):
        self.__serializer = None
        self.__map = dict()
        self.__validated_data = dict()

    @property
    def serializer(self):
        return self.__serializer

    @serializer.setter
    def serializer(self, serializer):
        self.__serializer = serializer
        return self

    @property
    def method_map(self):
        return self.__map

    @property
    def validated_data(self):
        method = self.method_map.get(self.validate_method_key)
        validate_data = self.__get_method_helper(method)
        return validate_data

    @classmethod
    def build_(cls, serializer):
        """
            Method should build with serializer
            :serializer - instance of serializer
            :rtype - self
        """
        instance = cls()
        instance.add_serializer(serializer)
        instance.discover_(instance.serializer)
        return instance

    def add_serializer(self, serializer):
        """
            Method should build with serializer
            :serializer - serializer instance
            :rtype - self
        """
        self.__serializer = serializer
        print(id(self.__serializer))
        return self

    def add_data(self, data):
        """
            Method should add data to serializer
            :rtype - self
        """
        # TODO Check if return method instead self?

        serializer_method, argument = self.method_map.get(self.add_data_method_key)
        # method can be like class of fuction base
        # for example class() or class.data()
        # import pdb; pdb.set_trace()
        if argument:
            instance_with_data = serializer_method(**{argument: data})
            self.update_serializer_with_data(instance_with_data)
            return self

        instance_with_data = serializer_method(data)
        self.update_serializer_with_data(instance_with_data)
        return self

    def validate_data(self):
        """
            Method should validate data
            :rtype - value with data
        """

        method = self.method_map.get(self.validate_method_key)
        validate_data_method = self.__get_method_helper(method)
        return validate_data_method()

    def discover_(self, _):
        """
            Methods should discover methods
            :serializer - instance of serializer
            :rtype - self
        """

        if self.is_rest_framework(self.serializer):
            self._add_data_method(self.serializer, 'data')
            self._add_validate_method(self.serializer.is_valid)
            self._add_validated_data_handler(self.serializer.validated_data)
            self._add_error_handler(self.serializer.errors)

        # TODO add for marshmallo

    def update_serializer_with_data(self, serializer_with_data):
        """
            Method should add serializer with data inside
            :serializer_with_data - <instance> with data
            :rtype - <self>
        """
        self.serializer = serializer_with_data
        return self

    def is_rest_framework(self, serializer):
        """
            Method should check if serializer
            type is rest framework
        """
        try:
            from rest_framework.serializers import Serializer
            return issubclass(serializer, Serializer)
        except ImportError:
            return False

    def _add_data_method(self, data_method, data_argument=None):
        """
            Method should add method for add data
            :data_method - func method with
            :data_argument - argument with data
            :return - self
        """
        self.method_map.update({
            self.add_data_method_key: (data_method, data_argument,)
        })
        return self

    def _add_validate_method(self, method):
        """
            Method should add validated method
            :method - non inited method,
            can use with functools partial
            :rtype - self
    """
        self.method_map.update({
            self.validate_method_key: method
        })
        return self

    def _add_validated_data_handler(self, handler):
        """
            Method should add get validated data handler
            :handler  - validated_data handler
            :rtype - self
        """
        self.method_map.update({
            self.validate_data_handler_key: handler
        })
        return self

    def _add_error_handler(self, handler):
        """
            Method should add error handler
            for serializers
            :handler - serializer error handler
            :rtype - self
        """
        self.method_map.update({
            self.error_data_key: handler
        })
        return self

    def __get_method_helper(self, method):
        """
            Method should help get methods from serializer
            :method - serializer method
            :rtype - <method> itself
        """
        if not method:
            raise Exception("Call _add_validate_method() first")

        validate_mehod_name = method.__name__
        validate_data_method = getattr(self.serializer, validate_mehod_name)
        return validate_data_method

    # def __getattr__(self, key):
    #     if key == 'map'
    #     return self[key]
