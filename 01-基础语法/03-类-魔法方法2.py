"""
__dict__ 方法返回一个对象的属性字典，其中包含对象的所有属性和它们的值。
属性字典是一个字典对象，键是属性名称，值是属性值。您可以使用 __dict__ 方法来动态添加、修改或删除对象的属性
"""


class MyClass:
    def __init__(self, x):
        self.x = x


obj = MyClass(10)
print(obj.__dict__)  # 输出: {'x': 10}

obj.y = 20  # 动态添加属性
print(obj.__dict__)  # 输出: {'x': 10, 'y': 20}

del obj.x  # 删除属性
print(obj.__dict__)  # 输出: {'y': 20}

"""
__dir__ 方法返回一个对象的属性列表，其中包含对象的所有属性和方法的名称。
属性列表是一个字符串列表，每个字符串表示一个属性或方法的名称。您可以使用 __dir__ 方法来查看一个对象的所有属性和方法
"""


class MyClass:
    def foo(self):
        pass

    def bar(self):
        pass


obj = MyClass()
print(
    dir(obj))
# 输出:
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',

"""
需要注意的是，__dir__ 方法返回的属性列表可能包含一些内置属性和方法，
这些属性和方法不是对象自己的属性和方法，而是 Python 的内置属性和方法。
如果您只想查看对象自己的属性和方法，可以使用 vars(obj) 函数来获取对象的属性字典，然后使用字典的 keys() 方法来获取属性名称列表
"""


class MyClass:
    def foo(self):
        pass

    def bar(self):
        pass


obj = MyClass()
print(list(vars(obj).keys()))  # 输出: []
obj.x = 10
print(list(vars(obj).keys()))  # 输出: ['x']

print([attr for attr in dir(obj) if not attr.startswith('__') and not attr.endswith('__')])
# 输出: ['bar', 'foo', 'x']
