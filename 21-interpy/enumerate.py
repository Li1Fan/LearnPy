lst = ["Tom", "Jerry", "Mike", "Tom", "Tom", "Jerry", "Tom"]
for index, item in enumerate(lst, start=1):
    print(index, item)

# dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。
print(dir(lst))
print(dir())

print(__name__)
print(__file__)
