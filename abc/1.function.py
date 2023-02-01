import os


# 函数，可变参数(位置参数、关键字参数)
def func(*args, **kwargs):
    print(args, type(args))
    print(kwargs, type(kwargs))


func(1, 2, a=1, b=2)


# 函数注释（"""回车"""）
def add(a: int, b: int) -> int:
    """
    :param a:加数a
    :param b:加数b
    :return:两者之和
    """
    return a + b


print(add(1, 2))
print(add(1, '2'))
