# -*- coding: utf-8 -*-
"""
Created on 2022.9.27
Author frz

UDP服务端
"""
import socket

recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_socket.bind(('', 22222))

while 1:
    msg, addr = recv_socket.recvfrom(1024)
    print(msg)
    print(addr)
    recv_socket.sendto(b'ok', addr)
