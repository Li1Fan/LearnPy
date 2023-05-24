# 生成器表达式：与列表推导式和字典推导式类似，使用生成器表达式可以快速生成生成器。
# 生成生成器
numbers = [1, 2, 3, 4, 5, 6]
evens = (x for x in numbers if x % 2 == 0)
print(evens)  # Output: <generator object <genexpr> at 0x0000020D7F6F4C80>
print(tuple(evens))  # 只能被迭代一次！！！
for even in evens:
    print(even)


# 使用生成器表达式可以节省内存，因为它不会一次性生成所有的元素，而是在需要时生成元素。
def square_numbers(numbers):
    for number in numbers:
        yield number ** 2


numbers = [1, 2, 3, 4, 5, 6]
squares = square_numbers(numbers)
for square in squares:
    print(square)
# Output: 1 4 9 16 25 36
