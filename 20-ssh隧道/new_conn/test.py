import time

from conn import SSHConnection

info = {
    "mode": "SU8600P",
    "ssh_ip": "192.168.222.123",
    "ssh_port": 8022,
    "ssh_user": "root",
    "ssh_pwd": "1"
}


def slave_test():
    master_ssh = SSHConnection(info['ssh_ip'], info['ssh_port'], info['ssh_user'], info['ssh_pwd'])
    if master_ssh.connect():
        print('连接成功')
        result = master_ssh.do_command('echo 1')
        print('result:{}'.format(result))

        master_ssh.master_ip = '192.168.5.1'
        master_ssh.slave_ip = '192.168.5.188'
        # 这个比较不好理解
        slave_ssh = master_ssh.slave_connect()
        if slave_ssh:
            print('slave连接成功')
            result = master_ssh.slave_do_command('echo 2')
            print('result:{}'.format(result))
            master_ssh.slave_close()
        master_ssh.close()
    else:
        print('连接失败')


# 这是一种端口转发的方式
def tunnel_test():
    master_ssh = SSHConnection(info['ssh_ip'], info['ssh_port'], info['ssh_user'], info['ssh_pwd'])
    if master_ssh.connect():
        print('连接成功')
        result = master_ssh.do_command('echo 1')
        print('result:{}'.format(result))

        # 连接到ssh或者telnet都可以
        if master_ssh.ssh_tunnel_connect('192.168.5.188', 8022) is True:
            print('隧道创建成功，本地端口：{}'.format(master_ssh.ssh_tunnel_port))
            time.sleep(100)
            master_ssh.ssh_tunnel_close()


if __name__ == '__main__':
    tunnel_test()
