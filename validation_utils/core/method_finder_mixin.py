
class MethodFinderMixin:

    def get_protected_method(self, wrapped_self, func_name):
        """
            Method should get protected method
            :wrapped_self - wraped instance of function
            :func_name - str name of function
        """
        return getattr(wrapped_self, func_name, None)

    def get_private_method(self, wrapped_self, func_name):
        """ Method should return method by name """
        class_name = wrapped_self.__class__.__name__
        return wrapped_self.__class__.__dict__.get(
            f'{self.__string_formatting(class_name)}{func_name}', None
        )

    def __string_formatting(self, class_name):
        """ Method should return string formatting """
        return f'_{class_name}'
