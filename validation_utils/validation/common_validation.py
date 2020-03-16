
from validation_utils.errors import CommonErrorMixin
from validation_utils.validation.base_validation import BaseValidation


class ValidationMixin(CommonErrorMixin, BaseValidation):

    def with_raw_data(self, raw_data):
        """
            Method should add raw data to object
            and validate it
            :raw_data - <dict> with raw data
            :rtype - self instance
        """
        self.add_raw_data(raw_data)
        self.validate()
        return self

    def with_error(self, errors):
        """
            Method should add error message to
            object
            :errors - <dict> errors
            :rtype - self
        """
        self.add_errors_messages(errors)
        return self

    def with_serializer(self, serializer):
        """
            Method should add serialiser to object
            :serialize - serializer instance
            :rtype - self
        """
        self.add_serializer(serializer)
        return self
