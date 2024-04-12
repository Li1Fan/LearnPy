from functools import reduce

lst = [1, 2, 3, 45]
new_lst = map(lambda x: x * x, lst)
# map() 函数返回的是一个迭代器, 可以使用 list() 函数将其转换为列表
print(new_lst, type(new_lst))
print(list(new_lst))
# 使用列表推导式
print([x * x for x in lst])
print("-" * 20)

lst = [1, 2, 3, 45, 36]
new_lst = filter(lambda x: x % 2 == 0, lst)
# filter() 函数返回的是一个迭代器, 可以使用 list() 函数将其转换为列表
print(new_lst, type(new_lst))
print(list(new_lst))
# 使用列表推导式
print([x for x in lst if x % 2 == 0])
print("-" * 20)

lst = [1, 2, 3, 45, 36, 7]
value = reduce(lambda x, y: x + y, lst)
print(value, type(value))
print(sum(lst))
