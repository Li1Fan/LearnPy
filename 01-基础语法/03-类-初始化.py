class A:
    pass


"""
父类是继承的类，也称为基类。
子类是从另一个类继承的类，也称为派生类。
"""


class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def print_name(self):
        print(self.firstname, self.lastname)


p = Person("Bill", "Gates")
p.print_name()

"""
1.直接继承，不做任何改变
如果您不想向该类添加任何其他属性或方法，请使用 pass 关键字。
继承父类的所有属性和方法，也不重写或增加方法
"""


class NormalPerson(Person):
    pass


n = NormalPerson('Stephen', 'Curry')
n.print_name()

"""
2.重写方法、新增方法
"""


class Teacher(Person):
    def print_name(self):
        print(f'My name is {self.firstname} {self.lastname}')

    def introduce(self):
        print(f'welcome to my class，i am {self.lastname}')


t = Teacher('James', 'Harden')
t.print_name()
t.introduce()

"""
3.新增属性（一般不会重写属性）
"""


class Student(Person):
    def __init__(self, lname, fname):
        self.age = 19
        super().__init__(fname, lname)  # 保持继承
        # super(Student, self).__init__(fname, lname)  # 同上一句等价，建议用上一句


s = Student('Kobe', 'Bryant')
print(s.age)
print(s.lastname)

"""
3.
重写初始化函数
子类的 __init__() 函数会覆盖对父类的 __init__() 函数的继承。
如需保持父类的 __init__() 函数的继承，请添加对父的 __init__() 函数的调用 - super()
新增属性、方法
"""


class Worker(Person):
    # 类变量
    class_attr1 = '打工人打工魂'
    class_attr2 = '打工都是人上人'

    def __init__(self, fname, lname, age):
        super().__init__(fname, lname)  # 保持继承
        self.age = age
        self.height = 175

    def print_name(self):
        print(f'My name is {self.firstname} {self.lastname}, age is {self.age}')

    def welcome(self):
        print('welcome')
        self.attr = 1
        print(self.attr)


w = Worker('Taylor', 'Swift', '25')
w.print_name()
w.welcome()
print(w.attr)

"""
类变量的特点是，所有类的实例化对象都同时共享类变量，
也就是说，类变量在所有实例化对象中是作为公用资源存在的。
类方法的调用方式有 2 种，既可以使用类名直接调用，也可以使用类的实例化对象调用。
"""
print(w.class_attr1, w.class_attr2)
print(Worker.class_attr1, Worker.class_attr2)
w.class_attr1 = 9  # 只会修改实例对象的变量值，类变量保持不变
print(w.class_attr1)
print(Worker.class_attr1)
Worker.class_attr1 = 9  # 都变
print(w.class_attr1)
print(Worker.class_attr1)

print(Worker.__dict__)  # 打印类的属性

# TODO 实例方法 静态方法 类方法 三种方法的区别
"""
实例方法：第一个参数必须是self，通过实例化对象调用
静态方法：使用@staticmethod装饰，可以通过实例化对象和类名调用
类方法：使用@classmethod装饰，可以通过实例化对象和类名调用
"""

# TODO 变量
"""
#类变量 实例变量
#局部变量 全局变量
#公有、私有变量"""


class A:
    pass


class B(A):
    pass


# 是否为子类
print(issubclass(B, A))  # True
print(issubclass(A, B))  # False
# 是否为实例对象
print(isinstance(B(), A))  # True
