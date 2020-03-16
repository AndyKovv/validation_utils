
from validation_utils.validation import ValidationMixin
from rest_framework import serializers


class SomeSerializer(serializers.Serializer):

    passed = serializers.BooleanField(required=True)


class SomeClass(ValidationMixin):

    def __init__(self):
        self.__passed = True

    @classmethod
    def build_(cls):
        return cls()

    def update_user_profile(self):
        return "Updated"


class TestsCommonValidationMixin:
    """
        Common validations mixin.
    """
    def tests_for_check_common_validation_for_drf_and_marshmello(self):
        """
            Check if base mixin should 
        """
        error_message_data = {
            "passed": ("Required", 112)
        }
        data = {
            'passed': True
        }

        instance = (
                SomeClass.build_()
                .with_serializer(SomeSerializer)
                .with_error(error_message_data)
                .with_raw_data(data)
                .update_user_profile()
            )
        assert instance == "Updated"

    def test_should_catch_error_with_rest_framework_serializer(self):
        """ Check raise error in rest framework """
        pass