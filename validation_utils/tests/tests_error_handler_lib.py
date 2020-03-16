import pytest

from validation_utils.error_lib import error_
from validation_utils.exceptions import HandlerParseException


def common_exception_parser(self, name):
    """ Some additional logic """
    raise self.exception_class(name)


class CommonException(Exception):

    def __init__(self, name):
        self.name = name


def idividual_exception_parser(self, second_name, last_name):
    """ Idividual exception parser """
    raise self.exception_class(second_name, last_name)


def incorect_parser(name, second_name):
    raise Exception()


def incorect_exception_parser_with_wrong_attrib(self, secod_name):
    raise self._wrong_attrib(secod_name)


class IndividualException(Exception):

    def __init__(self, second_name, last_name):
        self.second_name = second_name
        self.last_name = last_name


class OtherException(Exception):
    pass


class NewException(Exception):
    pass


class TestsErrorHandlerLib:

    def test_should_check_raise_exception_class(self):
        """ Check raise exception class with choosen exception """
        instance = error_.register_exception(
            CommonException
        ).register_parser(common_exception_parser)
        name = "Andy"
        with pytest.raises(CommonException):
            instance.raise_common_exception(name)

    def test_should_check_raise_multiple_register_errors(self):
        """ Test should check raise multiple exception class """
        instance = error_.register_exception(
            IndividualException
        ).register_parser(idividual_exception_parser)

        instance.register_exception(OtherException)
        instance.register_exception(NewException)

        with pytest.raises(IndividualException):
            second_name = "Kovv"
            last_name = "Olek"
            instance.raise_individual_exception(second_name, last_name)
            assert instance.second_name == second_name
            assert instance.last_name == last_name

        with pytest.raises(OtherException):
            instance.raise_other_exception()

        with pytest.raises(NewException):
            instance.raise_new_exception()

    def test_should_check_exception_handler_consistency(self):
        """ Test should raise exception if client use incorrect parser """
        with pytest.raises(HandlerParseException):
            error_.register_exception(
                CommonException
            ).register_parser(incorect_parser)

        with pytest.raises(HandlerParseException):
            error_.register_exception(
                CommonException
            ).register_parser(incorect_exception_parser_with_wrong_attrib)
