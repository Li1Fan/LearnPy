"""
Created on 2022.9.27
Author frz

UDP客户端
"""
import socket

packet = b'this is a message'
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send_socket.bind(('', 1111))  # 可以不需要绑定
send_socket.sendto(packet, ('192.168.222.3', 2222))  # 发送的packet报文为应用层，UDP需要指定地址以及端口
send_socket.close()
