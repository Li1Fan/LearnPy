# -*- coding: utf-8 -*-
"""
Created on 2022.9.27
Author frz

UDP服务端
"""
import socket

IP = '192.168.222.2'
PORT = 1234


class UdpServer(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.shutdown_flag = False
        self.list_phone = []

    def server_forever(self):
        self.recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.recv_socket.setblocking(False)  # 设置非阻塞
        self.recv_socket.bind((self.ip, self.port))

        def handle(msg, addr):
            """处理报文函数，这里忽略解包，可自定义报文格式解包"""
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            send_socket.bind((self.ip, self.port))
            print(msg)
            print(addr)
            if msg == b'hello':
                send_socket.sendto(b'ok', addr)
            send_socket.close()

        while True:
            try:
                msg, addr = self.recv_socket.recvfrom(1024)
                handle(msg, addr)
            except:
                pass

    def send_discover(self, device_ip, device_port):
        self.recv_socket.sendto(b'hello', (device_ip, device_port))


if __name__ == "__main__":
    t = UdpServer(IP, PORT)
    # t.send_discover('192.168.222.108', 2222)
    t.server_forever()
