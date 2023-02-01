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


# 原理
a = decorate(wait_s)
a(1)


@decorate
def wait_s_new(t):
    time.sleep(t)
    print('hello world')


# 通过装饰器实现重复调用
wait_s_new(1)


# 装饰器带参数
def decorate_with_argue(arg):
    def decorate(func):
        def wrap(*args, **kwargs):
            print(f'start:{time.time()}')
            func(*args, **kwargs)
            print(f'stop:{time.time()}')
            print(arg)

        return wrap

    return decorate


@decorate_with_argue('argue')
def fun():
    print(1)


fun()
