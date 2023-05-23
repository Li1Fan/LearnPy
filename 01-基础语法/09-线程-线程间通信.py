"""
常常用queue来实现线程中的通信，以queue.Queue类为例，常用的方法：

-put(item, block=True, timeout=None)
如果 block 为 True ， timeout 为 None （即默认的选项），阻塞写，直到队列为空。如果 timeout 是正整数，那么阻塞大于这个时间，就会抛出一个异常。
如果 block 为 False ，如果队列有空那么会立即插入，否则就立即抛出异常（ timeout 将会被忽略）。
-get(block=True, timeout=None)
同put

-task_done()：表示完成一项任务，即从put到get。每执行一次get操作，都要执行一次task_done，但不要放在put操作后面。
-join()：所有任务都完成了，即队列空了
可以简单理解为，每task_done一次 就从队列里删掉一个元素，这样在最后join的时候根据队列长度是否为零来判断队列是否结束。
"""

import threading
from queue import Queue
import time


def producer(queue, sequence):
    for item in sequence:
        queue.put(item)
        print('Producer notify: %s appended to queue by producer' % (item))
        time.sleep(2)


def consumer(queue):
    while True:  # 一直读
        item = queue.get()  # 阻塞
        queue.task_done()  # get之后要接task_done
        print('Consumer notify : %s popped from queue by consumer' % (item))


if __name__ == '__main__':
    que = Queue()
    t1 = threading.Thread(target=producer, args=(que, [1, 2, 3, 4]))
    t2 = threading.Thread(target=consumer, args=(que,), daemon=True)  # daemon为True，表示守护线程，随着主线程结束而结束
    t3 = threading.Thread(target=consumer, args=(que,), daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()  # t1.join一定写在queue.join之前，t1全部发完消息，再看queue是否done
    que.join()  # 当主线程接受后，threading也会结束，因为daemon为True
    print('all done')

    # 判断是否全部完成也可以通过标志位来判断
    # 当生产者生产完毕后，将标志位设置为True，消费者在消费时判断标志位是否为True，如果为True则退出循环
