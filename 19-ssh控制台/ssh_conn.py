# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2022.03.07
Author gc
Copyright (c) 2020 Star-Net
"""
import random

import paramiko
import sshtunnel
from loguru import logger as log
from paramiko.py3compat import u
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException
from scp import SCPClient


class SSHConnection(object):

    def __init__(self, ip, port, user, passwd):
        """
        SSH 连接初始化
        :param ip: 远端ip
        :param port: 远端端口
        :param user: SSH 用户名
        :param passwd: SSH 密码
        """
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.ssh = None
        self.chan = None  # 交互式通道
        self.chan_command = None
        self.ssh_tunnel = None
        self.ssh_tunnel_ip = None
        self.ssh_tunnel_port = None
        self.master_ip = None
        self.slave_ip = None
        self.slave_ssh = None
        self.slave_chan = None

    def get_pwd(self):
        return self.passwd

    def get_chan(self):
        return self.chan

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, self.port, self.user, self.passwd, auth_timeout=30.0, timeout=30.0,
                             banner_timeout=30.0)
            self.chan = self.ssh.invoke_shell()  # 交互式通道
            self.chan.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            self.chan_command = self.ssh.invoke_shell()
            self.chan_command.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            return True
        except NoValidConnectionsError as e:
            log.error('NoValidConnectionsError')
            log.error(e)
        except AuthenticationException as e:
            log.error('AuthenticationException')
            log.error(e)
        except Exception as e:
            log.error(e)
        self.close()
        return False

    def is_active(self):
        if self.ssh is None:
            raise ValueError('SSH is not connect to {}:{}'.format(self.ip, self.port))
        if self.ssh.get_transport() is None:
            raise ConnectionError('Transport is None')
        if self.ssh.get_transport().active is False:
            raise ConnectionError('SSH session not active')

    def chan_is_open(self):
        if self.chan is None:
            raise ValueError('Chan is None {}:{}'.format(self.ip, self.port))
        if self.chan.closed is True:
            self.chan = self.ssh.invoke_shell()
            self.chan.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            if self.chan.closed is True:
                raise ConnectionError('Chan is closed {}:{}'.format(self.ip, self.port))

    def chan_command_is_open(self):
        if self.chan_command is None:
            raise ValueError('Chan command is None {}:{}'.format(self.ip, self.port))
        if self.chan_command.closed is True:
            self.chan_command = self.ssh.invoke_shell()
            self.chan_command.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            if self.chan_command.closed is True:
                raise ConnectionError('Chan command is closed {}:{}'.format(self.ip, self.port))

    def close(self):
        """
        关闭 SSH 连接
        :return:
        """
        if self.ssh is None:
            return
        self.ssh.close()
        self.ssh = None
        if self.slave_ssh is None:
            return
        self.slave_ssh.close()
        self.slave_ssh = None

    def do_command(self, command, timeout):
        """
        执行命令
        :param commands: commands 命令参数列表
        :return: 返回命令执行结果
        """
        self.is_active()
        _, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)
        ret_code = stdout.channel.recv_exit_status()
        if ret_code == 127:
            raise ValueError('{} : command not found'.format(''))
        elif ret_code != 0:
            errmsg = stderr.read().decode('utf-8')
            raise ValueError('do command error : {} \r\nErr Message: {}'.format('', errmsg))
        retmsg = stdout.read().decode('utf-8')
        return retmsg

    def do_commands(self, commands, timeout):
        """
        顺序执行多条ssh命令
        :param commands:
        :return:
        """
        self.is_active()
        cmdstr = commands if not isinstance(commands, list) else '\n'.join(commands)
        _, stdout, stderr = self.ssh.exec_command(cmdstr, timeout=timeout, get_pty=True)  # get_pty 可以执行多条命令
        retmsg = stdout.read().decode('utf-8')
        return retmsg

    def scp_get(self, remote_file, local_file):
        """
        下载文件
        :param remote_file: 远端文件路径
        :param local_file: 本地路径
        :return:
        """
        self.is_active()
        scpclient = SCPClient(self.ssh.get_transport(), socket_timeout=60.0)
        scpclient.get(remote_file, local_file, recursive=True)

    def scp_put(self, local_file, remote_file):
        """
        上传文件
        :param local_file: 本地文件路径
        :param remote_file: 远端路径
        :return:
        """
        self.is_active()
        scpclient = SCPClient(self.ssh.get_transport(), socket_timeout=60.0)
        scpclient.put(local_file, remote_file, recursive=True)

    def send(self, command):
        self.is_active()
        self.chan_is_open()
        self.chan.send(command)

    def send_command(self, command):
        self.is_active()
        self.chan_command_is_open()
        self.chan_command.send(command)

    def recv(self):
        self.is_active()
        self.chan_is_open()
        try:
            x = u(self.chan.recv(65535))
            if len(x) == 0:
                return
            return x
        except:
            return

    def slave_connect(self):
        try:
            master_transport = self.ssh.get_transport()
            master_addr = (self.master_ip, self.port)
            slave_addr = (self.slave_ip, self.port)
            master_channel = master_transport.open_channel("direct-tcpip", slave_addr, master_addr)
            self.slave_ssh = paramiko.SSHClient()
            self.slave_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.slave_ssh.connect(self.slave_ip, self.port, self.user, self.passwd, auth_timeout=30.0, timeout=30.0,
                                   banner_timeout=30.0, sock=master_channel)
            self.slave_chan = self.slave_ssh.invoke_shell()
            self.slave_chan.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            return True
        except NoValidConnectionsError as e:
            log.error('NoValidConnectionsError')
            log.error(e)
        except AuthenticationException as e:
            log.error('AuthenticationException')
            log.error(e)
        except Exception as e:
            log.error(e)
        self.slave_close()
        return False

    def is_slave_active(self):
        if self.slave_ssh is None:
            raise ValueError('Slave SSH is not connect to {}:{}'.format(self.slave_ip, self.port))
        if self.slave_ssh.get_transport() is None:
            raise ConnectionError('Slave Transport is None')
        if self.slave_ssh.get_transport().active is False:
            raise ConnectionError('Slave SSH session not active')

    def slave_chan_is_open(self):
        if self.slave_chan is None:
            raise ValueError('Slave Chan is None {}:{}'.format(self.slave_ip, self.port))
        if self.slave_chan.closed is True:
            self.slave_chan = self.slave_ssh.invoke_shell()
            self.slave_chan.settimeout(0.0)  # 这边需要设置为非阻塞 保持界面功能
            if self.slave_chan.closed is True:
                raise ConnectionError('Slave Chan is closed {}:{}'.format(self.slave_ip, self.port))

    def slave_close(self):
        """
        关闭 SSH 连接
        :return:
        """
        if self.slave_ssh is None:
            return
        self.slave_ssh.close()
        self.slave_ssh = None

    def slave_do_command(self, command, timeout):
        """
        执行命令
        :param command: command 命令参数
        :return: 返回命令执行结果
        """
        self.is_slave_active()
        _, stdout, stderr = self.slave_ssh.exec_command(command, timeout=timeout)
        ret_code = stdout.channel.recv_exit_status()
        if ret_code == 127:
            raise ValueError('{} : command not found'.format(''))
        elif ret_code != 0:
            errmsg = stderr.read().decode('utf-8')
            raise ValueError('do command error : {} \r\nErr Message: {}'.format('', errmsg))
        retmsg = stdout.read().decode('utf-8')
        return retmsg

    def slave_do_commands(self, commands, timeout):
        """
        顺序执行多条ssh命令
        :param commands:
        :return:
        """
        self.is_slave_active()
        cmdstr = commands if not isinstance(commands, list) else '\n'.join(commands)
        _, stdout, stderr = self.slave_ssh.exec_command(cmdstr, timeout=timeout, get_pty=True)  # get_pty 可以执行多条命令
        retmsg = stdout.read().decode('utf-8')
        return retmsg

    def slave_scp_get(self, remote_file, local_file):
        """
        下载文件
        :param remote_file: 远端文件路径
        :param local_file: 本地路径
        :return:
        """
        self.is_slave_active()
        scpclient = SCPClient(self.slave_ssh.get_transport(), socket_timeout=60.0)
        scpclient.get(remote_file, local_file, recursive=True)

    def slave_scp_put(self, local_file, remote_file):
        """
        上传文件
        :param local_file: 本地文件路径
        :param remote_file: 远端路径
        :return:
        """
        self.is_slave_active()
        scpclient = SCPClient(self.slave_ssh.get_transport(), socket_timeout=60.0)
        scpclient.put(local_file, remote_file)

    def slave_send(self, command):
        self.is_slave_active()
        self.slave_chan_is_open()
        self.slave_chan.send(command)

    def slave_recv(self):
        self.is_slave_active()
        self.slave_chan_is_open()
        try:
            x = u(self.slave_chan.recv(65535))
            if len(x) == 0:
                return
            return x
        except:
            return

    def ssh_tunnel_connect(self, telnet_ip, telnet_port=8123):
        try:
            self.ssh_tunnel_ip = '0.0.0.0'
            self.ssh_tunnel_port = random.randint(50000, 60000)
            log.info('telnet_ip {} telnet_port {}'.format(telnet_ip, telnet_port))
            log.info('local_ip {} local_port {}'.format(self.ssh_tunnel_ip, self.ssh_tunnel_port))
            self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(
                (self.ip, self.port),
                ssh_username=self.user,
                ssh_password=self.passwd,
                remote_bind_address=(telnet_ip, telnet_port),
                local_bind_address=(self.ssh_tunnel_ip, self.ssh_tunnel_port)
            )
            self.ssh_tunnel.start()
            return True
        except Exception as e:
            log.error('init ssh tunnel fail error:{}'.format(e))
        self.ssh_tunnel_close()
        return False

    def ssh_tunnel_close(self):
        try:
            if self.ssh_tunnel is None:
                return
            self.ssh_tunnel.close()
            self.ssh_tunnel = None
        except Exception as e:
            log.error(e)

#   if __name__ == '__main__':
#     import time
#     import threading
#
#     my_ip = '192.168.222.198'
#     my_port = 6102
#     my_user = 'root'
#     my_pwd = 'ZjN+N~M5ZDFlNTU='
#     my_ssh = SSHConnection(ip=my_ip, port=my_port, user=my_user, passwd=my_pwd)
#     is_connect = my_ssh.connect()
#     if is_connect is False:
#         print('连接失败')
#         exit()
#
#     flag = 1
#
#
#     def writeall(ssh):
#         while flag == 1:
#             data = ssh.recv()
#             if not data:
#                 continue
#             print('data:{}'.format(data))
#             time.sleep(0.1)
#
#
#     print('----recv start----')
#     writer = threading.Thread(target=writeall, args=(my_ssh,))
#     writer.start()
#     print('----send comand----')
#     my_ssh.send('cat /proc/last_kmsg\n')
#     time.sleep(2)
#     flag = 0
#     my_ssh.close()
