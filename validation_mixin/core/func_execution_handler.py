
def dummy_function():
    """ Dummy execution function """
    pass


class ExecuteFuncHandler:
    """
        Execute functions object
        handle function and execution params
    """

    def __init__(self):
        self.__function_pointer = dummy_function
        self.__main_function = False
        self.__is_private = False
        self.__execution_result = None

    @classmethod
    def create(cls, func, is_main, is_private):
        """
            Method shold create handler instace
            :func - pointer to function
            :is_main - bool wrapped_function to call
            :is_private - bool private function to call
            :rtype - instance of self
        """

        return (
            cls()
            .add_function(func)
            .set_is_main(is_main)
            .set_is_private(is_private)
        )

    @property
    def is_main(self):
        return self.__main_function

    def add_function(self, func):
        """
            Method should add function
            :func - instance of func
        """
        self.__function_pointer = func
        return self

    def set_is_main(self, is_main):
        """
            Function should add is main flag
            :is_main - bool value
        """
        self.__main_function = is_main
        return self

    def set_is_private(self, is_private):
        """
            Function should add is main flag
            :is_private - bool value
        """
        self.__is_private = True
        return self

    def execution_result(self):
        """
            Method should return
            execution result
        """
        return self.__execution_result

    def add_execution_result(self, result):
        """
            Method should add execution result
            of function
            :result - any instance of execution
        """
        self.__execution_result = result

    def execute(self, wrapped_self, *args, **kwargs):
        """
            Method should handle excute logic
            :wrapped_self - wrapped self instance
        """

        if self.is_main:
            self.add_execution_result(
                self.__function_pointer(wrapped_self, *args, **kwargs)
            )
            return

        if self.__is_private:
            print(self.__function_pointer())
            self.add_execution_result(
                self.__function_pointer(*args, **kwargs)
            )
            return

        if not self.__is_private:
            self.add_execution_result(
                self.__function_pointer(*args, **kwargs)
            )
            return
