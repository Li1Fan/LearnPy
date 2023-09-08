# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2020.06.11
Author cmr

Copyright (c) 2020 Star-Net
"""
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QFileDialog
from loguru import logger as log


class SSHConsoleWin(QWidget):
    plain_update_signal = pyqtSignal(str)
    message_box_signal = pyqtSignal(str)

    def __init__(self, console, deviceinfo):
        super(SSHConsoleWin, self).__init__()
        self.console = console
        self.deviceinfo = deviceinfo
        self.period_count = 0
        self.buf = str()

        self.timer = QTimer()
        self.timer_period = 50
        self.timer.timeout.connect(self.period_read)

        self.plain_console = QPlainTextEdit()
        # 设置美化效果
        self.plain_console.setStyleSheet("font-family:'Courier New';font-size:14px;")

        self.btn_start = QPushButton('开始')
        self.btn_stop = QPushButton('结束')
        self.btn_stop.setEnabled(False)

        self.btn_save = QPushButton('保存')
        self.btn_save.setEnabled(False)

        self.btn_upload = QPushButton('文件上传')
        self.btn_upload.setEnabled(True)

        self.edit_send = QLineEdit()
        self.btn_send = QPushButton('发送')
        self.btn_send.setEnabled(False)

        self.btn_clear = QPushButton('清屏')
        self.btn_clear.setEnabled(True)

        self.btn_send_ctrl_c = QPushButton('Ctrl+C')
        self.btn_send_ctrl_c.setEnabled(False)

        self.init_ui()
        self.connect_fun()
        self.setWindowTitle('命令下发')

    def init_ui(self):
        self.resize(800, 600)
        self.plain_console.setFont(QFont("黑体", 11))
        self.plain_console.setReadOnly(True)
        self.plain_console.setFocusPolicy(Qt.StrongFocus)
        self.plain_console.setFocus()

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn_start)
        hbox.addWidget(self.btn_stop)

        send_hbox = QHBoxLayout()
        send_hbox.addWidget(self.edit_send)
        send_hbox.addWidget(self.btn_send)

        send_key_hbox = QHBoxLayout()
        send_key_hbox.addStretch(1)
        send_key_hbox.addWidget(self.btn_upload)
        send_key_hbox.addWidget(self.btn_save)
        send_key_hbox.addWidget(self.btn_clear)
        send_key_hbox.addWidget(self.btn_send_ctrl_c)

        vbox = QVBoxLayout()
        vbox.addWidget(self.plain_console)
        vbox.addLayout(send_key_hbox)
        vbox.addLayout(send_hbox)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def period_read(self):
        try:
            buf = self.console.recv()
            if buf:
                print('buf:{}'.format(buf))
            if buf is False:
                self.message_box_signal.emit('控制台开启失败\n请尝试重连或重新登录后再连接')
                self.click_stop_update()
                return
            # 十次周期内的接收删除
            # if self.period_count < 10:
            #     buf = None
            #     self.period_count += 1
            #     if self.period_count == 10:
            #         self.edit_send.returnPressed.emit()  # 触发一下回车
            if buf is not None:
                self.buf += buf
                self.plain_update_signal.emit(buf)
        except Exception as e:
            log.error(e)
            return

    def process_recv(self, buf):
        self.plain_console.moveCursor(QTextCursor.End)
        self.plain_console.insertPlainText(buf)
        self.plain_console.moveCursor(QTextCursor.End)
        self.plain_console.ensureCursorVisible()

    def quit(self):
        self.timer.stop()

    """关联函数"""

    def connect_fun(self):
        self.btn_start.clicked.connect(self.click_start_update)
        self.btn_stop.clicked.connect(self.click_stop_update)
        self.btn_send.clicked.connect(self.click_send_command)
        self.btn_send_ctrl_c.clicked.connect(self.click_send_ctrl_c)
        self.btn_clear.clicked.connect(self.click_clear)
        self.btn_save.clicked.connect(self.click_save)
        self.btn_upload.clicked.connect(self.click_upload)
        self.plain_update_signal.connect(self.process_recv)
        self.edit_send.returnPressed.connect(self.click_send_command)
        self.message_box_signal.connect(self.show_message_box)

    def click_start_update(self):
        """
        接收linux shell的数据 由于其有颜色设置 界面会乱码
        解决思路是：
                  1.对方取消显示颜色的设置
                  2.对接收到的带颜色的数据进行转义或者分割
        目前用的是第一种 alias ls='ls --color=never' 将ls命令设置为不显示颜色
        第二种方法分割可能会有问题 因为格式不是一成不变的
        --- guo chao
        """
        log.info('UI 点击按钮 开始控制台')
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_send.setEnabled(True)
        self.btn_send_ctrl_c.setEnabled(True)
        self.btn_save.setEnabled(True)
        if self.console is None:
            log.error('no console')
            return
        #  解决linux设备 ls乱码命令 ls显示不对齐等
        device_type = self.deviceinfo.get('systemtype', '')
        # if device_type == 'Linux':
        command = "alias ls='ls -1 --color=never'" + '\n'
        self.console.send(command)
        # 此标志位用来标志开始time计时器的周期
        self.period_count = 0
        self.timer.start(self.timer_period)

    def click_stop_update(self):
        log.info('UI 点击按钮 停止控制台')
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_send.setEnabled(False)
        self.btn_send_ctrl_c.setEnabled(False)
        self.btn_save.setEnabled(False)
        if self.console is None:
            log.error('no console')
            return
        self.timer.stop()

    def click_send_command(self):
        log.info('UI 点击按钮 发送命令')
        command = self.edit_send.text().strip()
        log.info('command:{}'.format(command))
        self.edit_send.clear()
        if self.btn_start.isEnabled():
            return
        if self.console is None:
            log.error('no console')
            return
        if 'exit' in command:
            self.message_box_signal.emit('请使用结束按钮退出')
            return
        command = command + '\n'
        self.console.send(command)

    def click_clear(self):
        log.info('UI 点击按钮 控制台清屏')
        self.plain_console.clear()
        self.buf = str()

    def click_send_ctrl_c(self):
        log.info('UI 点击按钮 ctrl+c')
        command = '\x03'
        if self.console is None:
            log.error('no console')
            return
        if 'busybox vi' in command:
            self.message_box_signal.emit('不支持编辑文本')
            return
        elif 'vi' in command:
            self.message_box_signal.emit('不支持编辑文本')
            return
        self.console.send(command)

    @staticmethod
    def show_message_box(message: str):
        # MessageBox().set_information_box('{}'.format(message))
        print(message)

    def click_save(self):
        try:
            directory_name = QFileDialog.getExistingDirectory(self, '选择文件保存路径')
            file_name = 'console_output.txt'
            if directory_name:
                f = open('{}/{}'.format(directory_name, file_name), 'w')
                f.write(str(self.buf))
                f.close()
                self.message_box_signal.emit('保存成功')
            else:
                self.message_box_signal.emit('未选择保存路径')
        except Exception as e:
            self.message_box_signal.emit('保存失败')
            log.error(e)

    def click_upload(self):
        pass


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from ssh_conn import SSHConnection
    from console import SSHConsole
    from device import Device

    app = QApplication(sys.argv)

    ip = '192.168.222.132'
    port = 6102
    user = 'root'
    passwd = 'N2RmMjljY%+jNzM='
    ssh = SSHConnection(ip=ip, port=port, user=user, passwd=passwd)
    if ssh.connect() is not True:
        print('ssh 连接失败')
        exit()

    my_device = Device(ssh)
    console = SSHConsole(device=my_device)

    console_win = SSHConsoleWin(console, {'systemtype': 'Linux'})
    console_win.show()

    sys.exit(app.exec_())
