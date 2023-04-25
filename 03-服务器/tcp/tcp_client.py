# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on 2022.9.27
Author frz

自定义TCP客户端
"""
import binascii
import socket
import threading
import time
import struct
import json

from scapy.volatile import RandMAC

host = "localhost"
port = 16667
ADDR = (host, port)
BUF_SIZE = 1024
protocolType = 0x1234


def client_connect():
    client = socket.socket()
    client.connect(ADDR)

    # 正常数据包定义
    body = json.dumps(dict(hello="world"))
    print(body)
    cmd = 101
    mac = RandMAC()
    mac = binascii.unhexlify(str(mac).replace(":", ""))
    header = [protocolType, body.__len__(), mac, cmd]
    headPack = struct.pack("!2I6sI", *header)
    sendData1 = headPack + body.encode()

    # 正常数据包
    client.send(sendData1)

    time.sleep(10)
    data = client.recv(BUF_SIZE)
    print(data)


if __name__ == '__main__':
    for i in range(1):
        thread_client = threading.Thread(target=client_connect, )
        thread_client.start()

"""
在上面的示例中，我们使用`socket.setsockopt()`方法设置了`SO_LINGER`选项，
将其值设置为一个长度为8的字节串`b'\x01\x00\x00\x00\x00\x00\x00\x00'`，表示在关闭socket时立即发送RST包，不进行挥手操作。
然后我们关闭了客户端socket。
"""
# client.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, b'\x01\x00\x00\x00\x00\x00\x00\x00')
#
# # 关闭客户端socket
# client.close()
