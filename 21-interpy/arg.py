def func_arg(*args):
    print(args, type(args))
    for arg in args:
        print(arg)


func_arg(1, 2, 3, 4, 5)

func_arg(*[1, 2, 3, 4, 5])


def func_kwarg(**kwargs):
    print(kwargs, type(kwargs))
    for key, value in kwargs.items():
        print(key, value)


func_kwarg(a=1, b=2, c=3, d=4, e=5)

func_kwarg(**{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})


def func(arg1, arg2, arg3, *args, **kwargs):
    print(arg1, arg2, arg3)
    print(args)
    print(kwargs)


func(*[1, 2, 3])

func(**{'arg1': 1, 'arg2': 2, 'arg3': 3})


def new_func(*args, **kwargs):
    print('new_func')
    print(args)
    print(kwargs)


class A:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return f'{self.a} {self.b} {self.c}'

    def __repr__(self):
        return f'{self.a} {self.b} {self.c}'

    def some_func(self):
        print('some_func', end=' ')
        print(self.a, self.b, self.c)


a = A('R', 'I', 'P')
print(a)
a.some_func()

# monkey patching
a.some_func = new_func
a.some_func()
