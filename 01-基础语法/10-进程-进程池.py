"""
Python中的进程池是一种并发编程的技术，它可以用来提高程序的执行效率和性能。
进程池是一组预先创建好的进程，这些进程可以被重复利用，从而避免了频繁创建和销毁进程的开销。

使用进程池可以将任务分配给多个进程同时执行，从而提高程序的并发性和执行效率。
进程池可以自动管理进程的数量，根据需要动态地创建或销毁进程，从而保证系统资源的最优利用。

在Python中，可以使用multiprocessing模块来创建进程池。
通过创建进程池对象，可以将需要执行的任务添加到进程池中，然后等待进程池中的进程完成任务并返回结果。
这种方式可以大大提高程序的执行效率，特别是在处理大量数据或需要进行密集计算的场景下。
"""
import multiprocessing


def func(a):
    return a * a


def calculate(a):
    return a * a * a


if __name__ == "__main__":
    pool = multiprocessing.Pool()
    lista = [1, 2, 3]
    result = pool.map_async(func, lista).get()  # 要调用get才能得到list返回值
    print(result)
    for i in lista:
        print(pool.apply_async(calculate, args=(i,)).get())
    pool.close()
    pool.join()
