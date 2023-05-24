"""
threading.Lock()实例化一个Lock，通过acquire和release方法来互斥内存的访问。
RLock可以在同一个线程中被多次acquire，但是必须要注意acquire和release的次数要相同，否则可能会导致死锁。
"""
import threading

shared_resource_with_lock = 0
shared_resource_with_no_lock = 0
COUNT = 100000  # 数量一定要多，否则观察不到异常
shared_resource_lock = threading.Lock()


# 有锁的情况
def increment_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock += 1
        shared_resource_lock.release()

    # 可等价于
    # with shared_resource_lock:
    #     shared_resource_with_lock += 1


def decrement_with_lock():
    global shared_resource_with_lock
    for i in range(COUNT):
        shared_resource_lock.acquire()
        shared_resource_with_lock -= 1
        shared_resource_lock.release()


# 没有锁的情况
def increment_without_lock():
    global shared_resource_with_no_lock
    for i in range(COUNT):
        shared_resource_with_no_lock += 1


def decrement_without_lock():
    global shared_resource_with_no_lock
    for i in range(COUNT):
        shared_resource_with_no_lock -= 1


if __name__ == "__main__":
    t1 = threading.Thread(target=increment_with_lock)
    t2 = threading.Thread(target=decrement_with_lock)
    t3 = threading.Thread(target=increment_without_lock)
    t4 = threading.Thread(target=decrement_without_lock)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    print("the value of shared variable with lock management is %s" % shared_resource_with_lock)
    print("the value of shared variable with race condition is %s" % shared_resource_with_no_lock)

# 结果显示
# the value of shared variable with lock management is 0
# the value of shared variable with race condition is -549701
