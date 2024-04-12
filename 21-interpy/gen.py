# iterable object 可迭代对象, 实现了 __iter__ 方法
# __iter__ 返回一个迭代器对象
# (__getitem__ 返回一个元素)

# iterator 迭代器, 实现了 __next__ 方法
# __next__ 返回下一个元素

# iteration 迭代

# for 循环的本质是迭代
# StopIteration 迭代结束的标志

# iter() 从可迭代对象中获取迭代器
# next() 从迭代器中获取下一个元素

# 在 Python 中，实现迭代器的方式有两种：使用类和生成器。
# 使用类实现迭代器，需要实现 __iter__ 和 __next__ 方法。
# 使用生成器实现迭代器，只需要实现一个 yield 语句即可。

# 类
class Gen:
    def __init__(self, seq):
        self.seq = seq
        self.index = 0

    def __iter__(self):
        print('call __iter__')
        return self

    def __next__(self):
        print('call __next__')
        if self.index >= len(self.seq):
            raise StopIteration
        result = self.seq[self.index]
        self.index += 1
        return result


g = Gen([1, 2, 3, 4, 5])
print('g is iterable:', hasattr(g, '__iter__'))
print('g is iterator:', hasattr(g, '__next__'))
# for 循环的本质是迭代, 会调用 __iter__ 方法, 获取迭代器, 然后调用 __next__ 方法, 获取元素
for i in g:
    print(i)
print("-" * 20)

g = Gen([1, 2, 3, 4, 5])
while True:
    try:
        print(next(g))
    except StopIteration:
        break
print("-" * 20)

a = range(10)
print('a is iterable:', hasattr(a, '__iter__'))
print('a is iterator:', hasattr(a, '__next__'))
# for 循环的本质是迭代, 会调用 __iter__ 方法, 获取迭代器, 然后调用 __next__ 方法, 获取元素
for i in a:
    print(i)
print("-" * 20)

iter_a = iter(a)
while True:
    try:
        print(next(iter_a))
    except StopIteration:
        break
print("-" * 20)


# 生成器
def gen(seq):
    for item in seq:
        yield item * item


gen_g = gen([1, 2, 3, 4, 5])
print('gen_g is iterable:', hasattr(gen_g, '__iter__'))
print('gen_g is iterator:', hasattr(gen_g, '__next__'))
while True:
    try:
        print(next(gen_g))
    except StopIteration:
        break
print("-" * 20)


# 应用
# 使用迭代器计算列表中元素的平方和
def square_sum(iterable):
    iterator = iter(iterable)
    result = 0

    try:
        while True:
            element = next(iterator)
            result += element ** 2
    except StopIteration:
        pass

    return result


my_list = [1, 2, 3, 4, 5]
total_square_sum = square_sum(my_list)
print(total_square_sum)  # 输出：55 (1 + 4 + 9 + 16 + 25)
print("-" * 20)


# 使用生成器计算斐波那契数列，更节约内存
def fibon(n):
    a = b = 1
    for i in range(n):
        yield a
        a, b = b, a + b


for num in fibon(10):
    print(num)

iterator = fibon(10)
lst = []
while True:
    try:
        lst.append(next(iterator))
    except StopIteration:
        break
print(lst)
print("-" * 20)
