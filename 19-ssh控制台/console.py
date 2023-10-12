# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2020.06.12
Author cmr

Copyright (c) 2020 Star-Net
"""
from loguru import logger as log


class SSHConsole(object):

    def __init__(self, device):
        self.device = device

    def recv(self):
        return self.device.recv()

    def send(self, command):
        return self.device.send(command)

    def push(self, local_path, remote_path):
        return self.device.push(local_path, remote_path)

    def send_key(self, key):
        return self.device.send(key)


class TelnetConsole(object):

    def __init__(self, device):
        self.device = device

    def recv(self):
        return self.device.telnet.recv()

    def send(self, command):
        return self.device.telnet.send(command)

# if __name__ == '__main__':
#     import threading
#     import time
#     from util.sshconnection import SSHConnection
#     from business.device.device import Device
#
#     flag = 1
#
#
#     def writeall(device):
#         while flag == 1:
#             data = device.recv()
#             if not data:
#                 continue
#             print('data:{}'.format(data))
#             time.sleep(0.1)
#
#
#     ip = '192.168.222.198'
#     port = 6102
#     user = 'root'
#     passwd = 'ZjN+N~M5ZDFlNTU='
#     ssh = SSHConnection(ip=ip, port=port, user=user, passwd=passwd)
#     ssh.connect()
#     if ssh.connect() is not True:
#         print('ssh 连接失败')
#         exit()
#
#     my_device = Device(ssh, emu=None, dev_info={'lanip': ip}, device_manager=None)
#     console = SSHConsole(my_device)
#
#     print('----recv start----')
#     writer = threading.Thread(target=writeall, args=(my_device,))
#     writer.start()
#
#     print('----send comand----')
#     console.send('ls -l /sdcard/\n')
#     time.sleep(1)
#     console.send('cd /sdcard\n')
#     time.sleep(1)
#     console.send('ls -l\n')
#     time.sleep(1)
#     console.send('exit\n')
#
#     flag = 0
#     print('=============================')
#     print(ssh.is_active())
#     my_device.disconnect()
