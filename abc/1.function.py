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


# 回调函数 以函数作为参数
# 作用：更加灵活，封装层面只看到中间函数func_callback，真正调用的函数是所传递的参数
def func_callback1(func1, arg):
    func1(arg)


def f1(argument):
    print('callbackL: ' + argument)


def func_callback2(func1, *args):
    func1(*args)


def f2(*args):
    print('callbackL: ' + str(args))


func_callback1(f1, '123')
func_callback2(f2, '123', '456')


# 回调函数实例
def apply_async(func, args, callback):
    """
    func 函数的是处理的函数
    args 表示的参数
    callback 表示的函数处理完成后的 该执行的动作
    """
    result = func(*args)  # !!!
    callback(result)


def add(x, y):
    return x + y


def print_result(result):
    print(result)


apply_async(add, (2, 3), callback=print_result)
