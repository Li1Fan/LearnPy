# -*- coding: utf-8 -*-
import threading

from scapy.layers.inet import IP, ICMP, TCP
from scapy.layers.l2 import ARP
from scapy.packet import fuzz, ls
from scapy.sendrecv import send, sr1, sr, sniff, srp, srp1
from scapy.volatile import RandMAC, RandIP

'''
send sendp 发送
sr sr1 srp srp1发送并接收
sr1和sr的区别在于sr1返回的只有应答包，没有未应答包  #TODO:区别
'''
# 创建IP包
ip_pcap = IP(dst='192.168.222.7')
# send(ip_pcap)

# 创建icmp包，ping
icmp_pcap = IP(dst='192.168.222.7') / ICMP()
# send(icmp_pcap)
icmp_pcap.show()
ls(icmp_pcap)

# ans = sr1(icmp_pcap)
# print(ans.summary())

# 创建TCP报文，TCP建立连接请求，判断端口是否打开
# # ans同时还捕获到了源数据包
# ans, unans = sr(IP(dst="192.168.222.6") / fuzz(TCP(dport=80, flags="S")))  # fuzz会随机填充内容然后发送
#
# for s, r in ans:
#     s.show()
#     r.show()
#     if r[TCP].flags == 18:
#         print("This port is open")
#     if r[TCP].flags == 20:
#         print("This port is closed")

# 监听网卡抓包
# r = sniff(filter='icmp', iface='enp1s0', count=10)
# print(r.nsummary())

# 生成随机MAC、IP
print(RandMAC())
print(RandIP())


def capture():
    # 监听网卡抓包
    r = sniff(filter='arp', iface='enp1s0', count=10)
    print(r.nsummary())


t = threading.Thread(target=capture,)
t.start()

# 创建ARP报文，dpkt？scapy？
arp = ARP(psrc='192.168.222.108', pdst='192.168.222.6')
arp.show()
send(arp)

# ans = sr1(icmp_pcap, timeout=10)
# print(ans.summary())
