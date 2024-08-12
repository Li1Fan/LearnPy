# from pythrone.log import log
# from pythrone.plugin import PluginArgs
import subprocess


# ### 获取插件配置参数
# def get_plugin_args():
#     input_args = PluginArgs()
#     input_args.add_argument('name_tag', key='tag', default='ADB插件')
#     input_args.add_argument('ip', key='ip', default='192.168.222.98')
#     input_args.add_argument('port', key='port', default='5654')
#     return input_args
#
#
# ### 获取插件依赖
# def get_plugin_deps():
#     return []


def Check_Out(_command, _decode='utf-8'):
    # log.info('_command:{}'.format(_command))
    try:
        return subprocess.check_output(_command, shell=True).decode(_decode)
    except:
        return None


def Call(_command):
    # log.info('_command:{}'.format(_command))
    subprocess.call(_command, shell=True)


def Popen(_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    # log.info('_command:{}'.format(_command))
    return subprocess.Popen(_command, stdout=stdout, stderr=stderr, shell=True)


class AdbPlugin():

    # def init(self, device, config):
    #     self.ip = config.ip
    #     self.port = config.port
    #     self.device = device
    #     self.device.register_obj('adb', self)

    def __init__(self):
        self.ip = '192.168.222.108'
        self.port = '5654'

    def start(self, dev):
        pass

    def end(self, dev):
        self.disconnect()

    def process(self, dev):
        return True

    def off_process(self, device):
        return True

    def exec_adb_shell(self, ip, port, command, _type="is_return"):
        ip = '{}:{}'.format(ip, port)
        log.info('exec_adb_shell,ip:{},command:{},return_type:{}'.format(ip, command, _type))
        if _type == "is_return":
            log.info('adb -s {} shell {}'.format(ip, command))
            response = Check_Out("adb -s {} shell {}".format(ip, command))
            log.info('return:{}'.format(response))
            return response
        Call("adb -s {}:{} shell {}".format(ip, port, command))

    def connect(self, ip=None):
        """
        ADB连接
        :return: bool
        """
        if ip is None:
            ip = self.ip
        command = 'adb connect {}:{}'.format(ip, self.port)
        res = self.do_command_by_popen(command)
        print('连接命令返回的结果：', res)
        if 'connected to {}:{}'.format(ip, self.port) in res[0]:
            return True
        return False

    def disconnect(self):
        """
        ADB断开连接
        :return: bool
        """
        command = 'adb disconnect {}:{}'.format(self.ip, self.port)
        res = self.do_command_by_popen(command)
        print('断开连接返回的结果：', res)
        if res[0].strip() in 'disconnected {}:{}'.format(self.ip, self.port):
            print('当前连接状态', self.adb_status())
            if not self.adb_status():
                return True
        return False

    def adb_status(self):
        """
        状态
        :return: bool
        """
        _info = self.do_command_by_popen('adb devices')
        for _line in _info[0].splitlines():
            if self.ip in _line and _line.endswith("device"):
                return True
        return False

    def do_command_by_call(self, command):
        Call(command)

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

    def adb_pull(self, src_file, dst_file, ip=None):
        """
        adb pull指令,下载文件
        :param src_file: 本地地址
        :param dst_file: 目的地址
        :return: tuple(),[0]:stdout,[1]:stderr
        """
        if ip is None:
            ip = self.ip
        res = self.do_command_by_popen("adb -s {}:{} pull {} {}".format(ip, self.port, src_file, dst_file))
        print('adb pull返回值：', res)
        return res


if __name__ == '__main__':
    a = AdbPlugin()
    # a.init()
    a.connect()
    res = a.adb_status()
    print('res is :{}'.format(res))
