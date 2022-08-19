# -*- coding: utf-8 -*-
import os

from scapy.all import conf

from pcap.p_capture.send_pacp.product_message import PMessage

raw_socket = conf.L2socket(iface=str('enp1s0'))


def create_packet(data: bytes):
    vlanid = 0
    pmessage = PMessage(0)
    pmessage.vlan_id = vlanid
    pmessage.smac = 'e4:54:e8:c8:8d:e9'
    pmessage.dmac = 'ff:ff:ff:ff:ff:ff'
    pmessage.action = 0x0101
    pmessage.session = 0
    pmessage.payload = data
    packet = pmessage.raw()


# filename = '/home/frz/SSC339-1.1.9-2022-06-14.tar.gz'
filename = '/home/frz/fileTest/0.tar.gz'
size = os.stat(filename).st_size
print(size)
with open(filename, "rb") as f:
    for line in f:
        pass
        a = len(line)
        if a // 1480 == 1:
            raw_socket.send(a[:1480])
            raw_socket.send(a[1480:])
            continue
        if a // 1480 == 2:
            raw_socket.send(a[:1480])
            raw_socket.send(a[1480:])
            raw_socket.send(a[2960:])
            continue
        raw_socket.send(line)  # 发送数据
