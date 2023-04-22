# <class 'builtin_function_or_method'>

print(type(len))
"""
# 以len()为例
# 内置方法可以通过len()或者.__len__()来调用
# 可以通过自定义类中的__len__()方法来实现len()的功能
"""

"""
__str__ 和 __repr__ 都是 Python 中用于自定义对象表示方式的特殊方法。
__str__ 方法用于返回对象的字符串表示形式，通常用于打印或显示对象的信息。
当您在控制台中使用 print(obj) 或 str(obj) 函数时，Python 会自动调用对象的 __str__ 方法来获取字符串表示形式
需要注意的是，__str__ 方法应该返回一个可读性好的字符串，而不是完整的对象信息。
如果您需要获取对象的完整信息，可以使用 __repr__ 方法。
"""


class MyClass:
    pass


obj = MyClass()
print(obj)  # 默认输出内存地址
print(str(obj))  # 默认输出内存地址
print(repr(obj))  # 默认输出内存地址


class MyClass:
    def __str__(self):
        return 'MyClass object'


obj = MyClass()
print(obj)  # 输出: MyClass object
print(str(obj))  # 输出: MyClass object
print(repr(obj))


class MyClass:
    def __str__(self):
        return 'MyClass object'

    __repr__ = __str__


obj = MyClass()
print(obj)  # 输出: MyClass object
print(str(obj))  # 输出: MyClass object
print(repr(obj))
