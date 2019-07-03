# 2019 Andrii Kovalov andy.kovv@gmail.com

from collections import deque

from validation_mixin.core import ExecuteFuncHandler, MethodFinderMixin


class call_chain(MethodFinderMixin):
    """
        Decorator call chain
    """
    method_itself_call_argument = 'self'

    def __init__(self, *args):
        self.__call_chan = args
        self.__call_stack = deque()

    def __call__(self, wrapped_func):
        def __wrapped(wrapped_self, *args, **kwargs):
            self.make_call_stack(wrapped_func, wrapped_self)

            original_func_result = None

            for execute_handler in self.__call_stack:

                execute_handler.execute(wrapped_self, *args, **kwargs)
                if execute_handler.is_main:
                    original_func_result = execute_handler.execution_result

            return original_func_result

        return __wrapped

    def get_method_(self, wrapped_self, func_name):
        """
            Method should get method
            :rtype - typle with func instance and flag private/protected
        """
        private_func = self.get_private_method(wrapped_self, func_name)
        if private_func:
            return private_func, True

        protected_func = self.get_protected_method(wrapped_self, func_name)
        if protected_func:
            return protected_func, False

        raise AttributeError(
            f"Method {func_name} not found in class"
        )

    def make_call_stack(self, wrapped_func, wrapped_self):
        """
            Method should make call stack
        """
        for func_name in self.__call_chan:
            if func_name == self.method_itself_call_argument:
                # TODO make manager execute object!! Important!!
                self.__call_stack.append(
                    ExecuteFuncHandler.create(wrapped_func, True, False)
                )
                continue

            method, is_private = self.get_method_(wrapped_self, func_name)
            self.__call_stack.append(
                ExecuteFuncHandler.create(method, False, is_private)
            )