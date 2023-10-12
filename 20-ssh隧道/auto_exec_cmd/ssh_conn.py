# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2022.03.07
Author gc
Copyright (c) 2020 Star-Net
"""
import sys

import paramiko
from loguru import logger as log
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

    def do_command(self, command, timeout=3):
        """
        执行命令
        :param command: commands 命令参数列表
        :param timeout: 命令执行超时时间
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


if __name__ == '__main__':

    my_ip = '192.168.222.110'
    my_port = 22
    my_user = 'root'
    my_pwd = 'starnetsvc9000PBX'
    my_ssh = SSHConnection(ip=my_ip, port=my_port, user=my_user, passwd=my_pwd)
    is_connect = my_ssh.connect()
    if is_connect is False:
        print('连接失败')
        sys.exit()

    print(my_ssh.do_command('date'))

    my_ssh.close()
