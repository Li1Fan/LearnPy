# -*- coding: utf-8 -*-
import socket
import time
import struct
import json

host = "localhost"
port = 16667
ADDR = (host, port)
protocolType = 0x1234

if __name__ == '__main__':
    client = socket.socket()
    client.connect(ADDR)

    # 正常数据包定义
    body = json.dumps(dict(hello="world"))
    print(body)
    cmd = 101
    header = [protocolType, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData1 = headPack + body.encode()

    # 分包数据定义
    body = json.dumps(dict(hello="world2"))
    print(body)
    cmd = 102
    header = [protocolType, body.__len__(), cmd]
    headPack = struct.pack("!3I", *header)
    sendData2_1 = headPack + body[:2].encode()
    sendData2_2 = body[2:].encode()

    # 粘包数据定义
    body1 = json.dumps(dict(hello="world3"))
    print(body1)
    cmd = 103
    header = [protocolType, body1.__len__(), cmd]
    headPack1 = struct.pack("!3I", *header)

    body2 = json.dumps(dict(hello="world4"))
    print(body2)
    cmd = 104
    header = [protocolType, body2.__len__(), cmd]
    headPack2 = struct.pack("!3I", *header)

    sendData3 = headPack1 + body1.encode() + headPack2 + body2.encode()

    # 正常数据包
    client.send(sendData1)
    time.sleep(3)

    # 分包测试
    client.send(sendData2_1)
    time.sleep(0.2)
    client.send(sendData2_2)
    time.sleep(3)

    # 粘包测试
    client.send(sendData3)
    time.sleep(3)
    input('stop')
    client.close()
