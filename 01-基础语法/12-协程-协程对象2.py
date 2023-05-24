import asyncio
import time


async def others():
    await asyncio.sleep(2)
    return '返回值'


async def func():
    print("执行协程函数内部代码")

    # 遇到IO操作挂起当前协程（任务），等IO操作完成之后再继续往下执行。当前协程挂起时，事件循环可以去执行其他协程（任务）。
    response1 = await others()
    print("IO请求1结束，结果为：", response1)

    response2 = await others()
    print("IO请求2结束，结果为：", response2)


print("start time: {}".format(time.strftime("%H:%M:%S")))
asyncio.run(func())
print("stop time: {}".format(time.strftime("%H:%M:%S")))

"""
示例只创建了一个任务，即：
事件循环的任务列表中只有一个任务，所以在IO等待时无法演示切换到其他任务效果。
在程序想要创建多个任务对象，需要使用Task对象来实现。
# 控制权在func上，func挂起时，事件循环可以去执行其他协程（任务）。
"""
