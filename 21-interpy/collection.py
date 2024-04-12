from collections import defaultdict, Counter, deque

my_dict = defaultdict(list)
my_dict['key'].append('value')
print(my_dict)
print(my_dict['key'])
print("-" * 20)

my_dict = {}
my_dict.setdefault('key', []).append('value')
print(my_dict)

tree = lambda: defaultdict(tree)
some_dict = tree()
some_dict['colours']['favourite'] = "yellow"
print(some_dict)


# 使用递归，我们可以创建一个无限深度的字典，但是不易读
def tree():
    return defaultdict(tree)


# 题外话：使用anytree库创建树
from anytree import Node, RenderTree

# 创建树
root = Node("A")
b = Node("B", parent=root)
c = Node("C", parent=root)
d = Node("D", parent=b)
e = Node("E", parent=b)
f = Node("F", parent=c)

# 遍历树
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
print("-" * 20)

# 创建一个 Counter 对象
c = Counter(['a', 'b', 'c', 'a', 'b', 'a'])

# 访问元素出现次数
print(c['a'])  # 输出：3
print(c['b'])  # 输出：2
print(c['c'])  # 输出：1
print('-' * 20)

d = deque(range(5))
print(len(d))
# 输出: 5

print(d.popleft())
# 输出: 0

print(d.pop())
# 输出: 4

print(d)
# 输出: deque([1, 2, 3])

d.insert(0, 'char')
print(d)
d.extend([1, 'right'])
print(d)
d.extendleft([3, 'left'])
print(d)

print('-' * 20)

from collections import namedtuple

# 定义一个命名元组，表示动物，包含三个字段：name, age, type，分别表示名字，年龄，种类
# 这种方式比使用类定义更加简洁，但是不支持方法，且字段是只读的，不能修改
Animal = namedtuple('Animal', 'name age type')
perry = Animal(name="perry", age=31, type="cat")

print(perry)
# 输出: Animal(name='perry', age=31, type='cat')

print(perry.name)
# 输出: 'perry'

# 转为字典，OrderedDict类型，有序字典
print(perry._asdict())
print('-' * 20)

from enum import Enum


# 定义一个枚举类型，表示动物的种类
class Species(Enum):
    cat = 1
    dog = 2
    horse = 3
    aardvark = 4
    butterfly = 5
    owl = 6
    platypus = 7
    dragon = 8
    unicorn = 9
    # 依次类推

    # 但我们并不想关心同一物种的年龄，所以我们可以使用一个别名
    kitten = 1  # (译者注：幼小的猫咪)
    puppy = 2  # (译者注：幼小的狗狗)


Animal = namedtuple('Animal', 'name age type')
perry = Animal(name="Perry", age=31, type=Species.cat)
drogon = Animal(name="Drogon", age=4, type=Species.dragon)
tom = Animal(name="Tom", age=75, type=Species.cat)
charlie = Animal(name="Charlie", age=2, type=Species.kitten)

print(charlie.type == tom.type)
# 输出: True
print(Species(1))
print(Species['cat'])
