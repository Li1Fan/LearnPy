import os
import platform
import subprocess
import threading
import re
import time
import psutil

adb_path = 'G:/adb'
iperf_path = 'G:/iperf'
global device_result
global computer_result


def device_cmd(cmd, ip=None):
    print('设备端执行{}命令成功'.format(cmd))
    global device_result
    device_result = ''
    if cmd == 's':
        if 'win' in platform.system().lower():
            cmd = '{}/adb.exe shell iperf -s -u -i 1 -p 40000 -l 1400 -w 16777216 -P 1'.format(adb_path)
        else:
            cmd = 'adb shell iperf -s -u -i 1 -p 40000 -l 1400 -w 16777216 -P 1'
    elif cmd == 'c':
        if 'win' in platform.system().lower():
            cmd = '{}/adb.exe shell iperf -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(adb_path,
                                                                                                              ip)
        else:
            cmd = 'adb shell iperf -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(ip)
    print(cmd)
    code, output = subprocess.getstatusoutput(cmd)
    if code != 0:
        device_result = ''
    device_result = output


def computer_cmd(cmd, ip=None):
    print('电脑端执行{}命令成功'.format(cmd))
    global computer_result
    computer_result = ''
    if cmd == 's':
        if 'win' in platform.system().lower():
            cmd = '{}/iperf.exe -s -u -i 1 -p 40000 -l 1400 -w 16777216 -P 1'.format(iperf_path)
        else:
            cmd = 'iperf -s -u -i 1 -p 40000 -l 1400 -w 16777216 -P 1'
    elif cmd == 'c':
        if 'win' in platform.system().lower():
            cmd = '{}/iperf.exe -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(iperf_path, ip)
        else:
            cmd = 'iperf -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(ip)
    print(cmd)
    code, output = subprocess.getstatusoutput(cmd)
    if code != 0:
        computer_result = ''
    computer_result = output


def pkg_lose_test(value):
    print(value)
    try:
        b = re.findall('\d+.\d+[%]|\d+[%]', value)
        c = (float)(b[-1].split('%')[0]) * 100
        if c <= 1:
            print("丢包合格")
            return True
        else:
            print("丢包不合格！")
            return False
    except:
        return False


# 这边有不可理解的异常问题，需要区分系统做处理
def device_as_server_test(device_ip):
    if 'win' in platform.system().lower():
        cmd = '{}/adb.exe shell iperf -s -u -i 1 -p 40000 -l 1400 -w 16777216 -P 1'.format(adb_path)
        r = os.popen(cmd)
        print('设备端执行s命令成功')
        print(cmd)
    else:
        t_server = threading.Thread(target=device_cmd, args=('s',))
        t_server.setDaemon(True)
        t_server.start()

    time.sleep(3)
    t_client = threading.Thread(target=computer_cmd, args=('c', device_ip))
    t_client.setDaemon(True)
    t_client.start()
    time.sleep(20)
    kill_iperf()


    if 'win' in platform.system().lower():
        res = pkg_lose_test(computer_result)
    else:
        res = pkg_lose_test(device_result)
    return res


def device_as_client_test(computer_ip):
    t_server = threading.Thread(target=computer_cmd, args=('s',))
    t_server.setDaemon(True)
    t_server.start()
    time.sleep(1)
    t_client = threading.Thread(target=device_cmd, args=('c', computer_ip))
    t_client.setDaemon(True)
    t_client.start()
    time.sleep(15)
    kill_iperf()
    # device_cmd('c', computer_ip)
    # time.sleep(10)

    res = pkg_lose_test(computer_result)
    return res


def kill_iperf():
    for process in psutil.process_iter():
        try:
            cmdline = process.cmdline()
            if "iperf.exe" in str(cmdline):
                process.terminate()
            if "cmd.exe" in str(cmdline):
                process.terminate()
            if "adb.exe" in str(cmdline):
                process.terminate()
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass


def star_iperf(device_ip, computer_ip):
    if 'win' in platform.system().lower():
        os.system('{}/adb.exe disconnect'.format(adb_path))
    else:
        os.system('adb disconnect')
    if 'win' in platform.system().lower():
        text = os.popen('{}/adb.exe connect {}:5654'.format(adb_path, device_ip))
    else:
        text = os.popen('adb connect {}:5654'.format(device_ip))
    con = text.buffer.read().decode(encoding='utf-8')
    if 'connected' not in con:
        # log.info('丢包测试设备{}连接失败'.format(device_ip))
        print('设备连接失败')
        return False
    else:
        # log.info('丢包测试设备{}连接成功'.format(device_ip))
        print('设备连接成功')
    kill_iperf()

    r1 = device_as_client_test(computer_ip)
    print('r1:', r1)
    r2 = device_as_server_test(device_ip)
    print('r2', r2)

    if r1 and r2:
        return True
    else:
        return False


if __name__ == '__main__':
    r = star_iperf('192.168.222.6', '192.168.222.250')
    print(r)
