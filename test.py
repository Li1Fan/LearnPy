# import threading
# import time
#
#
# def do_test():
#     for i in range(10):
#         time.sleep(1)
#         print(111)
#
#
# t = threading.Thread(target=do_test, args=())
# # t.setDaemon(True)
# t.start()
# print('退出')
import os
import re

import pyperclip

con = "[  3]  8.0- 9.0 sec  11.4 MBytes  95.5 Mbits/sec   0.207 ms  422/ 8950 (4.7%) \
[  3]  9.0-10.0 sec  11.4 MBytes  95.5 Mbits/sec   0.492 ms  472/ 8998 (5.2%)\
[  3]  0.0-10.0 sec   114 MBytes  95.5 Mbits/sec   0.746 ms 2477/87933 (2.8%)\
"
b = re.findall('\d+.\d+[%]|\d+[%]', con)
print(float(b[-1].split('%')[0]))

value = pyperclip.paste()
print(value, type(value))

a = '234345321'
b = b'55143235'
print(a, type(a))
print(b, type(b))
print(b.decode())

filename = '/home/frz/fileTest/0.tar.gz'
size = os.stat(filename).st_size
print(size)
with open(filename, "rb") as f:
    for line in f:
        pass
        a = len(line)
        if a // 1300 == 1:
            # print(a)
            continue
        if a // 1300 == 2:
            # print(a)
            continue
        if a // 1300 == 0:
            continue
        print(a // 1300)
        # client.send(line)  # 发送数据
a = b'1' + b'12222222222'
print(a)
print(a[0:3])
