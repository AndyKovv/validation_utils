
class A:

    attr_one = []

    def __init__(self):
        print("Init A")

    def push(self, v):
        self.attr_one.append(v)

    def show(self):
        print(self.attr_one)


class B(A):

    attr_one = []

    pass
