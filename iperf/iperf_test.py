import os
import threading
import re
import time

device_ip = '192.168.222.6'
computer_ip = '192.168.222.108'
global device_result
global computer_result


def device_cmd(cmd, ip=None):
    print('设备端执行命令成功')
    if cmd == 's':
        cmd = 'adb shell iperf -s -u -i 1 -p 40000 -P 1'
    elif cmd == 'c':
        cmd = 'adb shell iperf -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(ip)

    result = os.popen(cmd + ' >0.txt')
    # global device_result
    # device_result = result.read()
    # print(device_result)


def computer_cmd(cmd, ip=None):
    print('电脑端执行命令成功')
    if cmd == 's':
        cmd = 'iperf -s -u -i 1 -p 40000 -P 1'
    elif cmd == 'c':
        cmd = 'iperf -c {} -u -p 40000 -i 1 -b 100M -t 10 -l 1400 -w 16777216 -z'.format(ip)

    result = os.popen(cmd + ' > 1.txt')
    # global computer_result
    # computer_result = result.read()
    # print(computer_result)


# TODO:待优化
def pkg_lose_test(value):
    b = re.findall('\d+.\d+[%]|\d+[%]', value)
    c = (float)(b[-1].split('%')[0]) * 100
    if c <= 1:
        print("丢包合格")
        return True
    else:
        print("丢包不合格！")
        return False


def get_file_value(path):
    with open(path) as f:
        print(f.read())
        return f.read()


def device_as_client_test():
    t_server = threading.Thread(target=computer_cmd, args=('s',))
    t_server.setDaemon(True)
    t_server.start()
    time.sleep(1)
    t_client = threading.Thread(target=device_cmd, args=('c', computer_ip))
    t_client.setDaemon(True)
    t_client.start()

    time.sleep(12)
    # os.system('adb disconnect')
    # time.sleep(1)
    pkg_lose_test(get_file_value('1.txt'))


def device_as_server_test():
    t_server = threading.Thread(target=device_cmd, args=('s',))
    t_server.setDaemon(True)
    t_server.start()
    time.sleep(1)
    t_client = threading.Thread(target=computer_cmd, args=('c', device_ip))
    t_client.setDaemon(True)
    t_client.start()

    time.sleep(12)
    # os.system('adb disconnect')
    # time.sleep(1)
    pkg_lose_test(pkg_lose_test(get_file_value('0.txt')))


# os.system('adb disconnect')
# time.sleep(1)
# text = os.popen('adb connect {}:5654'.format(device_ip))
# con = text.buffer.read().decode(encoding='utf-8')
# if 'connected' not in con:
#     print('设备连接失败')
# else:
#     print('设备连接成功')
#
#     device_as_server_test()
#     # device_as_client_test()
#
if __name__ == "__main__":
    for i in range(5):
        device_cmd('c', '192.168.222.108')
        time.sleep(12)