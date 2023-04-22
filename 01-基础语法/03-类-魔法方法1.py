"""
在Python的类中，以两个下划线开头、两个下划线结尾的方法，
如常见的 ：__init__、__str__、__del__等，就被称为「魔术方法」（Magic methods）。
魔术方法在类或对象的某些事件出发后会自动执行，如果希望根据自己的程序定制特殊功能的类，那么就需要对这些方法进行重写。
使用这些「魔法方法」，我们可以非常方便地给类添加特殊的功能。
"""


class NewObject(object):
    def __init__(self, attr, *args, **kwargs):
        # 相当于重写初始化方法，要继承基类的属性或方法，必须调用基类的__init__()方法
        # 不重写可以直接pass
        # super(NewObject, self).__init__()
        # super().__init__()
        print('__init__')
        self.attr = attr
        self.args = args
        self.kwargs = kwargs
        print(f'attr:{self.attr}')
        print(f'args:{args}')
        print(f'kwargs:{kwargs}')

    # 实例化首先调用__new__
    def __new__(cls, *args, **kwargs):
        """
        1.只有继承object的新式类才有__new__
        2.__new__至少有一个参数cls,代表当前类
        3.__new__必须要有返回值,返回创建的对象
        """
        print('__new__')
        print(f'args:{args}')
        print(f'kwargs:{kwargs}')
        obj = super(NewObject, cls).__new__(cls)  # NotKnown
        return obj

    def __del__(self):
        """在 Python 中，对象的销毁是由垃圾回收机制来完成的。
        当一个对象不再被引用时，Python 的垃圾回收机制会自动将其标记为垃圾对象，并在适当的时候将其销毁。
        """
        print('__del__')


if __name__ == "__main__":
    test = NewObject('a', 'b', 'c', num='b')
    del test  # 不一定会立即执行__del__方法
    new = NewObject('a', 'b', 'c', num='b')
    print(new.__dict__)  # {'attr': 'a', 'args': ('b', 'c'), 'kwargs': {'num': 'b'}}
    print(new.__dir__())  # ['attr', 'args', 'kwargs']
    print(new.__class__)
