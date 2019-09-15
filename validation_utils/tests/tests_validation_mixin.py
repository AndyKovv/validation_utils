# 2018 Andrii Kovalov andy.kovv@gmail.com

import pytest
from marshmallow import Schema, fields

from validation_utils.validation import (
    validate_with, validate_field, validate, BaseValidation
)
from validation_utils.chains import call_chain


class HttpErrorException(Exception):
    pass


class CallChainTestObject:
    """
        Class should check @call_chain decorator
    """

    def __init__(self):
        self.pre_hook = False
        self.data = dict()
        self.post_hook = False

    @call_chain('pre_hook_fn', 'self', 'post_hook_fn')
    def something_interesting(self):
        self.data.update({"ok": "ok"})

    def pre_hook_fn(self):
        """
            Method should set pre hook
        """
        self.pre_hook = True

    def post_hook_fn(self):
        """
            Method should set post hook
        """
        self.post_hook = True


class ValidationSchema(Schema):

    id = fields.Integer(required=True)
    name = fields.String(required=True)


class MockedObj(BaseValidation):
    validation_class = None
    exception = None


class MockedObjectsVall(BaseValidation):
    validation_class = ValidationSchema
    exception = HttpErrorException

    def __init__(self, **user_params):
        super().__init__()
        self._raw_data = user_params
        # self._validated_data = None

    @validate_with('__validate')
    def get_somesing(self):
        """ Method should return get validation instance """
        return self._validated_data

    @validate_with('_validate_private')
    def get_somesing_private(self):
        """ Method should return get validation instance """
        return self._validated_data

    @validate_with('__not_a_func')
    def create_something(self):
        return None

    @validate_field('name')
    def return_name(self, name):
        return name

    @validate_field('id')
    def return_id(self, id):
        return id

    def __validate(self):
        """ Procedure should validate income data """
        self._validate_income()
        return True

    def _validate_private(self):
        self._validate_income()
        return True


class MockedValidationList(BaseValidation):
    validation_class = ValidationSchema
    exception = HttpErrorException

    def __init__(self, *args):
        super().__init__()
        self._raw_data = args

    @validate
    def get_some(self):
        return self._validated_data


class TestValidationMixinTestsCase:
    """ Tests should implement testing for validation mixin """

    def test_should_raise_error_if_no_validation_class_or_exception_class_defined(self):
        """ Tests should check raise error if no validation classes """
        with pytest.raises(AttributeError):
            MockedObj()

        with pytest.raises(AttributeError):
            MockedObj.validation_class = ValidationSchema
            MockedObj()

        MockedObj.validation_class = ValidationSchema
        MockedObj.exception = HttpErrorException
        MockedObj()

    def test_should_validate_income_data(self):
        """ Test should validate income data"""
        user_params = {
            'id': 1,
            'name': 'Andy'
        }
        obj = MockedObjectsVall(**user_params)
        assert obj.get_somesing() == user_params
        assert obj._validated_data is not None

    def test_shoudl_check_validation_on_private_method(self):
        """ Test should check validation in method in private """
        user_params = {
            'id': 1,
            'name': 'Andy'
        }
        obj = MockedObjectsVall(**user_params)
        assert obj.get_somesing_private() == user_params
        assert obj._validated_data is not None

    def test_should_raise_validation_error(self):
        """ Test should raise validation error with validation class """
        some_wrong_params = {
            'namek': 'someInt',
            'derec': 'some Spoon'
        }
        obj = MockedObjectsVall(**some_wrong_params)
        with pytest.raises(HttpErrorException):
            obj.get_somesing()

    def test_shoudl_raise_error_if_wrong_validation_function_income(self):
        """ Test should raise error if validation funtion not defined """
        obj = MockedObjectsVall()
        with pytest.raises(AttributeError):
            obj.create_something()

    def test_should_validate_income_params_from_list(self):
        """ Test should validate income prams if prams in list """
        params = [
            {
                'id': 1,
                'name': 'Andy'
            },
            {
                'id': 2,
                'name': 'Kovv'
            }
        ]
        obj = MockedValidationList(*params)
        assert obj.get_some() == params

    def test_should_raise_error_if_income_params_not_valid(self):
        """ Tets should raise exception if validate params is invalid"""
        params = [
            {
                'some_id': 1,
                'some_name': 'Name'
            },
            {
                'some_id': 2,
                'some_name': 'Name'
            }
        ]
        obj = MockedValidationList(*params)
        with pytest.raises(HttpErrorException):
            obj.get_some()

    def test_should_validate_only_income_field(self):
        """ Test should validate method only with income fields """
        user_params = {
            'id': 1,
            'name': 'Andy'
        }
        obj = MockedObjectsVall(**user_params)
        result = obj.return_name('Andy')
        assert result == 'Andy'

    def test_should_raise_error_if_validation_params_invalid_or_empty(self):
        """ Test should check if validation params is invalid or empty """
        user_params = {
            'id': 1,
            'name': 'Andy'
        }
        obj = MockedObjectsVall(**user_params)
        with pytest.raises(MockedObjectsVall.exception):
            obj.return_id('Andy')

    def test_should_test_call_chain_decorator(self):
        """ Check chain decorator """
        inst = CallChainTestObject()
        inst.something_interesting()
        assert inst.pre_hook
        assert inst.data['ok'] == 'ok'
        assert inst.post_hook

    def test_should_check_if_call_instance_not_found_in_object(self):
        """ Check if called method not found """
        pass
