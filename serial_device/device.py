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
            rnum = self.ser.inWaiting()  # 获取接收到的数据长度
            if rnum == 0:
                continue
            # self.ser.inWaiting()
            buf = self.ser.read(rnum)
            res += buf
        print(res.decode())
        return res.decode()

    def write(self, cmd):
        if cmd == 'stop':
            self.ser.write(chr(0x03).encode())
        else:
            self.ser.write(cmd.encode('utf-8'))
        self.ser.write(b'\n')

    def send_cmd(self, cmd, result, timeout):
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
                            self.dev.send_cmd(cmd, result, int(timeout))
                            time.sleep(int(delay_time))
                    self.dev.connect_status = False
                except Exception as e:
                    print(e)
                    # self.dev = None
                    print('设备断连')


if __name__ == "__main__":
    # test = AutoTest('step.txt', '/dev/ttyUSB0')
    # test.run()

    device = SerialDevice('/dev/ttyUSB0')
    # device.read(3)
    device.write('busybox pwd')
    print(device.ser.read(1000).decode())

    # num = device.ser.inWaiting()
    # print(num)
    # buf = device.ser.read(num)    # # device.ser.write(chr(0x03).encode())
    # print(buf)
