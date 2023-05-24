"""
多进程和多线程：使用多进程和多线程可以将计算分配到多个 CPU 核心或线程中，从而加快程序的执行速度。
多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响。
而多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，需要格外强调互斥和同步。
多进程适用于计算密集型（如：矩阵运算）任务上，多线程适用于 I/O 密集型（如：文件操作、网络爬虫）任务上。
参阅 https://zhuanlan.zhihu.com/p/438107406
"""
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
