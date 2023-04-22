"""
Created on 2022.9.27
Author frz

UDP客户端
"""
import socket

packet = b'hello'
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send_socket.bind(('', 1111))  # 可以不需要绑定
# msg, addr = send_socket.recvfrom(1024)
send_socket.sendto(packet, ('192.168.222.2', 1234))  # 发送的packet报文为应用层，UDP需要指定地址以及端口
msg, addr = send_socket.recvfrom(1024)
print(msg)
send_socket.close()