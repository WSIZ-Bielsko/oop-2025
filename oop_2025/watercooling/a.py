
class A:

    def __call__(self, *args, **kwargs):
        return args[0] * args[1]


def compute(a, b, function):
    return function(a, b)


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


if __name__ == '__main__':
    print(compute(1, 2, add))
    print(compute(1, 2, subtract))

    print(isinstance(add, object))

    aa = A()
    print(aa(2,3))