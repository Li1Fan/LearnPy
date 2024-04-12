from ctypes import *

# load the shared object file
adder = CDLL('/home/frz/c_file/adder.so')

# Find sum of integers
res_int = adder.add_int(4, 5)
print("Sum of 4 and 5 = " + str(res_int))

# Find sum of floats
a = c_float(5.5)
b = c_float(4.1)

add_float = adder.add_float
add_float.restype = c_float
print("Sum of 5.5 and 4.1 = ", str(add_float(a, b)))

# CPython
# ctypes 是 Python 的一个外部库，它允许 Python 调用 C 语言的库函数。这对于 Python 的扩展和性能优化非常有用。
