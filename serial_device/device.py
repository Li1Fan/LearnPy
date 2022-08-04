# -*- coding: utf-8 -*-
import threading
import time

from serial import Serial


class SerialDevice(object):

    def __init__(self, port, bps=115200, timeout=1):
        try:
            self.ser = Serial(port, bps, timeout=timeout)
            self.ser_name = self.ser.name
            print('串口打开成功')
        except Exception as e:
            print(e)
            self.ser = None
            print("串口打开失败")
        finally:
            self.connect_status = False

    def __del__(self):
        if self.ser:
            self.ser.close()

    def close(self):
        if self.ser:
            self.ser.close()
        self.ser = None

    def read(self, wait_time):
        current_time = time.time()
        res = b''
        while True:
            offset = time.time() - current_time
            if offset > wait_time:
                break
            # self.ser.in_waiting()
            buf = self.ser.read(1000)
            res += buf
        print(res.decode())
        return res.decode()

    def write(self, cmd):
        if cmd == 'stop':
            self.ser.write(chr(0x03).encode())
        else:
            self.ser.write(cmd.encode('utf-8'))
        self.ser.write(b'\n')

    def excute_cmd(self, cmd, result, timeout):
        self.write(cmd)
        if result in self.read(timeout):
            return True
        else:
            print(f'{result} 回显值未找到')
            return False

    def discover(self):
        while True:
            if not self.connect_status:
                self.write('\n')
                if 'VT40' in self.read(1):
                    print('设备连接成功')
                    self.connect_status = True


class AutoTest(object):
    def __init__(self, script_file, port, bps=115200, timeout=1):
        self.file = script_file
        self.dev = SerialDevice(port, bps, timeout)

    def run(self):
        thread_discover = threading.Thread(target=self.dev.discover)
        thread_discover.start()

        while True:

            if self.dev.connect_status:
                print("开始测试")
                try:
                    with open(self.file, encoding='utf-8') as f:
                        text = f.readlines()
                        print(text)
                        for i, j in enumerate(text):
                            cmd, result, timeout, delay_time = j.split(',')
                            self.dev.excute_cmd(cmd, result, int(timeout))
                            time.sleep(int(delay_time))
                    self.dev.connect_status = False
                except Exception as e:
                    print(e)
                    # self.dev = None
                    print('设备断连')


if __name__ == "__main__":
    test = AutoTest('step.txt', '/dev/ttyUSB0')
    test.run()
    # while True:
    #     print(test.dev.ser.isOpen())
    #     time.sleep(2)
    # device = SerialDevice('/dev/ttyUSB0')
    # # device.ser.in_waiting()
    # buf = device.ser.read(1000)    # # device.ser.write(chr(0x03).encode())
    # print(buf)
    # device.write('')
    # device.read(2)
    # print(device.ser.isOpen())
    # device.excute_cmd('ls\n', 'mnt', 3)
    # time.sleep(1)
    # device.excute_cmd('ifconfig\n', 'eth0', 3)
    # time.sleep(1)
    # device.excute_cmd('top', '1', 3)

    # if device.ser:
    #     device.write('ifconfig\n')
    #     recv = device.read(2)
    #     print(recv)

    # a = input()
    # device.ser.write(b'')
    # cmd = 'ifconfig'
    # device.ser.write(cmd.encode('utf-8'))
    # device.ser.write(b'\n')
    # # device.ser.inWaiting()

    # delay_mark = time.time()
    # res = b''
    # while True:
    #     offset = time.time() - delay_mark
    #     if offset > 5:
    #         break
    #     buf = device.ser.read()
    #     res += buf
    # print(res.decode())
    # while True:
    #
    #     buf = device.ser.read()
    #     # print('com read :', buf, ',len ', len(buf))
    #     if buf:
    #         print(buf.decode())
