
def make_error_message(field_name, additional_info, code):
    """
        Function should make error message
        :field_name - <str> with field name
        :code - <int> with code
        :additional_info - <str> with text
    """
    return {
        'name': field_name,
        'additional_info': additional_info,
        'code': code
    }


def parse_message_function(
    errors,
    make_error_message_function=make_error_message
):
    """
        Method should parse message
        :rtype - parsed_data
    """
    parsed_messages = dict()
    for field_name, tuple_with_info in errors.items():
        additional_info = tuple_with_info[0]
        code = tuple_with_info[1]
        message = {
            field_name: make_error_message_function(
                field_name, additional_info, code
            )
        }
        parsed_messages.update(message)

    return parsed_messages


__all__ = (
    'make_error_message',
    'parse_message_function'
)
