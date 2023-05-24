"""
asyncio 模块：asyncio 是 Python 内置的异步编程模块，可以帮助开发者编写高效的异步程序
    1. 协程：协程是一种用户态的轻量级线程，协程的调度完全由用户控制
    2. 事件循环：事件循环是 asyncio 框架的核心，它负责调度和执行任务
    3. 任务：任务是 asyncio 框架中的最小执行单元，它是对协程的进一步封装
    4. future：future 是协程执行完毕后返回的结果，它和 task 的区别在于，future 是不能取消的，而 task 可以取消
    5. async/await：async/await 是 Python 3.5 之后引入的关键字，用于定义协程

    6. 异步编程：异步编程是一种编程方式，它将任务的执行过程分为多个阶段，每个阶段都可以挂起，然后转而去执行其他任务，从而提高程序的执行效率
    7. 并发编程：并发编程是一种程序设计方式，它允许程序中包含多个同时运行的部分，这些部分可以单独执行，也可以一起执行
    8. 并行编程：并行编程是一种程序设计方式，它允许程序中包含多个同时运行的部分，这些部分可以同时执行
    9. 阻塞：阻塞是指调用函数时当前线程被挂起，直到函数返回结果后才能继续执行
    10. 非阻塞：非阻塞是指在不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回
    11. 同步：同步是指调用函数时当前线程被挂起，直到函数返回结果后才能继续执行
    12. 异步：异步是指在不能立刻得到结果之前，该函数不会阻塞当前线程，而会立刻返回
    13. I/O 密集型任务：I/O 密集型任务是指任务的主要时间消耗在 I/O 操作上的任务，例如文件读写、网络通信等
    14. 计算密集型任务：计算密集型任务是指任务的主要时间消耗在 CPU 计算上的任务，例如大规模的科学计算
    15. 并发：并发是指多个任务交替执行，但是任意时刻只有一个任务在执行
    16. 并行：并行是指多个任务同时执行
    17. 多线程：多线程是指在同一进程内开启多个线程执行任务
    18. 多进程：多进程是指在操作系统中可以同时运行多个进程
    19. 多进程 + 多线程：多进程 + 多线程是指在操作系统中可以同时运行多个进程，每个进程中又可以开启多个线程
    20. 多线程 + 多进程：多线程 + 多进程是指在同一进程内开启多个线程执行任务，每个线程中又可以开启多个进程
    21. 多线程 + 多进程 + 协程：多线程 + 多进程 + 协程是指在同一进程内开启多个线程执行任务，每个线程中又可以开启多个进程，每个进程中又可以开启多个协程
    22. 多进程 + 多线程 + 协程：多进程 + 多线程 + 协程是指在操作系统中可以同时运行多个进程，每个进程中又可以开启多个线程，每个线程中又可以开启多个协程
"""
import asyncio
import time


async def my_coroutine(t, name):
    await asyncio.sleep(t)
    print("协程 {} 执行完毕".format(name))


async def main():
    coroutine1 = my_coroutine(1, 'coroutine1')  # 创建协程对象
    coroutine2 = my_coroutine(2, 'coroutine2')
    coroutine3 = my_coroutine(3, 'coroutine2')
    # await asyncio.gather(coroutine1, coroutine2, coroutine3)  # 并发执行协程对象

    tasks = [coroutine1, coroutine2, coroutine3]
    await asyncio.wait(tasks)  # 并发执行协程对象


if __name__ == "__main__":
    print("start time: {}".format(time.strftime("%H:%M:%S")))

    # # 创建事件循环并运行协程
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    # Python 3.7 之后，可以使用 asyncio.run(main()) 来运行协程
    asyncio.run(main())

    print("stop time: {}".format(time.strftime("%H:%M:%S")))
