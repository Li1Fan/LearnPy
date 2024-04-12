from functools import wraps


def a_new_decorator(a_func):
    @wraps(a_func)  # 这个装饰器的作用是将函数 a_func 的元信息复制到函数 wrapTheFunction 中
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


def a_function_requiring_decoration():
    print("I am the function which needs some decoration to remove my foul smell")


a_function_requiring_decoration()
print(a_function_requiring_decoration.__name__)
print()

a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration)

a_function_requiring_decoration()
print(a_function_requiring_decoration.__name__)
print()


# 使用 @ 语法糖
# 可以理解为将new_func函数作为参数传递给a_new_decorator函数，然后将a_new_decorator函数的返回值赋值给new_func
# 也就是说，@a_new_decorator等价于new_func = a_new_decorator(new_func)
@a_new_decorator
def new_func():
    print("I am the new function")


new_func()
print()


def logger(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " was called")
        return func(*args, **kwargs)

    return with_logging


# 带参数的装饰器
def logger2(arg1="arg1"):
    def logger1(func):
        @wraps(func)
        def with_logging(*args, **kwargs):
            print(arg1)
            print(func.__name__ + " was called")
            return func(*args, **kwargs)

        return with_logging

    return logger1


@logger2()
def addition_func(x):
    """Do some math."""
    return x + x


result = addition_func(4)
print()


# 还可以以类的形式实现装饰器
class logit(object):
    _logfile = 'out.log'

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        log_string = self.func.__name__ + " was called"
        print(log_string)
        # # 打开logfile并写入
        # with open(self._logfile, 'a') as opened_file:
        #     # 现在将日志打到指定的文件
        #     opened_file.write(log_string + '\n')
        # 现在，发送一个通知
        self.notify()

        # return base func
        return self.func(*args)

    def notify(self):
        # logit只打日志，不做别的
        pass


logit._logfile = 'out2.log'  # 如果需要修改log文件参数


@logit
def myfunc1():
    pass


myfunc1()
