class A:

    def foo(self):
        print('works')


def goo():
    print('hack')


if __name__ == '__main__':
    a = A()
    a.foo = goo
    a.foo()
