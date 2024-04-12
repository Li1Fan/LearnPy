import sys


class MyClass(object):

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


a = MyClass("name", 1)
print(a.__dict__)
print(sys.getsizeof(a.__dict__))
a.grade = 1


class SlotClass(object):
    # __slots__ 限制对象的属性，只能是指定的属性，否则会抛出 AttributeError 异常
    # __slots__ 会使得对象不再有 __dict__ 属性
    # 对于大量对象的情况，可以减少内存占用，提高性能
    __slots__ = ['name', 'identifier']

    def __init__(self, name, identifier):
        self.name = name
        self.identifier = identifier


b = SlotClass("name", 1)
print(sys.getsizeof(b.__dict__))
try:
    b.grade = 1
except AttributeError as e:
    print(e)
