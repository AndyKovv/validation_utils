
from .parse_message_functions import parse_message_function


class CommonErrorMixin:

    errors_list = NotImplemented
    error_lib = NotImplemented

    # parse_message_function_for_serializer = parse_message_function  # TODO implement this.
    parse_message_function_for_single_error = None  # TODO implement this.

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, *kwargs)
        instance._error_fields_messages = dict()
        instance._error_message = dict()
        instance._schema = None
        instance._schema_errors = None
        return instance

    def parse_message_function_for_serializer(self):
        """
            @overridable
            Method should return parse message function
            :rtype - message function
        """
        return parse_message_function

    def add_errors_messages(self, error):
        """
            Method should add errors messages
            :error - error instance
            :rtype - self instance
        """
        parse_messages = self.parse_message_function_for_serializer()
        errors_messages = parse_messages(error)
        self._error_fields_messages.update(errors_messages)
        return self

    def add_error_message(self, error):
        """
            Method should add error message
            :message - <dict> with error message
            :rtype - <self> with instance
        """
        error_message = self.parse_message_function_for_single_error(*error)
        self._error_message.update(error_message)
        return self

    def add_schema(self, schema):
        """
            Method should add schema
            :schema - schema instance
            :rtype - self
        """
        self._schema = schema
        return self

    def raise_for_message(self, status_code=400):
        """
            Method should raise error messge
        """

        if not self._error_message:
            raise AttributeError("Call add_error_message()")

        self.error_lib.with_error(**self._error_message).raise_(status_code)

    def raise_(self, status_code):
        """
            Method should raise error
            :status_code - response status code
        """
        self.__message_required()

        if self._schema_errors:
            self.error_lib(
                errors_messages=self._error_fields_messages
            ).process_schema(self._schema_errors).raise_(status_code)

        self.error_lib.with_error(**self._error_message).raise_(status_code)

    def __message_required(self):
        """
            Method should check if message exist
        """
        message_exist = self._error_message or self._error_fields_messages
        if not message_exist:
            raise AttributeError(
                "Call add_error_message() for single error "
                "or add_errors_messages() for serializer errors "
            )

    def __serializer_required(self):
        """
            Method should check if serializer exist
        """
        if not self._schema:
            raise AttributeError(
                "shema attribute not exist, call add_schema() first"
            )
