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
