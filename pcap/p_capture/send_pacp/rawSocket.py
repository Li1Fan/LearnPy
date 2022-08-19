# -*- coding: utf-8 -*-
"""
__version__ = '1.0'

Created on 2022.8.18
Author frz

Copyright (c) 2022 Star-Net
"""
import queue
from src.log.Log import log

from src.util.send_pacp.pcap import WinPcap

packet_data = queue.Queue()


def callback(win_pcap, param, header, pkt):
    """
    抓包的回调，将报文和报头存到队列中
    :param win_pcap: 网卡对象
    :param param: 参数
    :param header: 报文头包括时间戳 报文长度
    :param pkt: 报文数据
    :return: None
    """
    packet_data.put(pkt)


class RawSocket(object):
    def __init__(self, iface):
        super(RawSocket, self).__init__()
        try:
            self.adapter = WinPcap(iface)
            self.adapter.init()
            self.adapter_flag = True
        except:
            self.adapter = None
            self.adapter_flag = False

    def start(self):
        try:
            self.adapter.run(callback=callback)
        except Exception as e:
            log.error(e)

    def stop(self):
        self.adapter.stop()

    def exit(self):
        self.adapter.exit()

    def send(self, pkt):
        self.adapter.send(pkt)

    @staticmethod
    def recv():
        if not packet_data.empty():
            return packet_data.get()
        return None
