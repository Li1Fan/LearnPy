# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2020.07.10
Author cmr

Copyright (c) 2020 Star-Net
"""
import os
import subprocess
import time


def Check_Out(_command, _decode='utf-8'):
    # print('_command:{}'.format(_command))
    try:
        return subprocess.check_output(_command, shell=True).decode(_decode)
    except  subprocess.CalledProcessError as exc:
        # print('returncode:', exc.returncode)
        # print('cmd:', exc.cmd)
        # print('output:, exc.output')
        return None


def Call(_command):
    # print('_command:{}'.format(_command))
    return subprocess.call(_command, shell=True)


def Popen(_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    # print('_command:{}'.format(_command))
    return subprocess.Popen(_command, stdout=stdout, stderr=stderr, shell=True)


class OSCommand(object):

    def do_command_by_call(self, command):
        return Call(command)

    def do_command_by_checkout(self, command, _decode='utf-8'):
        return Check_Out(command, _decode)

    def do_command_by_popen(self, command, stdout="PIPE", stderr="PIPE", _decode='utf-8', read_out=True):
        """
        :param command: shell 命令
        :param stdout: None, PIPE,
        :param stderr: None, PIPE,STDOUT
        :return:
        """
        if stdout is None and stderr is None:
            return Popen(command, stdout=None, stderr=None)
        elif stdout == "PIPE" and stderr == "PIPE":
            p = Popen(command, getattr(subprocess, stdout), getattr(subprocess, stderr))
            return p.stdout.read().decode(_decode), p.stderr.read().decode(_decode) if read_out else p
        elif stdout == "PIPE" and stderr == "STDOUT":
            p = Popen(command, getattr(subprocess, stdout), getattr(subprocess, stderr))
            return p.stdout.read().decode(_decode) if read_out else p
        else:
            return Popen(command, stdout, stderr)

    def ping_ip_address(self, ip, num=1):
        p_type, p_outtime = ('n', 'w') if os.name == 'nt' else ('c', 'W')
        o_req, e_req = self.do_command_by_popen(
            'ping {_ip} -{_type} {num} -{out_time} {num}'.format(
                _ip=ip,
                _type=p_type,
                num=num,
                out_time=p_outtime
            ),
            _decode='utf-8'
        )
        return True if "rtt min/avg/max/mdev" in o_req else False

    def do_adb_shell_cmd_by_popen_interactively(self, adb_shell, cmds: list = None, timeout=3):
        """
        在adb shell下执行命令
        :param adb_shell: adb -s 192.168.222.xx shell
        :param cmds: 在adb shell下要顺序执行的命令们
        :param timeout: 默认3s
        :return:
        """
        obj = subprocess.Popen(
            [adb_shell], shell=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for cmd in cmds:
            obj.stdin.write((r"""{}""".format(cmd) + "\n").encode('utf-8'))
        obj.stdin.write('exit\r\n'.encode('utf-8'))  # 重点，一定要执行exit
        stdout, stderr = obj.communicate(timeout=float(timeout))
        text = stdout.decode('utf-8')
        obj.stdin.close()
        obj.stdout.close()
        obj.stderr.close()
        obj.kill()
        cmds.append("exit\r\n")
        del_s = "\r\n".join(cmds).strip()
        return text.replace(del_s, "").strip()


if __name__ == '__main__':
    osc = OSCommand()
    cmd = r"ps -ef |grep 'utools --enable' | awk '{print $2}'"
    r = osc.do_command_by_popen(cmd)
    print(r)
    pid_list = r[0].strip().split('\n')
    if len(pid_list) >= 3:
        r1 = osc.do_command_by_popen('kill -9 {}'.format(pid_list[0]))
        print(r1)
        time.sleep(0.3)
    r2 = osc.do_command_by_call('utools &')
    print(r2)
    # adb_shell = "adb shell"
    # cmds = ['cd /sn_app/', 'cd /sn_app/']
    # osc = OSCommand()
    # s = osc.ping_ip_address("192.168.222.85")
    # print(s)
