# mutable可变性
var = [1, 2, 3]
print(id(var))
print(var)

new_var = var
print(id(new_var))
print(new_var)
print()

new_var.append(4)
print(new_var)
print(var)

print("-" * 20)


def add_to(num, target=[]):
    target.append(num)
    return target


print(add_to(1))
# 输出: [1]

print(add_to(2))
# 输出: [1, 2]

print(add_to(3))


# 输出: [1, 2, 3]

# 永远不要定义可变类型的默认参数，除非你知道你正在做什么。你应该像这样做：

def add_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target


add_to(42)
# 输出: [42]

add_to(42)
# 输出: [42]

add_to(42)
# 输出: [42]
