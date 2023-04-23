# 多进程和多线程：使用多进程和多线程可以将计算分配到多个 CPU 核心或线程中，从而加快程序的执行速度。
# 使用多进程和多线程
from threading import Thread

numbers = [1, 2, 3, 4, 5, 6]


# 使用多线程
def print_numbers(numbers):
    for number in numbers:
        print(number)


thread = Thread(target=print_numbers, args=(numbers,))
thread.start()
# thread.join()  # 等待线程结束
# Output: 1 2 3 4 5 6
print('Done!')
