# asyncio 模块：asyncio 是 Python 内置的异步编程模块，可以帮助开发者编写高效的异步程序
import asyncio


async def my_coroutine():
    print("Start")
    await asyncio.sleep(1)
    print("End")


# 创建事件循环并运行协程
loop = asyncio.get_event_loop()
loop.run_until_complete(my_coroutine())
