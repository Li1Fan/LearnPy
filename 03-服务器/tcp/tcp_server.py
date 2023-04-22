# -*- coding: utf-8 -*-
"""
Created on 2022.9.27
Author frz

自定义TCP服务器
"""
import binascii
import errno
import socket
import struct
from threading import Thread

IP = ''
PORT = 16667
BUF_SIZE = 1024
CLIENT_MAX = 100

"""
TCP报文需要自定义报文格式，才能处理粘包分包问题
这里简单定义：
    报文头（18byte）：协议号0x1234（4byte）、报文体长度（4bytes）、Mac（6bytes）、操作码（4bytes）
    报文体：有效数据，json格式
"""
headerSize = 18
protocolType = 0x1234


class TcpServer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # 停止标志位
        self.shutdown_flag = False
        self.client_socket = {}  # 存储socket对象，{Mac：Socket}

    def server_forever(self):
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        self.recv_socket.bind((self.ip, self.port))
        self.recv_socket.listen(CLIENT_MAX)

        def handle_packet(client, packet):
            """处理报文函数"""
            headPack = struct.unpack('!2I6sI', packet[:headerSize])
            protocol_type = headPack[0]
            bodySize = headPack[1]
            mac = headPack[2]
            cmd = headPack[3]
            payload = struct.unpack('{}s'.format(bodySize), packet[headerSize:])
            print(protocol_type, bodySize, mac, cmd)
            mac = binascii.hexlify(mac).decode('utf-8', 'backslashreplace')
            print(mac)
            print(payload[0])
            client.send(b'ok')

        def handle(client, addr):

            dataBuffer = bytes()
            print('Connected by', addr)

            close_flag = False
            while not close_flag:
                try:
                    data = client.recv(BUF_SIZE)  # 阻塞态
                except socket.error as e:
                    if e.errno == errno.ECONNRESET:
                        print('连接被重置')
                    # self.remove_socket(client)
                    break
                # 当recv()返回值小于等于0时，socket连接断开。
                # 但是还需要判断 errno 是否等于 EINTR，如果 errno == EINTR，
                # 则说明recv函数是由于程序接收到信号后返回的，socket连接还是正常的，不应close掉socket连接。
                if not data and errno != errno.EINTR:
                    # self.remove_socket(client)
                    print('连接断开')
                    break
                if data:
                    # 把数据存入缓冲区，类似于push数据
                    dataBuffer += data
                    while True:
                        if len(dataBuffer) < headerSize:
                            # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(dataBuffer))
                            break

                        # 读取包头
                        # struct中:!代表Network order，3I代表3个unsigned int数据
                        headPack = struct.unpack('!2I6sI', dataBuffer[:headerSize])
                        protocol_type = headPack[0]
                        bodySize = headPack[1]
                        cmd = headPack[2]

                        if protocol_type != protocolType:
                            dataBuffer = dataBuffer[2:]
                            client.close()
                            close_flag = True
                            print('非本协议报文，丢弃数据包')

                        # 分包情况处理，跳出函数继续接收数据
                        if len(dataBuffer) < headerSize + bodySize:
                            # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(dataBuffer), headerSize + bodySize))
                            break

                        try:
                            # 解包并处理
                            packet = dataBuffer[:headerSize + bodySize]
                            handle_packet(client, packet)
                            # 粘包情况的处理
                            dataBuffer = dataBuffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出
                        except Exception as e:
                            print(e)
                            print('解包错误')
                            dataBuffer = dataBuffer[headerSize + bodySize:]
                            continue

        while self.shutdown_flag is False:
            try:
                client, addr = self.recv_socket.accept()
                handler = Thread(target=handle, args=(client, addr))
                handler.start()
            except Exception as e:
                print(e)

    def remove_socket(self, client_object):
        for mac in list(self.client_socket.keys()):
            if self.client_socket[mac] == client_object:
                self.client_socket.pop(mac)


if __name__ == "__main__":
    s = TcpServer(IP, PORT)
    s.server_forever()
