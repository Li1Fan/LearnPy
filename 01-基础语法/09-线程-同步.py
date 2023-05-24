"""
互斥只需要保证同时只有一个线程在处理临界资源。
而所谓同步就是有顺序的执行，拿最经典的生产者-消费者为例，必须要先生产出产品，才能消费。存在先后顺序！
threading.Semaphore()信号量
acquire，当sema大于0时才会执行下面语句，并且sema-1
release，sema+1
"""
import random
import threading
import time

empty = threading.Semaphore(3)
full = threading.Semaphore(0)
rlock = threading.RLock()
items = []


def consumer():
    global items
    while True:
        time.sleep(1)
        full.acquire()  # full.acquire必须要在rlock.qcquire之前，否则可能会死锁

        rlock.acquire()
        item = items.pop(0)
        rlock.release()

        empty.release()  # empty.release和rlock.release顺序无关系
        print("consume %d items:%s \n" % (item, items))


def producer():
    global items
    while True:
        empty.acquire()

        rlock.acquire()  # 同consumer
        item = random.randint(0, 100)
        items.append(item)
        rlock.release()

        full.release()
        print("produce %d items:%s \n" % (item, items))


if __name__ == '__main__':
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start()
    t2.start()
