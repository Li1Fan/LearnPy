from functools import reduce

# 传值
lst = [1, 22, 2, 1]

a, b, *c = lst
print(a, b, c)

a, b = (1, 2)
print(a, b)

# lambda
f = lambda a: a + 1
print(f(2))

# 排序 key
lst.sort()  # 更改自身值
print(lst)
print(sorted(lst, reverse=True))  # 返回值

lst_1 = [(1, 2), (22, 2), (1, 0)]
lst_1.sort(key=lambda a: a[-1], reverse=True)  # key排序条件，reverse颠倒 默认False
print(lst_1)

# def __init__(self, func, *iterables):
#     pass

# map 映射
# 根据func遍历每个元素，组成新列表
lst = [(1, 2), (22, 2), (1, 0)]
lst_2 = map(lambda a: a[0] + 1, lst)
print(list(lst_2))

# filter 过滤
# 遍历所有满足func的元素，组成新列表
lst_2 = filter(lambda a: a[0] > 1, lst)
print(list(lst_2))

# reduce 减少到只剩一个值
# 依次传值进入，最终返回一个值
lst = [1, 2, 3, 4]
r = reduce(lambda a, b: a + b, lst)
print(r)
print(sum(lst))

# 遍历器！！！魔法方法需要学一下
a = iter([1, 2, 3])
print(next(a))
print(next(a))

# enumerate
for i, j in enumerate(lst, 3):  # start，这个3相当于是原索引上加了3
    print(i, j)

# 字典
a = {1: 2}
b = {2: 3}
# 组合两个字典
c = {**a, **b}
print(c)

c.update({'a': 3})  # 字典增加
print(c)

# 列表生成式
a = [i ** 2 for i in range(10) if i > 3]
print(a)
# 字典生成式
b = {i + '1': j + '1' for (i, j) in {'key': 'value'}.items() if i == 'key'}
print(b)

# 异常捕获
try:
    a = 1 / 0
except (ZeroDivisionError, ValueError):
    print("error")
else:
    print("right")
finally:
    print("over")
# except ZeroDivisionError as e:
#     pass
# except ValueError:
#     pass


# repr打印
print(repr('abc\n'))
print('abc\n')