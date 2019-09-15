# 2018 Andrii Kovalov andy.kovv@gmail.com


class validate_with:
    """ Decorator should use for validate data before method call """

    def __init__(self, func_name):
        self.__func_name = func_name
        self.__private_method = None
        self.__protected_method = None

    def __call__(self, func):
        def __wrapped(wrapped_self, *args, **kwargs):

            self.__private_method = self.__get_method(wrapped_self)

            if not self.__private_method:
                # Try find protected or publick method
                self.__protected_method = getattr(
                    wrapped_self, self.__func_name, None
                )

            method_not_found = (
                not self.__private_method and not self.__protected_method)
            if method_not_found:
                raise AttributeError(
                    f'Method not found in class method:{self.__func_name}'
                )

            if self.__private_method:
                self.__private_method(wrapped_self, *args, **kwargs)

            if self.__protected_method:
                self.__protected_method(*args, **kwargs)

            return func(wrapped_self, *args, **kwargs)
        return __wrapped

    def __get_method(self, wrapped_self):
        """ Method should return method by name """
        class_name = wrapped_self.__class__.__name__
        return wrapped_self.__class__.__dict__.get(
            f'{self.__string_formatting(class_name)}{self.__func_name}', None
        )

    def __string_formatting(self, class_name):
        """ Method should return string formatting """
        return f'_{class_name}'


class validate_field:
    """ Decorator should validate field uses marshmalow schema """

    # TODO Think need implement for class decorator
    def __init__(self, field_name):
        self.__field_name = field_name

    def __call__(self, func):
        def __wrapped(wrapped_self, *args, **kwargs):
            validation_class = getattr(wrapped_self, 'validation_class', None)
            if not validation_class:
                raise AttributeError(
                    f'Validation class not defined, please define '
                    f'validation class attribute: validation_class'
                )
            # Check validation fields method
            validate_field_func = getattr(wrapped_self, '_validate_field', None)
            if not validate_field_func:
                raise AttributeError(
                    f'Method for field validation not defined '
                    f'please define _validate_field method'
                )
            income_func_value = self.__get_income_value(*args, **kwargs)
            # Validate income field with schema
            validate_field_func(self.__field_name, income_func_value)
            return func(wrapped_self, *args, **kwargs)
        return __wrapped

    def __get_income_value(self, *args, **kwargs):
        """
            Method should check income value and return it from kwargs or args
            first of all method find value in kwargs, and if value didn't found
            get first value from args
        """
        value = kwargs.get(self.__field_name, None)
        if not value:
            if not len(args):
                raise ReferenceError(
                    f'You must define first positional argument for validation'
                    f' or named argument with name "{self.__field_name}"'
                    f' for value validation'
                )
            value = args[0]
        return value


def validation_required(func):
    # TODO Think! Can implement is empty?? What if need empty dict??
    """
        Decorator should check if validation data
        exists and not empty
    """

    def __wraped(wrapped_self, *args, **kwargs):
        # Check if validated data exists
        validated_data = getattr(wrapped_self, '_validated_data', None)
        if not validated_data:
            raise AttributeError(
                f'You must define validated attribute '
                f'Set self._validated_data'
            )
        return func(wrapped_self, *args, **kwargs)
    return __wraped


def validate(func):
    """
        Decorator should use default class attribute validation_class
        and set _validated_params attribut with values
    """
    default_validate_method = '_validate_income'

    def __wrapped(wrapped_self, *args, **kwargs):
        method = getattr(wrapped_self, default_validate_method, None)
        if not method:
            raise AttributeError(
                f'Default method:{default_validate_method} not found'
                'please define it in the class'
            )
        method()
        return func(wrapped_self, *args, **kwargs)
    return __wrapped


class BaseValidation:
    """ Base validation object """

    default_validation_class_attrib = 'validation_class'
    default_exception_class = 'exception'

    def __init__(self, *args, **kwargs):
        self._raw_data = None
        self._validated_data = None
        self._field = None
        self._validation_errors = list()

    def __new__(cls, *args, **kwargs):
        cls.check_if_validation_class_exist()
        cls.check_if_exception_class_exists()
        return object().__new__(cls)

    @property
    def validated_data(self):
        return self._validated_data

    @classmethod
    def check_if_validation_class_exist(cls):
        """
            Check if validation class not empty for prevent runtime error
        """
        class_dict = cls.__dict__
        if not class_dict.get(cls.default_validation_class_attrib, None):
            raise AttributeError(
                f'Validation class not defined, '
                f'please set validation_class attribute'
            )
        return True

    @classmethod
    def check_if_exception_class_exists(cls):
        """ Check if exception class not empty """
        class_dict = cls.__dict__
        if not class_dict.get(cls.default_exception_class, None):
            raise AttributeError(
                'Exception class not defined, please set exception attribute'
                )
        return True

    def _validate_field(self, field_name, field_value):
        """
            Procedure should validate income field with marshmallow shema,
            redefine procedure for user custom serializer/schema
        """
        income_data = {field_name: field_value}
        schema = self.validation_class(only=(field_name,), partial=True).load(income_data)
        if schema.errors:
            raise self.exception(schema.errors, 400)
        self._field = schema.data[field_name]
        return True

    def _validate_income(self):
        """ Procedure should validate income data """
        many = isinstance(self._raw_data, (list, tuple))
        serializer = self.validation_class(many=many).load(self._raw_data)
        if serializer.errors:
            raise self.exception(serializer.errors, 400)
        self._validated_data = serializer.data
        return True
