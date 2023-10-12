import os
import sys

from PyQt5.QtWidgets import QApplication

from config_manage import ConfigManager
from message_box import MessageBox
from ssh_conn import SSHConnection

# 兼容以exe形式运行
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    config_manage = ConfigManager('config.ini')
    ip = config_manage.get_value('info', 'ip')
    port = config_manage.get_value('info', 'port')
    user = config_manage.get_value('info', 'user')
    # pwd = config_manage.get_value('info', 'pwd')
    pwd = 'starnetsvc9000PBX'
    cmd = config_manage.get_value('info', 'cmd')

    my_ssh = SSHConnection(ip=ip, port=port, user=user, passwd=pwd)
    is_connect = my_ssh.connect()

    app = QApplication(sys.argv)

    if is_connect is False:
        print('设备连接失败')
        MessageBox().set_error_box('设备连接失败')
        sys.exit()

    res = my_ssh.do_command(cmd)
    print(res)
    my_ssh.close()
    MessageBox().set_information_box('命令执行成功')
