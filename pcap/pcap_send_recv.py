# -*- coding: utf-8 -*-
from dpkt.icmp import ICMP
from scapy.layers.inet import IP
from scapy.sendrecv import send

# send三层 sendp二层

ip_pcap = IP(dst='192.168.222.7')
send(ip_pcap)

icmp_pcap = IP(dst='192.168.222.7')/ICMP()
send(icmp_pcap)
