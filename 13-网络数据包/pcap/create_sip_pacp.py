# -*- coding: utf-8 -*-
import copy
import random

from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.packet import Raw, ls
from scapy.utils import rdpcap
from scapy.volatile import RandMAC

src_ip = '1.2.3.4'
dst_ip = '11.22.33.44'
src_mac = RandMAC()
print(src_mac)
dst_mac = RandMAC()
print(dst_mac)

pcaps = rdpcap('/home/frz/PycharmProjects/Project/qt_tools/Attack' + "/data/sip/invite.pcap")
pcap = copy.deepcopy(pcaps[0])
pcap[IP].src = src_ip
pcap[IP].dst = dst_ip
pcap[Ether].src = src_mac
pcap[Ether].dst = dst_mac
data = pcap[Raw].load.decode("utf-8")
print(data)
call_id = "UDDlMtlT3qucgjJofGWlwPxbS8gmIye-163884{}5281-0x816f8ea8-000e0c628c8e".format(
    random.randint(100, 999))
branch = "z9hG4bK-61aec363-92a{}d1-638c5504".format(random.randint(100, 999))
tag = "a4789c48-0-13c4-61aec363-2d41f{}-61aec363".format(random.randint(100, 999))
old_call_id = data.split('Call-ID: ')[1].split('@')[0]
old_branch = data.split('branch=')[1].split('\r\n')[0]
old_tag = data.split('tag=')[1].split('\r\n')[0]
number = data.split('INVITE sip:')[1].split('@')[0]
s_ip = data.split('Via: SIP/2.0/UDP ')[1].split(':')[0]
d_ip = data.split('INVITE sip:')[1].split('@')[1].split(':')[0]
pcap[Raw].load = pcap[Raw].load.decode("utf-8").replace('192.168.222.18', src_ip).replace('192.168.222.19',
                                                                                          dst_ip). \
    replace(old_call_id, call_id).replace('branch=' + old_branch, branch). \
    replace(number, "3{}1".format(random.randint(100, 999))).replace('tag=' + old_tag, tag). \
    replace(s_ip, src_ip).replace(d_ip, dst_ip).encode('gbk')
# print(pcap[Raw].load.decode("utf-8"))
pcap[IP].len = len(pcap[IP])
pcap[UDP].len = len(pcap[UDP])
pcap[UDP].chksum = None
pcap[IP].chksum = None
print(pcap[Raw].load.decode("utf-8"))
pcap.show()
