from functools import reduce
from collections import OrderedDict

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

# 特殊的几个函数
# def __init__(self, func, *iterables):
#     pass

# map 映射，常用
# 根据func遍历每个元素，组成新列表
lst = [(1, 2), (22, 2), (1, 0)]
lst_2 = map(lambda a: a[0] + 1, lst)
print(list(lst_2))

# filter 过滤
# 遍历所有满足func的元素，组成新列表
lst_2 = filter(lambda a: a[0] > 1, lst)
print(list(lst_2))

# reduce 减少到只剩一个值，少用
# 依次传值进入，最终返回一个值
lst = [1, 2, 3, 4]
r = reduce(lambda a, b: a + b, lst)
print(r)
print(sum(lst))

# TODO 遍历器！！！
#  __inter__ 魔法方法需要学一下
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

# 有序字典
d = OrderedDict([("a", 3), ("b", 4)])
print(f'd:{d} {d.get("a")} {d.get("c", 999)} {d.get("c")}')

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

# 原始字符串
print(r'a\b\n')
# 字节
print(b'hello')
# unicode编码 !!!
print(u'你好，世界')
# format格式化输出
print(f'a:{a}')

# TODO 内置函数
"""
__str__
__repr__
"""

#
"""
1.微信小程序-Web框架、代码、前端
2.基础知识
数据结构 数据库 操作系统 计算机网络 高级编程语音
计算机组成原理、微机原理
模电、数电、电分

3.编码
ascii   英文字符编码 0-127（7位） a=65

gb2312  国标编码 连续两个大于127的字节
        其中，ASCII码中原有的数字字符、英文字符、标点等称为半角字符，大于0x7F的相应字符编码称为全角字符。
gbk     只要出现一个大于128的字节，那么这个字节和它后面一个字节共两个字节就表示一个汉字
ansi    Window编码的称呼，包括gb2312、gbk

unicode 字符集，对世界上所有的字符进行编号
utf-8   节省空间的编码规则
在内存中存储字符时还是使用unicode编码，因为unicode编码的长度固定，处理起来很方便。
而在文件的存储中，则使用utf-8编码，可以压缩内存，节省空间。
这里一般有个自动转换的机制，即从文件中读取utf-8编码到内存时，会自动转换为unicode编码，
                            而从内存中将字符保存到文件时，则自动转换为utf-8编码。
乱码原因：编解码不一致。

4.守护线程
while true; do
 PRO_NOW=$(ps aux|grep demo.py | grep -v grep | wc -l)
 if [ $PRO_NOW = 0 ]; then
  echo died,checktiem:$(date +"%Y%m%d %H:%M:%S.%3N")
  nohup /usr/bin/python3.8 app.py &
 fi
 sleep 5
done
"""
