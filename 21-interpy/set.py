# 获取重复元素
some_list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
print([x for x in some_list if some_list.count(x) > 1])
duplicates = set([x for x in some_list if some_list.count(x) > 1])
print(duplicates)

# 使用集合推导式
duplicates = {x for x in some_list if some_list.count(x) > 1}
print(duplicates)
print("-" * 20)

# 集合的交集和差集
valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print(input_set.intersection(valid))

valid = set(['yellow', 'red', 'blue', 'green', 'black'])
input_set = set(['red', 'brown'])
print(input_set.difference(valid))
