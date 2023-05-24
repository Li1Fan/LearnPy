"""
Tasks用于并发调度协程，通过asyncio.create_task(协程对象)的方式创建Task对象，这样可以让协程加入事件循环中等待被调度执行。
除了使用 asyncio.create_task() 函数以外，还可以用低层级的 loop.create_task() 或 ensure_future() 函数。
本质上是将协程对象封装成task对象，并将协程立即加入事件循环，同时追踪协程的状态。
"""
import asyncio
import time


async def func():
    await asyncio.sleep(2)
    return "返回值"


async def main():
    print("main开始")

    # 创建协程，将协程封装到一个Task对象中并立即添加到事件循环的任务列表中，等待事件循环去执行（默认是就绪状态）。
    task1 = asyncio.create_task(func())

    # 创建协程，将协程封装到一个Task对象中并立即添加到事件循环的任务列表中，等待事件循环去执行（默认是就绪状态）。
    task2 = asyncio.create_task(func())

    print("main结束")

    # 当执行某协程遇到IO操作时，会自动化切换执行其他任务。
    # 此处的await是等待相对应的协程全都执行完毕并获取结果
    ret1 = await task1
    ret2 = await task2
    print(ret1, ret2)

    # 也可以使用 asyncio.gather() 函数，它可以并发运行多个任务，返回一个包含所有任务返回值的列表。
    # ret1, ret2 = await asyncio.gather(task1, task2)
    # print(ret1, ret2)

    # 或者使用 asyncio.wait() 函数，它可以并发运行多个任务，返回一个包含所有任务的done和pending的元组。
    # done, pending = await asyncio.wait([task1, task2])
    # print(done, pending)
    # for r in done:
    #     print(r.result())


print("start time: {}".format(time.strftime("%H:%M:%S")))
asyncio.run(main())
print("stop time: {}".format(time.strftime("%H:%M:%S")))
