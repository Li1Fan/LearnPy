"""
concurrent.futures是重要的异步编程库。
内部实现机制非常复杂，简单来说就是开辟一个固定大小为n的进程池/线程池。
进程池中最多执行n个进程/线程，当任务完成后，从任务队列中取新任务。若池满，则排队等待。
参阅 https://zhuanlan.zhihu.com/p/438627177
"""
import random
import time
from concurrent import futures


def returnNumber(number: int) -> int:
    print("start threading {}".format(number))
    time.sleep(random.randint(0, 5))  # 随机睡眠
    print("end threading {}".format(number))
    return number  # 返回参数本身


if __name__ == '__main__':
    with futures.ThreadPoolExecutor(3) as executor:
        # with语句会调用executor.shutdown(wait=True)，在所有线程都执行完毕前阻塞当前线程
        res = executor.map(returnNumber, range(0, 5))
        # 返回一个生成器，遍历的结果为0,1,2,3。无论执行结果先后顺序如何，看输入的iterator顺序
        # 因为线程池为3，所以0~2进池，其中某个执行完后，3进池
        # print(res)
    print("----print result----")
    # for r in res:
    #     print(r)
    print(list(res))
