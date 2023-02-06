import time


# 装饰器
def decorate(func):
    def wrap(*args, **kwargs):
        print(f'start:{time.time()}')
        func(*args, **kwargs)
        print(f'stop:{time.time()}')

    return wrap


def wait_s(t):
    time.sleep(t)
    print('hello world')


# 原理，返回一个函数对象
a = decorate(wait_s)
a(1)
print()


@decorate
def wait_s_new(t):
    time.sleep(t)
    print('hello world')


# 通过装饰器实现重复调用
wait_s_new(1)
print()


# 装饰器带参数
def decorate_with_argue(arg):
    def decorate1(func):
        def wrap(*args, **kwargs):
            print(f'start:{time.time()}')
            func(*args, **kwargs)
            print(arg)
            print(f'stop:{time.time()}')

        return wrap

    return decorate1


@decorate_with_argue('argument')
def fun(t):
    time.sleep(t)
    print('hello world')


fun(1)
print()

# 原理
a = decorate_with_argue('argue')
b = a(wait_s)
b(1)
