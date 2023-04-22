class C:
    def __init__(self):
        self.attr = 1


c = C()
print(hasattr(c, 'attr'))  # True
print(hasattr(c, 'attr1'))  # False

setattr(c, 'attr', 2)
print(getattr(c, 'attr'))  # 2

delattr(c, 'attr')


# delattr(c, 'attr1')   # AttributeError: attr1

class D:
    def __init__(self):
        self.size = 1

    def getSize(self):
        return self.size + 100

    def setSize(self, value):
        self.size = value ** 2

    def delSize(self):
        del self.size

    sizeValue = property(getSize, setSize, delSize)


# 封装，用户只关心看到的值，内部如何处理不关心
d = D()
print(d.sizeValue)
d.sizeValue = 9
print(d.sizeValue)
